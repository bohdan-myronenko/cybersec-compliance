"""
Evaluation logging for LLM comparison research.

Captures structured data about each LLM call during report generation,
enabling automated comparison of Ollama vs External LLM providers.
Writes structured JSONL logs for analysis in the evaluation notebook.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

EVAL_LOG_DIR = os.getenv("EVAL_LOG_DIR", "/out/eval_logs")

# --------------------------------------------------------------------------
# Schema constants
# --------------------------------------------------------------------------
REQUIRED_TOP_KEYS = ["summary", "risk_level", "findings", "positive_observations", "trend_analysis"]
FINDING_KEYS = ["id", "severity", "category", "title", "description", "evidence",
                "compliance_impact", "recommendation", "priority"]
EVIDENCE_KEYS = ["metric", "current_value", "baseline_value", "deviation"]
VALID_SEVERITIES = {"critical", "high", "medium", "low", "info"}
VALID_RISK_LEVELS = {"low", "medium", "high", "critical"}


def create_eval_entry(
    provider: str,
    model: str,
    period: str,
    metrics_input: Dict[str, Any],
    framework: str = "NIS2",
) -> Dict[str, Any]:
    """Create a new evaluation log entry."""
    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "model": model,
        "period": period,
        "framework": framework,
        "metrics_input": metrics_input,
        "compliance_call": None,
        "insight_call": None,
        "report_length_chars": None,
        "total_pipeline_seconds": None,
    }


def record_llm_call(
    prompt: str,
    response: str,
    latency_seconds: float,
    success: bool = True,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """Record data about a single LLM call."""
    return {
        "latency_seconds": round(latency_seconds, 3),
        "prompt_length_chars": len(prompt),
        "response_length_chars": len(response) if response else 0,
        "estimated_prompt_tokens": len(prompt) // 4,
        "estimated_response_tokens": len(response) // 4 if response else 0,
        "raw_response": response,
        "success": success,
        "error": error,
    }


def validate_insight_schema(insights: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parsed insights against expected schema.
    Returns detailed conformance data for automated metric computation.
    """
    result: Dict[str, Any] = {
        "top_level_keys_present": {},
        "top_level_conformance": 0.0,
        "risk_level_valid": False,
        "findings_count": 0,
        "findings_field_completeness": [],
        "severity_validity": [],
        "evidence_completeness": [],
        "overall_conformance": 0.0,
    }

    # Top-level keys
    present = 0
    for key in REQUIRED_TOP_KEYS:
        is_present = key in insights
        result["top_level_keys_present"][key] = is_present
        if is_present:
            present += 1
    result["top_level_conformance"] = round(present / len(REQUIRED_TOP_KEYS), 3)

    # Risk level validity
    risk = insights.get("risk_level", "")
    result["risk_level_valid"] = str(risk).lower().strip() in VALID_RISK_LEVELS

    # Findings analysis
    findings = insights.get("findings", [])
    result["findings_count"] = len(findings)

    for i, finding in enumerate(findings):
        if not isinstance(finding, dict):
            result["findings_field_completeness"].append(
                {"finding_index": i, "completeness": 0.0, "missing": FINDING_KEYS}
            )
            continue

        missing = [k for k in FINDING_KEYS if k not in finding or finding[k] is None]
        completeness = (len(FINDING_KEYS) - len(missing)) / len(FINDING_KEYS)
        result["findings_field_completeness"].append({
            "finding_index": i,
            "completeness": round(completeness, 3),
            "missing": missing,
        })

        # Severity validity
        sev = str(finding.get("severity", "")).lower().strip()
        result["severity_validity"].append({
            "finding_index": i,
            "severity": sev,
            "valid": sev in VALID_SEVERITIES,
        })

        # Evidence completeness
        evidence = finding.get("evidence", {})
        if isinstance(evidence, dict):
            ev_present = [k for k in EVIDENCE_KEYS if k in evidence]
            result["evidence_completeness"].append({
                "finding_index": i,
                "completeness": round(len(ev_present) / len(EVIDENCE_KEYS), 3),
                "present_keys": ev_present,
            })

    # Overall conformance score
    scores = [result["top_level_conformance"]]
    scores.append(1.0 if result["risk_level_valid"] else 0.0)
    if result["findings_field_completeness"]:
        avg_completeness = sum(
            f["completeness"] for f in result["findings_field_completeness"]
        ) / len(result["findings_field_completeness"])
        scores.append(avg_completeness)
    result["overall_conformance"] = round(sum(scores) / len(scores), 3)

    return result


def save_eval_log(entry: Dict[str, Any]) -> None:
    """Append an evaluation log entry to the JSONL file."""
    log_dir = Path(EVAL_LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "eval_log.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str, ensure_ascii=False) + "\n")
