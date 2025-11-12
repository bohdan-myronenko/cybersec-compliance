import json, csv, re, datetime
from .ecs_schema import ECS_MIN

IP_RE = re.compile(r"\b(?:(?:\d{1,3}\.){3}\d{1,3})\b")
USER_RE = re.compile(r"user(?:name)?=(\w+)|\b(uid|user)\b[:= ](\w+)")

def parse_time_any(s: str):
    # try a few formats
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%b %d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(s, fmt)
        except Exception:
            pass
    return None

def kv_pairs(line: str):
    pairs = {}
    for part in re.findall(r"(\w+)=([^\s]+)", line):
        k, v = part
        pairs[k] = v
    return pairs

def extract_first(regex, text):
    m = regex.search(text or "")
    if not m: return None
    for g in m.groups():
        if g: return g
    return None

def to_ecs_min(rec: dict, raw: str):
    return {
        "@ts": rec.get("@ts"),
        "user": rec.get("user"),
        "src_ip": rec.get("src_ip"),
        "dst_ip": rec.get("dst_ip"),
        "action": rec.get("action"),
        "status": rec.get("status"),
        "resource": rec.get("resource"),
        "msg": rec.get("msg"),
        "raw": raw[:2048]
    }

def normalize_line(line: str, fmt: str):
    if fmt == "jsonl":
        try:
            obj = json.loads(line)
        except Exception:
            obj = {}
        rec = {
            "@ts": obj.get("ts") or obj.get("@timestamp"),
            "user": obj.get("user") or obj.get("username"),
            "src_ip": obj.get("src_ip") or obj.get("src") or extract_first(IP_RE, line),
            "dst_ip": obj.get("dst_ip") or obj.get("dst"),
            "action": obj.get("action") or obj.get("event") or obj.get("verb"),
            "status": obj.get("status") or obj.get("result"),
            "resource": obj.get("resource") or obj.get("path") or obj.get("service"),
            "msg": obj.get("message") or obj.get("msg"),
        }
        return to_ecs_min(rec, line)

    if fmt == "csv":
        # Simple heuristic: split by comma, infer columns
        parts = [p.strip() for p in line.split(",")]
        rec = {
            "@ts": parts[0] if parts else None,
            "user": None,
            "src_ip": extract_first(IP_RE, line),
            "dst_ip": None,
            "action": None,
            "status": None,
            "resource": None,
            "msg": line.strip(),
        }
        return to_ecs_min(rec, line)

    if fmt == "syslog":
        # best-effort: ts + msg
        ts = line[:15]
        msg = line[16:]
        rec = {
            "@ts": ts,
            "user": extract_first(USER_RE, line),
            "src_ip": extract_first(IP_RE, line),
            "dst_ip": None,
            "action": None,
            "status": None,
            "resource": None,
            "msg": msg.strip(),
        }
        return to_ecs_min(rec, line)

    # unknown → heuristic key=value, ip, etc.
    kv = kv_pairs(line)
    rec = {
        "@ts": kv.get("ts") or kv.get("@ts"),
        "user": kv.get("user") or extract_first(USER_RE, line),
        "src_ip": kv.get("src_ip") or extract_first(IP_RE, line),
        "dst_ip": kv.get("dst_ip"),
        "action": kv.get("action") or kv.get("verb") or None,
        "status": kv.get("status") or kv.get("result"),
        "resource": kv.get("resource") or kv.get("path"),
        "msg": kv.get("message") or kv.get("msg") or line.strip(),
    }
    return to_ecs_min(rec, line)