import os, json
from pathlib import Path
import polars as pl
from jinja2 import Template
from .universal_logs.sniffers import sniff_format
from .universal_logs.normalizers import normalize_line
from .universal_logs.aggregations import rollups
from .kb_loader.loader import load_kb
from .llm_clients.ollama_chat import OllamaChatClient
from .llm_clients.external_chat import ExternalChatClient
from . import config

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

ECS_COLS = ["@ts","user","src_ip","dst_ip","action","status","resource","msg","raw"]


def read_lines(path: Path, limit=None):
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        if limit:
            return [next(f, "") for _ in range(limit)]
        return f.readlines()


def normalize_file(path: Path) -> pl.DataFrame:
    lines = read_lines(path)
    fmt = sniff_format(lines)
    recs = [normalize_line(ln, fmt) for ln in lines if ln.strip()]
    return pl.DataFrame(recs)


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
    """Build minimal demo metrics for access-control reporting."""
    # enforce safe types to avoid Null-series errors
    df = enforce_schema_types(df)

    total_rows = df.height

    # Authentication failures
    failures_df = df.filter(pl.col("status") == "fail")
    failures_total = failures_df.height

    # Top IPs by event count (very simple example)
    top_ips = (
        df.filter(pl.col("src_ip") != "")
          .group_by("src_ip")
          .len()
          .sort("len", descending=True)
          .limit(5)
          .rename({"len": "count"})
          .to_dicts()
    )

    metrics = {
        "mfa": {
            "total_users": 120,
            "enabled_users": 118,
            "coverage_pct": round(118 / 120 * 100, 2),
        },
        "auth_failures": {
            "total": int(failures_total),
            "top_ips": [{"ip": d["src_ip"], "count": int(d["count"])} for d in top_ips],
        },
        "admins": {
            "count": 8,
            "with_mfa": 8,
            "last_review_date": "2025-10-31",
        },
        "exceptions": [],
        "frame": {"rows": int(total_rows)},
    }
    return metrics


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


def generate_report(metrics: dict, period="This Week"):
    legal_text, refs = load_legal()
    prompt = ANSWER_PROMPT.format(
        metrics_json=json.dumps(metrics, ensure_ascii=False),
        legal_text=legal_text,
    )
    client = choose_chat()
    prose = client.chat(config.SYSTEM_PROMPT, prompt)

    # Render to template
    tpl_path = Path(__file__).parent / "templates" / "access_control_report.md.j2"
    tpl = Template(tpl_path.read_text(encoding="utf-8"))
    md = tpl.render(
        metrics=metrics, period=period, observations=prose, legal_refs=refs
    )
    return md
