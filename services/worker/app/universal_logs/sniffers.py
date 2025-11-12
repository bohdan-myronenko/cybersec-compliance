import json, csv, re

JSONL_THRESHOLD = 0.8
SYSLOG_RE = re.compile(r"^\w{3}\s+\d{1,2}\s+\d\d:\d\d:\d\d\s")

def looks_like_jsonl(lines):
    ok = 0; total = min(len(lines), 50)
    for ln in lines[:total]:
        try:
            json.loads(ln)
            ok += 1
        except Exception:
            pass
    return total>0 and ok/total >= JSONL_THRESHOLD

def looks_like_csv(lines):
    try:
        sample = "\n".join(lines[:50])
        dialect = csv.Sniffer().sniff(sample)
        rd = csv.reader(sample.splitlines(), dialect)
        widths = [len(r) for r in rd if r]
        return len(widths)>5 and len(set(widths))<=3
    except Exception:
        return False

def looks_like_syslog(lines):
    return any(SYSLOG_RE.match(ln or "") for ln in lines[:50])

def sniff_format(lines):
    if looks_like_jsonl(lines): return "jsonl"
    if looks_like_csv(lines): return "csv"
    if looks_like_syslog(lines): return "syslog"
    return "unknown"