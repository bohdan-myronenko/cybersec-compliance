import os
import json
import datetime as dt
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Iterable, Callable

import polars as pl
from jinja2 import Template

from .universal_logs.sniffers import resolve_format
from .universal_logs.normalizers import normalize_line, parse_time_any
from .kb_loader.loader import load_kb
from .llm_clients.ollama_chat import OllamaChatClient
from .llm_clients.external_chat import ExternalChatClient
from . import config
from .progress import update_progress

ANSWER_PROMPT = """Question:
Generate a concise access-control compliance section using the METRICS JSON and LEGAL TEXTS below.

METRICS JSON:
{metrics_json}

LEGAL TEXTS:
{legal_text}

Instructions:
- Use only the provided legal text for citations.
- Cite clause IDs in brackets (e.g., [NIS2-21.2.i]).
- Keep bullets short (<= 25 words).
"""

ECS_COLS = ["@ts", "user", "src_ip", "dst_ip", "action", "status", "resource", "msg", "raw"]


# --------------------------------------------------------------------
# File reading / normalisation (RBA-aware, streaming)
# --------------------------------------------------------------------
def read_lines(path: Path, limit: Optional[int] = None) -> Iterable[str]:
    """Simple helper to read lines from a file, with optional limit."""
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        if limit is not None:
            for _ in range(limit):
                ln = f.readline()
                if not ln:
                    break
                yield ln
        else:
            for ln in f:
                yield ln


def iter_normalized_records(path: Path, user_format: Optional[str] = None):
    """
    Stream normalised ECS-like records from a file, without loading the whole file.

    For RBA:
    - resolve_format() should detect "rba" from the header.
    - normalize_line(..., "rba") will map each CSV row into ECS_MIN + RBA extras.

    We:
    - Read up to 50 lines as a sample to detect/resolve format.
    - Use that format for the rest of the file.
    - Yield one normalised dict per log line (skipping header rows).
    """
    sample_lines = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for _ in range(50):
            ln = f.readline()
            if not ln:
                break
            sample_lines.append(ln)

        if not sample_lines:
            return

        fmt = resolve_format(sample_lines, user_format=user_format)

        # First yield the sample lines
        for ln in sample_lines:
            if not ln.strip():
                continue
            rec = normalize_line(ln, fmt)
            if rec is not None:
                yield rec

        # Then stream the rest of the file line-by-line
        for ln in f:
            if not ln.strip():
                continue
            rec = normalize_line(ln, fmt)
            if rec is not None:
                yield rec


def normalize_file(path: Path) -> pl.DataFrame:
    """
    Eagerly normalise a whole file into a DataFrame.

    NOTE:
    - Kept only for small tests / debugging.
    - For real RBA workloads, use iter_normalized_records() instead.
    """
    user_format = os.getenv("LOG_FORMAT")
    recs = list(iter_normalized_records(path, user_format=user_format))
    if not recs:
        return pl.DataFrame()
    return pl.DataFrame(recs)


