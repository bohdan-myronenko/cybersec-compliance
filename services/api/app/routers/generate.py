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