import os
from pathlib import Path

from fastapi import FastAPI
import uvicorn
import traceback

from .pipeline import build_windowed_metrics_for_dir, generate_report
from .progress import update_progress, get_progress, reset_progress

app = FastAPI(title="Compliance Worker", version="0.1.0")

DATA_DIR = Path(os.getenv("DEFAULT_DATA_DIR", "/data"))
OUT_DIR = Path(os.getenv("OUT_DIR", "/out"))
OUT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/progress")
def get_current_progress():
    """Get the current progress of report generation."""
    progress = get_progress()
    if progress is None:
        return {"status": "idle", "message": "No report generation in progress"}
    return {"status": "running", "progress": progress.to_dict()}


@app.post("/run/access-control")
def run_access_control():
    try:
        # Reset and start progress tracking
        reset_progress()
        update_progress("init", "Starting access control report generation...")
        
        window_days = int(os.getenv("WINDOW_DAYS", "7"))

        # Stream over all files, aggregate per time window
        metrics_by_window = build_windowed_metrics_for_dir(DATA_DIR, window_days=window_days)

        if not metrics_by_window:
            update_progress("complete", f"No parsable files in {DATA_DIR.resolve()}", is_complete=True, is_error=True)
            return {"error": f"No parsable files in {DATA_DIR.resolve()}"}

        outputs = []
        total_windows = len(metrics_by_window)
        
        for i, (window_key, metrics) in enumerate(metrics_by_window.items(), 1):
            window_info = f" (window {i}/{total_windows})" if total_windows > 1 else ""
            
            # window_key is ISO start-of-window or "unknown"
            period_label = (
                f"{window_key} (window={window_days}d)" if window_key != "unknown"
                else "Unknown period"
            )

            report_md = generate_report(metrics, period=period_label, window_info=window_info)

            # Make filename safe for filesystem
            update_progress("save", f"Saving report for window: {window_key}")
            filename_safe = window_key.replace(":", "-") if window_key != "unknown" else "unknown"
            outpath = OUT_DIR / f"access_control_report_{filename_safe}.md"
            outpath.write_text(report_md, encoding="utf-8")

            outputs.append({"window": window_key, "output": str(outpath)})

        update_progress("complete", f"Successfully generated {len(outputs)} report(s)", is_complete=True)
        return {"ok": True, "windows": outputs}

    except Exception:
        tb = traceback.format_exc()
        print(tb, flush=True)
        update_progress("complete", f"Error: {tb[:200]}", is_complete=True, is_error=True)
        return {"error": "worker_exception", "traceback": tb}


if __name__ == "__main__":
    uvicorn.run("app.run_worker:app", host="0.0.0.0", port=8081, reload=False)