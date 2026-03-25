"""
Checkpoint persistence for the report generation pipeline.

Saves intermediate results as a JSON file so that failed runs can
resume from the last successful stage instead of recomputing everything.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


CHECKPOINT_DIR = Path(os.getenv("OUT_DIR", "/out"))
CHECKPOINT_FILENAME = ".pipeline_checkpoint.json"


def _checkpoint_path() -> Path:
    return CHECKPOINT_DIR / CHECKPOINT_FILENAME


def save_checkpoint(
    completed_stages: List[str],
    stage_data: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Persist checkpoint to disk.

    Args:
        completed_stages: List of stage keys that finished successfully.
        stage_data: Dict of intermediate results keyed by stage name,
                    e.g. {"metrics_by_window": {...}, "reports": [...]}.
        params: Pipeline parameters (e.g. target_filename, window_days)
                used to verify the checkpoint matches the current run.
    """
    payload = {
        "completed_stages": completed_stages,
        "stage_data": stage_data,
        "params": params or {},
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = _checkpoint_path().with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8")
    tmp.replace(_checkpoint_path())


def load_checkpoint() -> Optional[Dict[str, Any]]:
    """Load checkpoint from disk, or return None if missing/corrupt."""
    p = _checkpoint_path()
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if "completed_stages" not in data or "stage_data" not in data:
            return None
        return data
    except (json.JSONDecodeError, OSError):
        return None


def clear_checkpoint() -> bool:
    """Delete checkpoint file. Returns True if a file was removed."""
    p = _checkpoint_path()
    if p.exists():
        p.unlink()
        return True
    return False


def get_checkpoint_info() -> Optional[Dict[str, Any]]:
    """Return a lightweight summary of the checkpoint (no bulky data)."""
    ckpt = load_checkpoint()
    if ckpt is None:
        return None
    return {
        "completed_stages": ckpt["completed_stages"],
        "last_stage": ckpt["completed_stages"][-1] if ckpt["completed_stages"] else None,
        "params": ckpt.get("params", {}),
        "updated_at": ckpt.get("updated_at"),
    }
