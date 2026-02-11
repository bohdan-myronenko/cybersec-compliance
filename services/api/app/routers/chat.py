"""
Chat and upload API routes. Forwards to worker for chat, RAG index, uploads, and onboard.
"""

import os
from typing import List, Optional

import requests
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter()
WORKER_URL = os.getenv("WORKER_URL", "http://worker:8081")


def _get_worker_response_error(e: Exception):
    resp = getattr(e, "response", None)
    if resp is not None:
        return resp.status_code, (resp.text or str(e))[:500]
    return 502, str(e)


# -----------------------------------------------------------------------------
# Request models
# -----------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None
    include_context: bool = True


class OnboardAnalyzeRequest(BaseModel):
    samples: List[str]
    max_samples: int = 20


class OnboardConfirmRequest(BaseModel):
    format_id: str
    format_name: str
    format_type: str
    detection_rules: dict
    field_mappings: dict
    unmapped_fields: Optional[List[dict]] = None
    approved_by: str = "webui_user"


# -----------------------------------------------------------------------------
# Chat endpoints
# -----------------------------------------------------------------------------

@router.post("")
async def chat(request: ChatRequest):
    """Chat with RAG context from KB and reports."""
    try:
        resp = requests.post(
            f"{WORKER_URL}/chat",
            json=request.model_dump(),
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.post("/index")
async def chat_index():
    """Trigger re-indexing of KB and reports."""
    try:
        resp = requests.post(
            f"{WORKER_URL}/chat/index",
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.get("/index/status")
async def chat_index_status():
    """Get RAG index status."""
    try:
        resp = requests.get(
            f"{WORKER_URL}/chat/index/status",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


# -----------------------------------------------------------------------------
# Upload endpoints (mounted at prefix /upload)
# -----------------------------------------------------------------------------

upload_router = APIRouter()


def _forward_upload(url: str, file: UploadFile):
    content = file.file.read()
    files = {"file": (file.filename or "upload", content)}
    return requests.post(url, files=files, timeout=60)


@upload_router.post("/logs")
async def upload_logs(file: UploadFile = File(...)):
    """Upload log file to worker; returns format detection and onboarding hint."""
    try:
        resp = _forward_upload(f"{WORKER_URL}/upload/logs", file)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        code, detail = _get_worker_response_error(e)
        raise HTTPException(status_code=code, detail=detail)


@upload_router.post("/kb")
async def upload_kb(file: UploadFile = File(...)):
    """Upload KB document to worker and trigger RAG re-index."""
    try:
        resp = _forward_upload(f"{WORKER_URL}/upload/kb", file)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        code, detail = _get_worker_response_error(e)
        raise HTTPException(status_code=code, detail=detail)


# -----------------------------------------------------------------------------
# Onboard endpoints (mounted at prefix /onboard)
# -----------------------------------------------------------------------------

onboard_router = APIRouter()


@onboard_router.post("/analyze")
async def onboard_analyze(request: OnboardAnalyzeRequest):
    """Analyze log format and return proposed mappings for review."""
    try:
        resp = requests.post(
            f"{WORKER_URL}/onboard/analyze",
            json=request.model_dump(),
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@onboard_router.post("/confirm")
async def onboard_confirm(request: OnboardConfirmRequest):
    """Confirm and save approved format configuration."""
    try:
        resp = requests.post(
            f"{WORKER_URL}/onboard/confirm",
            json=request.model_dump(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")
