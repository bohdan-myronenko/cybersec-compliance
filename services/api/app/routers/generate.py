import os, requests
from fastapi import APIRouter, Body

router = APIRouter()
WORKER_URL = os.getenv("WORKER_URL", "http://worker:8081")

@router.post("/access-control")
def generate_access_control(payload: dict = Body(default={})):
    r = requests.post(f"{WORKER_URL}/run/access-control", json=payload, timeout=3600)
    try:
        return r.json()
    except Exception as e:
        return {"error": "api_parse_error", "detail": str(e), "raw": r.text}


@router.get("/progress")
def get_generation_progress():
    """Get the current progress of report generation from the worker."""
    try:
        r = requests.get(f"{WORKER_URL}/progress", timeout=5)
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}