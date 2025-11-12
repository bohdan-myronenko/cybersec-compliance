import os
import requests
from fastapi import APIRouter, Body

router = APIRouter()

WORKER_URL = os.getenv("WORKER_URL", "http://compliance_worker:8081")  # internal-only example

@router.post("/access-control")
def generate_access_control(payload: dict = Body(default={})):
    r = requests.post(f"{WORKER_URL}/run/access-control", json=payload, timeout=300)
    try:
        return r.json()
    except Exception as e:
        return {"error": "api_parse_error", "detail": str(e), "raw": r.text}