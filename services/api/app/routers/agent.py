"""
Agent API routes for the hybrid agentic compliance system.

These routes handle:
- Format analysis (schema inference)
- Format configuration approval
- Metric suggestions
- Format configuration management
"""

import os
from typing import List, Optional

import requests
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

router = APIRouter()
WORKER_URL = os.getenv("WORKER_URL", "http://worker:8081")


# -----------------------------------------------------------------------------
# Pydantic Models
# -----------------------------------------------------------------------------

class AnalyzeFormatRequest(BaseModel):
    """Request model for format analysis."""
    samples: List[str]
    max_samples: int = 20


class ApproveFormatRequest(BaseModel):
    """Request model for approving a format configuration."""
    format_id: str
    format_name: str
    format_type: str
    detection_rules: dict
    field_mappings: dict
    unmapped_fields: Optional[List[dict]] = []
    approved_by: str = "webui_user"


class MetricSuggestionRequest(BaseModel):
    """Request model for metric suggestions."""
    format_id: str
    available_fields: List[str]
    unmapped_fields: Optional[List[dict]] = []
    sample_stats: Optional[dict] = {}


class SaveMetricsRequest(BaseModel):
    """Request model for saving metric configuration."""
    format_id: str
    metrics: List[dict]


# -----------------------------------------------------------------------------
# Format Analysis Endpoints
# -----------------------------------------------------------------------------

@router.post("/analyze-format")
async def analyze_format(request: AnalyzeFormatRequest):
    """
    Analyze log samples and infer format schema.
    
    Sends samples to the worker's schema inference agent and returns
    proposed field mappings for human review.
    """
    try:
        resp = requests.post(
            f"{WORKER_URL}/agent/analyze-format",
            json={"samples": request.samples, "max_samples": request.max_samples},
            timeout=120,  # LLM calls can be slow
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.post("/quick-analyze")
async def quick_analyze(request: AnalyzeFormatRequest):
    """
    Quick heuristic-based format detection without LLM.
    
    Useful for initial format identification before engaging the full
    schema inference agent.
    """
    try:
        resp = requests.post(
            f"{WORKER_URL}/agent/quick-analyze",
            json={"samples": request.samples},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


# -----------------------------------------------------------------------------
# Format Configuration Endpoints
# -----------------------------------------------------------------------------

@router.post("/approve-format")
async def approve_format(request: ApproveFormatRequest):
    """
    Save an approved format configuration to Redis.
    
    This endpoint is called after a human has reviewed and approved
    the format schema suggested by the agent.
    """
    try:
        resp = requests.post(
            f"{WORKER_URL}/agent/approve-format",
            json=request.model_dump(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.get("/formats")
async def list_formats():
    """
    List all registered format configurations.
    
    Returns format IDs and basic metadata for all approved formats.
    """
    try:
        resp = requests.get(
            f"{WORKER_URL}/agent/formats",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.get("/formats/{format_id}")
async def get_format(format_id: str):
    """
    Get details of a specific format configuration.
    """
    try:
        resp = requests.get(
            f"{WORKER_URL}/agent/formats/{format_id}",
            timeout=10,
        )
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Format '{format_id}' not found")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.delete("/formats/{format_id}")
async def delete_format(format_id: str):
    """
    Delete a format configuration.
    """
    try:
        resp = requests.delete(
            f"{WORKER_URL}/agent/formats/{format_id}",
            timeout=10,
        )
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Format '{format_id}' not found")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


# -----------------------------------------------------------------------------
# Metric Suggestion Endpoints
# -----------------------------------------------------------------------------

@router.post("/suggest-metrics")
async def suggest_metrics(request: MetricSuggestionRequest):
    """
    Get metric suggestions for a format based on available fields.
    
    Returns a list of suggested metrics, both from defaults and LLM suggestions.
    """
    try:
        resp = requests.post(
            f"{WORKER_URL}/agent/suggest-metrics",
            json=request.model_dump(),
            timeout=120,  # LLM calls can be slow
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.post("/save-metrics")
async def save_metrics(request: SaveMetricsRequest):
    """
    Save approved metric configuration for a format.
    """
    try:
        resp = requests.post(
            f"{WORKER_URL}/agent/save-metrics",
            json=request.model_dump(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


@router.get("/metrics/{format_id}")
async def get_metrics(format_id: str):
    """
    Get saved metric configuration for a format.
    """
    try:
        resp = requests.get(
            f"{WORKER_URL}/agent/metrics/{format_id}",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")


# -----------------------------------------------------------------------------
# Health Check
# -----------------------------------------------------------------------------

@router.get("/health")
async def agent_health():
    """
    Check agent system health including Redis connectivity.
    """
    try:
        resp = requests.get(
            f"{WORKER_URL}/agent/health",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"status": "unhealthy", "error": str(e)}


@router.get("/scan-data-formats")
async def scan_data_formats():
    """
    Scan all data files and check their format status.
    Returns which files match onboarded formats and which don't.
    """
    try:
        resp = requests.get(
            f"{WORKER_URL}/agent/scan-data-formats",
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Worker error: {str(e)}")
