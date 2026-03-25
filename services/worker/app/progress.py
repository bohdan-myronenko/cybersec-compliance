"""
Progress tracking for report generation pipeline.
"""

import json
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Thread-safe progress storage
_lock = threading.Lock()
_current_progress: Optional["ProgressState"] = None


@dataclass
class ProgressState:
    """Current state of report generation progress."""
    stage: str
    stage_number: int
    total_stages: int
    message: str
    detail: str = ""
    started_at: str = ""
    updated_at: str = ""
    is_complete: bool = False
    is_error: bool = False
    stages_status: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return asdict(self)


# Define pipeline stages
STAGES = [
    ("init", "Initializing report generation"),
    ("scan", "Scanning data directory for log files"),
    ("normalize", "Normalizing and parsing log records"),
    ("metrics", "Computing security metrics per time window"),
    ("legal", "Loading legal compliance texts from knowledge base"),
    ("llm", "Querying LLM for compliance analysis"),
    ("insights", "Generating AI insights"),
    ("render", "Rendering compliance report from template"),
    ("save", "Saving report to output directory"),
    ("complete", "Report generation complete"),
]


def get_stage_info(stage_key: str) -> tuple[int, str]:
    """Get stage number and message for a stage key."""
    for i, (key, msg) in enumerate(STAGES):
        if key == stage_key:
            return i + 1, msg
    return 0, "Unknown stage"


def _build_stages_status(
    current_stage_num: int,
    is_error: bool = False,
    is_complete: bool = False,
    prev_status: dict | None = None,
) -> dict:
    """Build a dict of {stage_key: status_string} for every stage."""
    status = dict(prev_status) if prev_status else {}
    for i, (key, _msg) in enumerate(STAGES):
        num = i + 1
        if num < current_stage_num:
            # Only mark Done if not already Error
            if status.get(key) != "Error!":
                status[key] = "Done"
        elif num == current_stage_num:
            if is_error:
                status[key] = "Error!"
            elif is_complete:
                status[key] = "Done"
            else:
                status[key] = "Processing..."
        else:
            if key not in status:
                status[key] = "Pending"
    return status


def update_progress(
    stage: str,
    detail: str = "",
    is_complete: bool = False,
    is_error: bool = False,
):
    """Update the current progress state."""
    global _current_progress
    
    stage_num, message = get_stage_info(stage)
    now = datetime.utcnow().isoformat() + "Z"
    
    with _lock:
        started = _current_progress.started_at if _current_progress else now
        prev_status = _current_progress.stages_status if _current_progress else None
        stages_status = _build_stages_status(stage_num, is_error, is_complete, prev_status)
        _current_progress = ProgressState(
            stage=stage,
            stage_number=stage_num,
            total_stages=len(STAGES),
            message=message,
            detail=detail,
            started_at=started,
            updated_at=now,
            is_complete=is_complete,
            is_error=is_error,
            stages_status=stages_status,
        )


def get_progress() -> Optional[ProgressState]:
    """Get the current progress state."""
    with _lock:
        return _current_progress


def reset_progress():
    """Reset progress state for a new run."""
    global _current_progress
    with _lock:
        _current_progress = None


def clear_progress():
    """Clear progress state after completion."""
    global _current_progress
    with _lock:
        _current_progress = None
