import os
from pathlib import Path

from fastapi import FastAPI
import uvicorn
import traceback

from .pipeline import build_windowed_metrics_for_dir, generate_report

app = FastAPI(title="Compliance Worker", version="0.1.0")

DATA_DIR = Path(os.getenv("DEFAULT_DATA_DIR", "/data"))
OUT_DIR = Path(os.getenv("OUT_DIR", "/out"))
OUT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run/access-control")
def run_access_control():
    try:
        window_days = int(os.getenv("WINDOW_DAYS", "7"))

        # Stream over all files, aggregate per time window
        metrics_by_window = build_windowed_metrics_for_dir(DATA_DIR, window_days=window_days)

        if not metrics_by_window:
            return {"error": f"No parsable files in {DATA_DIR.resolve()}"}

        outputs = []
        for window_key, metrics in metrics_by_window.items():
            # window_key is ISO start-of-window or "unknown"
            period_label = (
                f"{window_key} (window={window_days}d)" if window_key != "unknown"
                else "Unknown period"
            )

            report_md = generate_report(metrics, period=period_label)

            # Make filename safe for filesystem
            filename_safe = window_key.replace(":", "-") if window_key != "unknown" else "unknown"
            outpath = OUT_DIR / f"access_control_report_{filename_safe}.md"
            outpath.write_text(report_md, encoding="utf-8")

            outputs.append({"window": window_key, "output": str(outpath)})

        return {"ok": True, "windows": outputs}

    except Exception:
        tb = traceback.format_exc()
        print(tb, flush=True)
        return {"error": "worker_exception", "traceback": tb}


if __name__ == "__main__":
    uvicorn.run("app.run_worker:app", host="0.0.0.0", port=8081, reload=False)