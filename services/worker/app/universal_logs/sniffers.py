import json
import csv
import re
from typing import List, Optional, Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..config_store import FormatConfigStore

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


def matches_custom_format(lines: List[str], config: dict) -> bool:
    """
    Check if log lines match a custom format's detection rules.
    
    Args:
        lines: Sample log lines
        config: Custom format configuration with detection_rules
        
    Returns:
        True if the lines match the format's detection rules
    """
    detection_rules = config.get("detection_rules", {})
    if not detection_rules:
        return False
    
    rule_type = detection_rules.get("type", "pattern")
    
    # Pattern-based detection (regex)
    if rule_type == "pattern":
        pattern = detection_rules.get("pattern", "")
        if pattern:
            try:
                regex = re.compile(pattern)
                # Check if any sample line matches
                matches = sum(1 for ln in lines[:20] if regex.search(ln))
                return matches >= len(lines[:20]) * 0.5  # At least 50% match
            except re.error:
                return False
    
    # Header-based detection (for CSV-like formats)
    elif rule_type == "header":
        required_fields = detection_rules.get("required_fields", [])
        if required_fields and lines:
            try:
                # Try to parse first line as CSV header
                header = next(csv.reader([lines[0]]))
                header_set = {h.strip().lower() for h in header}
                required_set = {f.strip().lower() for f in required_fields}
                return required_set.issubset(header_set)
            except Exception:
                return False
    
    # Structure-based detection (JSON with specific keys)
    elif rule_type == "structure":
        required_fields = detection_rules.get("required_fields", [])
        if required_fields and lines:
            try:
                # Try to parse first non-empty line as JSON
                for ln in lines[:10]:
                    ln = ln.strip()
                    if not ln:
                        continue
                    obj = json.loads(ln)
                    if isinstance(obj, dict):
                        obj_keys = set(obj.keys())
                        required_set = set(required_fields)
                        return required_set.issubset(obj_keys)
            except (json.JSONDecodeError, Exception):
                return False
    
    return False


def compute_format_similarity(lines: List[str], config: dict) -> float:
    """
    Compute a similarity score (0.0 to 1.0) between log lines and a custom format.
    
    Args:
        lines: Sample log lines
        config: Custom format configuration
        
    Returns:
        Similarity score from 0.0 (no match) to 1.0 (perfect match)
    """
    detection_rules = config.get("detection_rules", {})
    if not detection_rules:
        return 0.0
    
    rule_type = detection_rules.get("type", "pattern")
    
    # Pattern-based detection
    if rule_type == "pattern":
        pattern = detection_rules.get("pattern", "")
        if pattern:
            try:
                regex = re.compile(pattern)
                sample_lines = [ln for ln in lines[:20] if ln.strip()]
                if not sample_lines:
                    return 0.0
                matches = sum(1 for ln in sample_lines if regex.search(ln))
                return matches / len(sample_lines)
            except re.error:
                return 0.0
    
    # Header-based detection
    elif rule_type == "header":
        required_fields = detection_rules.get("required_fields", [])
        if required_fields and lines:
            try:
                header = next(csv.reader([lines[0]]))
                header_set = {h.strip().lower() for h in header}
                required_set = {f.strip().lower() for f in required_fields}
                if not required_set:
                    return 0.0
                matched = len(required_set.intersection(header_set))
                return matched / len(required_set)
            except Exception:
                return 0.0
    
    # Structure-based detection
    elif rule_type == "structure":
        required_fields = detection_rules.get("required_fields", [])
        if required_fields and lines:
            try:
                for ln in lines[:10]:
                    ln = ln.strip()
                    if not ln:
                        continue
                    obj = json.loads(ln)
                    if isinstance(obj, dict):
                        obj_keys = set(obj.keys())
                        required_set = set(required_fields)
                        if not required_set:
                            return 0.0
                        matched = len(required_set.intersection(obj_keys))
                        return matched / len(required_set)
            except (json.JSONDecodeError, Exception):
                return 0.0
    
    return 0.0


def find_best_matching_format(
    lines: List[str],
    config_store: Optional["FormatConfigStore"] = None,
    threshold: float = 0.5,
) -> Tuple[Optional[str], Optional[dict], float]:
    """
    Find the best matching custom format from Redis.
    
    Args:
        lines: Sample log lines
        config_store: Redis config store with custom formats
        threshold: Minimum similarity threshold to consider a match
        
    Returns:
        Tuple of (format_id, config, similarity_score)
        Returns (None, None, 0.0) if no match above threshold
    """
    if not config_store:
        return (None, None, 0.0)
    
    try:
        all_formats = config_store.get_all_formats()
        best_match = (None, None, 0.0)
        
        for format_id, config in all_formats.items():
            similarity = compute_format_similarity(lines, config)
            if similarity > best_match[2]:
                best_match = (format_id, config, similarity)
        
        if best_match[2] >= threshold:
            return best_match
        return (None, None, best_match[2])  # Return best score even if below threshold
    except Exception:
        return (None, None, 0.0)


def resolve_format_with_custom(
    lines: List[str],
    user_format: Optional[str] = None,
    config_store: Optional["FormatConfigStore"] = None,
) -> Tuple[str, Optional[dict]]:
    """
    Resolve format, checking custom configurations first.
    
    Args:
        lines: Sample log lines
        user_format: User-specified format override
        config_store: Optional Redis config store with custom formats
        
    Returns:
        Tuple of (format_name, custom_config or None)
        - If a custom format matches, returns (format_id, config_dict)
        - If built-in format matches, returns (format_name, None)
    """
    # User override always wins
    if user_format:
        uf = user_format.strip().lower()
        if uf in {"rba", "jsonl", "csv", "syslog", "unknown"}:
            return (uf, None)
    
    # Check custom formats from Redis - find best match
    if config_store:
        format_id, config, similarity = find_best_matching_format(lines, config_store, threshold=0.5)
        if format_id and config:
            return (format_id, config)
    
    # Fall back to built-in format detection
    fmt = sniff_format(lines)
    return (fmt, None)
