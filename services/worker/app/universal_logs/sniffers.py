import json
import csv
import re
from typing import List, Optional

JSONL_THRESHOLD = 0.8
SYSLOG_RE = re.compile(r"^\w{3}\s+\d{1,2}\s+\d\d:\d\d:\d\d\s")


def looks_like_jsonl(lines: List[str]) -> bool:
    ok = 0
    total = min(len(lines), 50)
    for ln in lines[:total]:
        try:
            json.loads(ln)
            ok += 1
        except Exception:
            pass
    return total > 0 and ok / total >= JSONL_THRESHOLD


def looks_like_csv(lines: List[str]) -> bool:
    try:
        sample = "\n".join(lines[:50])
        dialect = csv.Sniffer().sniff(sample)
        rd = csv.reader(sample.splitlines(), dialect)
        widths = [len(r) for r in rd if r]
        return len(widths) > 5 and len(set(widths)) <= 3
    except Exception:
        return False


RBA_KEY_COLUMNS = {
    "IP Address",
    "Country",
    "Region",
    "City",
    "ASN",
    "User Agent String",
    "OS Name and Version",
    "Browser Name and Version",
    "Device Type",
    "User ID",
    "Login Timestamp",
    "Login Successful",
    "Is Attack IP",
    "Is Account Takeover",
}


def looks_like_rba(lines: List[str]) -> bool:
    if not lines:
        return False
    try:
        header = next(csv.reader([lines[0]]))
        header_set = {h.strip() for h in header}
        return RBA_KEY_COLUMNS.issubset(header_set)
    except Exception:
        return False


def looks_like_syslog(lines: List[str]) -> bool:
    return any(SYSLOG_RE.match(ln or "") for ln in lines[:50])


def sniff_format(lines):
    if looks_like_rba(lines):
        return "rba"
    if looks_like_jsonl(lines):
        return "jsonl"
    if looks_like_csv(lines):
        return "csv"
    if looks_like_syslog(lines):
        return "syslog"
    return "unknown"


def resolve_format(lines: List[str], user_format: Optional[str] = None) -> str:
    """
    Resolve the effective format, allowing a user override.

    - If user_format is one of {"rba","jsonl","csv","syslog","unknown"}, it wins.
    - Otherwise, fall back to sniff_format(lines).
    """
    if user_format:
        uf = user_format.strip().lower()
        if uf in {"rba", "jsonl", "csv", "syslog", "unknown"}:
            return uf
    return sniff_format(lines)