# --------------------------------------------------------------------
# Metrics accumulator (RBA-specific, streaming)
# --------------------------------------------------------------------
@dataclass
class MetricsAccumulator:
    """
    Streaming accumulator for RBA login events.

    We expect normalised records to include at least:
      - "@ts"  : ISO-8601 timestamp string or raw timestamp string
      - "user" : stringified "User ID"
      - "src_ip"
      - "status" : "success" / "fail"
      - "is_attack_ip" : bool-ish
      - "is_account_takeover" : bool-ish
    """

    total_rows: int = 0
    users: set = field(default_factory=set)
    src_ips: set = field(default_factory=set)

    failures_total: int = 0
    successes_total: int = 0
    fail_ip_counts: Counter = field(default_factory=Counter)

    attack_ip_attempts: int = 0
    attack_ip_ips: set = field(default_factory=set)

    account_takeovers: int = 0
    users_with_takeover: set = field(default_factory=set)

    def _to_bool(self, value) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        s = str(value).strip().lower()
        return s in {"1", "true", "yes", "y", "t"}

    def update(self, rec: Dict):
        """Consume a single normalised log record and update counters."""
        self.total_rows += 1

        user = str(rec.get("user") or "").strip()
        src_ip = (rec.get("src_ip") or "").strip()
        status = (rec.get("status") or "").strip().lower()

        if user:
            self.users.add(user)
        if src_ip:
            self.src_ips.add(src_ip)

        # Success / failure
        if status == "fail":
            self.failures_total += 1
            if src_ip:
                self.fail_ip_counts[src_ip] += 1
        elif status == "success":
            self.successes_total += 1

        # Attack IP & Account Takeover flags from RBA
        is_attack_ip = self._to_bool(rec.get("is_attack_ip"))
        is_ato = self._to_bool(rec.get("is_account_takeover"))

        if is_attack_ip:
            self.attack_ip_attempts += 1
            if src_ip:
                self.attack_ip_ips.add(src_ip)

        if is_ato:
            self.account_takeovers += 1
            if user:
                self.users_with_takeover.add(user)

    def finalize(self) -> Dict:
        """Produce a metrics dict compatible with generate_report()."""
        distinct_users = len(self.users)
        distinct_src_ips = len(self.src_ips)

        failures = self.failures_total
        successes = self.successes_total
        auth_total = failures + successes or 1
        fail_rate = failures / auth_total

        top_ips_list = [
            {"ip": ip, "count": int(cnt)}
            for ip, cnt in self.fail_ip_counts.most_common(5)
        ]

        # MFA: RBA dataset has no explicit MFA info → we are honest about that.
        mfa_total_users = distinct_users
        mfa_enabled_users = 0
        mfa_coverage_pct = 0.0

        metrics = {
            "mfa": {
                "total_users": int(mfa_total_users),
                "enabled_users": int(mfa_enabled_users),
                "coverage_pct": float(mfa_coverage_pct),
            },
            "auth_failures": {
                "total": int(failures),
                "success_total": int(successes),
                "fail_rate": float(round(fail_rate, 4)),
                "top_ips": top_ips_list,
                "attack_ip_attempts": int(self.attack_ip_attempts),
                "attack_ip_distinct_ips": int(len(self.attack_ip_ips)),
                "account_takeovers": int(self.account_takeovers),
                "users_with_takeover": int(len(self.users_with_takeover)),
            },
            "admins": {
                # No role information in RBA dataset → cannot infer real admin stats.
                "count": 0,
                "with_mfa": 0,
                "last_review_date": "unknown",
            },
            "exceptions": [],
            "frame": {
                "rows": int(self.total_rows),
                "distinct_users": int(distinct_users),
                "distinct_src_ips": int(distinct_src_ips),
            },
        }

        return metrics


