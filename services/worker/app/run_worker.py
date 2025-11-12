import os
from pathlib import Path
from fastapi import FastAPI
import uvicorn
import polars as pl
import traceback

from .pipeline import normalize_file, build_metrics, generate_report

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
        # Combine all files in DATA_DIR into one DataFrame
        frames = []
        for p in DATA_DIR.rglob("*"):
            if p.is_file():
                try:
                    frames.append(normalize_file(p))
                except Exception:
                    # non-parsable file -> skip
                    continue

        if not frames:
            return {"error": f"No parsable files in {DATA_DIR.resolve()}"}

        df = pl.concat(frames, how="vertical_relaxed")

        metrics = build_metrics(df)
        report_md = generate_report(metrics, period="This Week")

        outpath = OUT_DIR / "access_control_report.md"
        outpath.write_text(report_md, encoding="utf-8")
        return {"ok": True, "output": str(outpath)}

    except Exception:
        tb = traceback.format_exc()
        print(tb, flush=True)
        return {"error": "worker_exception", "traceback": tb}


if __name__ == "__main__":
    uvicorn.run("app.run_worker:app", host="0.0.0.0", port=8081, reload=False)
