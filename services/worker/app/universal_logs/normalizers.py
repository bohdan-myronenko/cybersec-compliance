import json
import csv
import re
import datetime

from .ecs_schema import ECS_MIN

IP_RE = re.compile(r"\b(?:(?:\d{1,3}\.){3}\d{1,3})\b")
USER_RE = re.compile(r"user(?:name)?=(\w+)|\b(uid|user)\b[:= ](\w+)")

def parse_time_any(s: str):
    """
    Try parsing a timestamp string using a few common formats.
    We return a datetime, or None if nothing matches.

    NOTE:
    - Normalisation keeps @ts as the raw string; the caller can decide
      whether to store the parsed datetime, its ISO string, or leave as-is.
    """
    if not s:
        return None
    s = str(s).strip()

    try:
        return datetime.datetime.fromisoformat(s)
    except Exception:
        pass

    # try a few common patterns
    fmts = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%b %d %H:%M:%S",
    ]
    for fmt in fmts:
        try:
            return datetime.datetime.strptime(s, fmt)
        except Exception:
            continue
    return None


def kv_pairs(line: str):
    pairs = {}
    for part in re.findall(r"(\w+)=([^\s]+)", line):
        k, v = part
        pairs[k] = v
    return pairs


def extract_first(regex, text):
    m = regex.search(text or "")
    if not m:
        return None
    for g in m.groups():
        if g:
            return g
    return None


def to_ecs_min(rec: dict, raw: str):
    """
    Map an intermediate record dict to the minimal ECS-like schema.
    All keys not in ECS_MIN are dropped; raw is kept (truncated).
    """
    return {
        "@ts": rec.get("@ts"),
        "user": rec.get("user"),
        "src_ip": rec.get("src_ip"),
        "dst_ip": rec.get("dst_ip"),
        "action": rec.get("action"),
        "status": rec.get("status"),
        "resource": rec.get("resource"),
        "msg": rec.get("msg"),
        "raw": raw[:2048],
    }


def normalize_rba_row(row: dict):
    """
    Convert a single RBA dataset CSV row into ECS_MIN format.
    RBA schema reference: rba-dataset-metadata.json

    Expected logical keys in 'row':
      - "Login Timestamp"
      - "User ID"
      - "IP Address"
      - "Device Type"
      - "OS Name and Version"
      - "Browser Name and Version"
      - "Login Successful"
      - "Is Attack IP"
      - "Is Account Takeover"
    """
    # Timestamp: handle either integer epoch or human-readable string
    ts = None
    ts_raw = row.get("Login Timestamp")
    if ts_raw:
        ts_str = str(ts_raw).strip()
        # Try epoch seconds (original Kaggle spec)
        if ts_str.isdigit():
            try:
                ts = datetime.datetime.utcfromtimestamp(int(ts_str)).isoformat()
            except Exception:
                ts = None
        # Try parsing as datetime string (actual, Kaggle description is wrong)
        if ts is None:
            dt = parse_time_any(ts_str)
            if dt is not None:
                ts = dt.isoformat()
            else:
                # Last resort: keep raw string
                ts = ts_str

    # Convert login success to ECS status
    success_raw = row.get("Login Successful")
    success_str = str(success_raw).strip().lower()
    if success_str == "true":
        status = "success"
    elif success_str == "false":
        status = "fail"
    else:
        status = "unknown"

    user = str(row.get("User ID") or "").strip()
    src_ip = (row.get("IP Address") or "").strip()

    # Build a descriptive message
    msg_parts = [
        str(row.get("Device Type", "") or "").strip(),
        str(row.get("OS Name and Version", "") or "").strip(),
        str(row.get("Browser Name and Version", "") or "").strip(),
    ]
    msg = ", ".join(p for p in msg_parts if p)

    return {
        "@ts": ts,
        "user": user if user else None,
        "src_ip": src_ip if src_ip else None,
        "dst_ip": None,
        "action": "login",
        "status": status,
        "resource": None,
        "msg": msg or None,
        "raw": json.dumps(row)[:2048],
    }


def normalize_line(line: str, fmt: str):
    """
    Normalise a single log line into the ECS_MIN schema.

    Parameters
    ----------
    line : str
        Raw log line (one row / entry).
    fmt : str
        Detected or user-specified format: "jsonl", "csv", "rba", "syslog", or "unknown".

    Notes
    -----
    - 'fmt' can be determined automatically (resolve_format/sniff_format) or
      supplied by the user (LOG_FORMAT).
    - We keep @ts as a raw/ISO string here; the caller can later parse via
      parse_time_any or leave it as string for DB storage.
    """

    # JSON Lines: one JSON object per line
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

    # RBA dataset (Login Data Set for Risk-Based Authentication)
    if fmt == "rba":
        # Use csv.reader to handle commas in user agent etc.
        try:
            cols = next(csv.reader([line]))
        except Exception:
            cols = [p.strip() for p in line.split(",")]

        # Header line → skip as data, but keep raw
        if cols and cols[0].strip().lower() == "index":
            return to_ecs_min({"msg": line.strip()}, line)

        # Map by known column order from the RBA dataset:
        # 0: index
        # 1: Login Timestamp
        # 2: User ID
        # 3: Round-Trip Time [ms]
        # 4: IP Address
        # 5: Country
        # 6: Region
        # 7: City
        # 8: ASN
        # 9: User Agent String
        # 10: Browser Name and Version
        # 11: OS Name and Version
        # 12: Device Type
        # 13: Login Successful
        # 14: Is Attack IP
        # 15: Is Account Takeover
        def safe(idx):
            return cols[idx] if len(cols) > idx else ""

        row = {
            "Login Timestamp": safe(1),
            "User ID": safe(2),
            "Round-Trip Time [ms]": safe(3),
            "IP Address": safe(4),
            "Country": safe(5),
            "Region": safe(6),
            "City": safe(7),
            "ASN": safe(8),
            "User Agent String": safe(9),
            "Browser Name and Version": safe(10),
            "OS Name and Version": safe(11),
            "Device Type": safe(12),
            "Login Successful": safe(13),
            "Is Attack IP": safe(14),
            "Is Account Takeover": safe(15),
        }
        return to_ecs_min(normalize_rba_row(row), line)

    # CSV logs (generic)
    if fmt == "csv":
        # Simple heuristic: split by comma. This is intentionally generic and
        # does not assume a specific header
        try:
            # Use csv.reader for basic quoting support
            row = next(csv.reader([line]))
        except Exception:
            row = [p.strip() for p in line.split(",")]

        parts = [p.strip() for p in row]

        # Basic assumptions: first col is some kind of timestamp / index
        ts = parts[0] if parts else None
        user = parts[1] if len(parts) > 1 else None
        status = parts[2] if len(parts) > 2 else None

        rec = {
            "@ts": ts,
            "user": user,
            "src_ip": extract_first(IP_RE, line),
            "dst_ip": None,
            "action": None,
            "status": status,
            "resource": None,
            "msg": line.strip(),
        }
        return to_ecs_min(rec, line)

    # Syslog-like lines (e.g. auth.log)
    if fmt == "syslog":
        # Best-effort: first 15 chars as timestamp (e.g. "Jan  2 03:04:05")
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