# --------------------------------------------------------------------
# Time windowing (e.g. per week) – uses @ts from RBA
# --------------------------------------------------------------------
def compute_window_start(ts: Optional[dt.datetime], window_days: int) -> str:
    """
    Compute a stable window key given a timestamp and window size in days.

    - For ts=None, returns 'unknown'.
    - For ts, we floor to midnight, then group by blocks of `window_days` days.
    """
    if ts is None:
        return "unknown"

    if ts.tzinfo is not None:
        ts = ts.astimezone(dt.timezone.utc).replace(tzinfo=None)

    date = ts.date()
    ordinal = date.toordinal()
    base_ordinal = (ordinal // window_days) * window_days
    start_date = dt.date.fromordinal(base_ordinal)
    start_dt = dt.datetime.combine(start_date, dt.time.min)
    return start_dt.isoformat()


def build_windowed_metrics_for_dir(
    data_dir: Path, window_days: int = 7
) -> Dict[str, Dict]:
    """
    Stream over all RBA CSV files in data_dir, group events into fixed-duration
    windows (e.g., 7 days), and compute metrics per window without ever
    materialising the full dataset in memory.

    Returns:
        dict: {window_key: metrics_dict}
    """
    acc_by_window: Dict[str, MetricsAccumulator] = {}
    user_format = os.getenv("LOG_FORMAT")  # may be None; sniffers should detect "rba"

    # First, scan for files
    update_progress("scan", "Discovering log files...")
    files = [p for p in data_dir.rglob("*") if p.is_file()]
    update_progress("scan", f"Found {len(files)} file(s) to process")

    # Process each file
    update_progress("normalize", "Starting log normalization...")
    total_records = 0
    for i, p in enumerate(files, 1):
        update_progress("normalize", f"Processing file {i}/{len(files)}: {p.name}")
        
        for rec in iter_normalized_records(p, user_format=user_format):
            total_records += 1
            ts_raw = rec.get("@ts")
            ts: Optional[dt.datetime] = None
            if isinstance(ts_raw, str) and ts_raw.strip():
                ts = parse_time_any(ts_raw)

            window_key = compute_window_start(ts, window_days)
            acc = acc_by_window.get(window_key)
            if acc is None:
                acc = MetricsAccumulator()
                acc_by_window[window_key] = acc
            acc.update(rec)
            
            # Update progress every 10000 records
            if total_records % 10000 == 0:
                update_progress("normalize", f"Processed {total_records:,} records from {i}/{len(files)} files")

    update_progress("metrics", f"Finalizing metrics for {len(acc_by_window)} time window(s)...")
    
    metrics_by_window: Dict[str, Dict] = {}
    for win, acc in acc_by_window.items():
        metrics_by_window[win] = acc.finalize()

    update_progress("metrics", f"Computed metrics: {total_records:,} records across {len(metrics_by_window)} window(s)")
    
    return metrics_by_window


# --------------------------------------------------------------------
# (Legacy) DataFrame-based metrics – for small tests only
# --------------------------------------------------------------------
def enforce_schema_types(df: pl.DataFrame) -> pl.DataFrame:
    """Ensure all expected columns exist and have safe types (no Null dtypes)."""
    for c in ECS_COLS:
        if c not in df.columns:
            df = df.with_columns(pl.lit(None).alias(c))

    text_cols = ["user", "src_ip", "dst_ip", "action", "status",
                 "resource", "msg", "raw"]
    for c in text_cols:
        df = df.with_columns(
            pl.col(c).cast(pl.Utf8, strict=False).fill_null("")
        )

    df = df.with_columns(
        pl.when(pl.col("status").str.len_bytes() == 0)
          .then(pl.lit("unknown"))
          .otherwise(pl.col("status"))
          .alias("status")
    )

    if "@ts" in df.columns and df["@ts"].dtype == pl.Utf8:
        try:
            df = df.with_columns(
                pl.col("@ts").str.to_datetime(strict=False)
            )
        except Exception:
            pass

    return df


def build_metrics(df: pl.DataFrame) -> dict:
    """
    DataFrame-based metrics, using the same RBA-specific accumulator.

    NOTE:
      - Not used in the main streaming path.
      - Handy for smaller subsets of the dataset.
    """
    df = enforce_schema_types(df)
    acc = MetricsAccumulator()
    for rec in df.to_dicts():
        acc.update(rec)
    return acc.finalize()


# --------------------------------------------------------------------
# Legal loading + LLM calls
# --------------------------------------------------------------------
def load_legal():
    docs = load_kb("/kb")
    text = "\n\n".join(
        [
            f"[{Path(d['id']).stem}]\n{d['body']}"
            for d in docs
            if "access" in d["title"].lower() or "article_21" in d["id"]
        ]
    )
    refs = [
        Path(d["id"]).stem
        for d in docs
        if "access" in d["title"].lower() or "article_21" in d["id"]
    ]
    return text, refs


def choose_chat():
    if config.API_MODE == "EXTERNAL":
        return ExternalChatClient(config.API_URL, config.API_KEY, config.API_MODEL)
    return OllamaChatClient(config.OLLAMA_BASE_URL, config.LLM_MODEL)


def generate_report(metrics: dict, period: str = "This Week", window_info: str = "") -> str:
    update_progress("legal", f"Loading legal compliance texts{window_info}...")
    legal_text, refs = load_legal()
    update_progress("legal", f"Loaded {len(refs)} relevant legal reference(s)")
    
    prompt = ANSWER_PROMPT.format(
        metrics_json=json.dumps(metrics, ensure_ascii=False),
        legal_text=legal_text,
    )
    
    update_progress("llm", f"Querying LLM for compliance analysis{window_info}...")
    client = choose_chat()
    prose = client.chat(config.SYSTEM_PROMPT, prompt)
    update_progress("llm", "LLM analysis complete")

    update_progress("render", f"Rendering compliance report{window_info}...")
    tpl_path = Path(__file__).parent / "templates" / "access_control_report.md.j2"
    tpl = Template(tpl_path.read_text(encoding="utf-8"))
    md = tpl.render(
        metrics=metrics,
        period=period,
        observations=prose,
        legal_refs=refs,
    )
    return md
