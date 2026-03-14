import os
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, Body
from pydantic import BaseModel
import uvicorn
import traceback

from .pipeline import build_windowed_metrics_for_dir, generate_report, choose_chat
from .progress import update_progress, get_progress, reset_progress
from .config_store import get_config_store, FormatConfigStore
from .agents import SchemaInferenceAgent, MetricSuggestionAgent, InsightGenerationAgent
from .chat_handler import chat as chat_handler_chat, get_rag_engine
from .rag import RAGEngine, get_index_status

app = FastAPI(title="Compliance Worker", version="0.1.0")

DATA_DIR = Path(os.getenv("DEFAULT_DATA_DIR", "/data"))
OUT_DIR = Path(os.getenv("OUT_DIR", "/out"))
KB_DIR = Path(os.getenv("DEFAULT_KB_DIR", "/kb"))
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize RAG index on startup if KB files exist
@app.on_event("startup")
def startup_event():
    """Initialize RAG index on startup if KB files are present."""
    try:
        if KB_DIR.exists() and any(KB_DIR.rglob("*.md")):
            engine = get_rag_engine()
            engine.rebuild_index(kb_dir=KB_DIR, out_dir=OUT_DIR)
            print(f"RAG index initialized: KB={KB_DIR}, Reports={OUT_DIR}", flush=True)
    except Exception as e:
        print(f"Warning: RAG index initialization failed: {e}", flush=True)


# -----------------------------------------------------------------------------
# Pydantic Models for Agent Endpoints
# -----------------------------------------------------------------------------

class AnalyzeFormatRequest(BaseModel):
    samples: List[str]
    max_samples: int = 20


class ApproveFormatRequest(BaseModel):
    format_id: str
    format_name: str
    format_type: str
    detection_rules: dict
    field_mappings: dict
    unmapped_fields: Optional[List[dict]] = []
    approved_by: str = "system"


class MetricSuggestionRequest(BaseModel):
    format_id: str
    available_fields: List[str]
    unmapped_fields: Optional[List[dict]] = []
    sample_stats: Optional[dict] = {}


class SaveMetricsRequest(BaseModel):
    format_id: str
    metrics: List[dict]


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None
    include_context: bool = True


class OnboardAnalyzeRequest(BaseModel):
    samples: List[str]
    max_samples: int = 20


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
def run_access_control(payload: dict = Body(default={})):
    try:
        # Reset and start progress tracking
        reset_progress()
        update_progress("init", "Starting access control report generation...")
        
        window_days = int(os.getenv("WINDOW_DAYS", "7"))
        target_filename = payload.get("filename")  # if set, only process this file (current session upload)

        # Stream over all files (or only target file), aggregate per time window
        metrics_by_window = build_windowed_metrics_for_dir(
            DATA_DIR,
            window_days=window_days,
            target_filenames=[target_filename] if target_filename else None,
        )

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

        # Re-index reports so they're available for chat queries
        try:
            engine = get_rag_engine()
            engine.rebuild_index(kb_dir=KB_DIR, out_dir=OUT_DIR)
        except Exception:
            pass  # Index update failed, but don't fail the whole request

        update_progress("complete", f"Successfully generated {len(outputs)} report(s)", is_complete=True)
        return {"ok": True, "windows": outputs}

    except Exception:
        tb = traceback.format_exc()
        print(tb, flush=True)
        update_progress("complete", f"Error: {tb[:200]}", is_complete=True, is_error=True)
        return {"error": "worker_exception", "traceback": tb}


# -----------------------------------------------------------------------------
# Chat Endpoints
# -----------------------------------------------------------------------------

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """Chat with RAG context from KB and reports."""
    try:
        result = chat_handler_chat(
            message=request.message,
            history=request.history,
            include_context=request.include_context,
        )
        return result
    except Exception as e:
        tb = traceback.format_exc()
        return {"response": f"Error: {str(e)}", "sources": [], "error": str(e), "traceback": tb}


@app.post("/chat/index")
def chat_index_rebuild():
    """Trigger re-indexing of KB and reports for RAG."""
    try:
        engine = get_rag_engine()
        result = engine.rebuild_index(kb_dir=KB_DIR, out_dir=OUT_DIR)
        return {"ok": True, **result}
    except Exception as e:
        tb = traceback.format_exc()
        return {"ok": False, "error": str(e), "traceback": tb}


@app.get("/chat/index/status")
def chat_index_status():
    """Get current RAG index status."""
    return get_index_status()


# -----------------------------------------------------------------------------
# Upload Endpoints
# -----------------------------------------------------------------------------

def _read_sample_lines(content: bytes, max_lines: int = 50) -> List[str]:
    """Decode content and return first max_lines lines."""
    text = content.decode("utf-8", errors="ignore")
    lines = []
    for line in text.splitlines():
        if len(lines) >= max_lines:
            break
        lines.append(line)
    return lines


@app.post("/upload/logs")
async def upload_logs(file: UploadFile = File(...)):
    """Upload a log file to DATA_DIR; detect format; return analysis for onboarding if unknown."""
    try:
        content = await file.read()
        filename = file.filename or "uploaded_logs.txt"
        safe_name = os.path.basename(filename).replace("..", "_")
        dest = DATA_DIR / safe_name
        dest.write_bytes(content)
    except Exception as e:
        return {"error": "upload_failed", "detail": str(e)}

    sample_lines = _read_sample_lines(content)
    if not sample_lines:
        return {"error": "empty_file", "saved_path": str(dest), "format_detected": "unknown", "needs_onboard": True}

    # Quick-analyze and check custom formats
    try:
        store = get_config_store()
        redis_ok = store.ping()
    except Exception:
        store = None
        redis_ok = False

    from .universal_logs.sniffers import find_best_matching_format, sniff_format

    custom_match = None
    if store and redis_ok:
        format_id, config, similarity = find_best_matching_format(sample_lines, store, threshold=0.3)
        if format_id:
            custom_match = {
                "format_id": format_id,
                "format_name": config.get("format_name", format_id),
                "similarity": round(similarity, 2),
            }

    builtin_format = sniff_format(sample_lines)
    known = builtin_format in {"rba", "jsonl", "csv", "syslog"} or (custom_match and custom_match.get("similarity", 0) >= 0.5)
    return {
        "ok": True,
        "saved_path": str(dest),
        "filename": safe_name,
        "format_detected": custom_match["format_id"] if custom_match and custom_match.get("similarity", 0) >= 0.5 else builtin_format,
        "custom_match": custom_match,
        "needs_onboard": not known,
        "message": "File saved. Format known; you can generate reports." if known else "File saved. Unknown format; use /onboard with this file to add format.",
    }


@app.post("/upload/kb")
async def upload_kb(file: UploadFile = File(...)):
    """Upload a KB document to KB_DIR and trigger RAG re-index."""
    try:
        content = await file.read()
        filename = file.filename or "uploaded.md"
        safe_name = os.path.basename(filename).replace("..", "_")
        if not safe_name.lower().endswith(".md"):
            safe_name = safe_name + ".md"
        KB_DIR.mkdir(parents=True, exist_ok=True)
        dest = KB_DIR / safe_name
        dest.write_bytes(content)
    except Exception as e:
        return {"error": "upload_failed", "detail": str(e)}

    try:
        engine = get_rag_engine()
        result = engine.rebuild_index(kb_dir=KB_DIR, out_dir=OUT_DIR)
        return {"ok": True, "saved_path": str(dest), "filename": safe_name, "index": result}
    except Exception as e:
        return {"ok": True, "saved_path": str(dest), "filename": safe_name, "index_error": str(e)}


# -----------------------------------------------------------------------------
# Onboard Endpoints
# -----------------------------------------------------------------------------

@app.post("/onboard/analyze")
def onboard_analyze(request: OnboardAnalyzeRequest):
    """Analyze uploaded file format and return proposed mappings for review."""
    try:
        chat_client = choose_chat()
        agent = SchemaInferenceAgent(chat_client)
        result = agent.analyze(request.samples, max_samples=request.max_samples)
        return result
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb}


@app.post("/onboard/confirm")
def onboard_confirm(request: ApproveFormatRequest):
    """Confirm and save approved format configuration (same as agent/approve-format)."""
    try:
        store = get_config_store()
        cfg = {
            "format_name": request.format_name,
            "format_type": request.format_type,
            "detection_rules": request.detection_rules,
            "field_mappings": request.field_mappings,
            "unmapped_fields": request.unmapped_fields or [],
        }
        store.save_format(request.format_id, cfg, approved_by=request.approved_by)
        return {"ok": True, "format_id": request.format_id}
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb}


# -----------------------------------------------------------------------------
# Agent Endpoints
# -----------------------------------------------------------------------------

@app.post("/agent/analyze-format")
def analyze_format(request: AnalyzeFormatRequest):
    """Analyze log samples and infer format schema using LLM."""
    try:
        chat_client = choose_chat()
        agent = SchemaInferenceAgent(chat_client)
        result = agent.analyze(request.samples, max_samples=request.max_samples)
        return result
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb}


@app.post("/agent/quick-analyze")
def quick_analyze(request: AnalyzeFormatRequest):
    """Quick heuristic-based format detection without LLM, also checks custom formats."""
    try:
        from .universal_logs.sniffers import find_best_matching_format, sniff_format
        
        # First check custom formats in Redis
        store = None
        custom_match = None
        try:
            store = get_config_store()
            if store.ping():
                format_id, config, similarity = find_best_matching_format(
                    request.samples, store, threshold=0.3
                )
                if format_id:
                    custom_match = {
                        "format_id": format_id,
                        "format_name": config.get("format_name", format_id),
                        "format_type": config.get("format_type", "custom"),
                        "similarity": round(similarity, 2),
                        "is_exact_match": similarity >= 0.8,
                        "is_onboarded": True,
                    }
        except Exception:
            pass  # Redis not available
        
        # Also run heuristic detection
        agent = SchemaInferenceAgent(chat_client=None)
        heuristic_result = agent.quick_analyze(request.samples)
        
        # Combine results
        result = {
            **heuristic_result,
            "custom_format_match": custom_match,
            "has_onboarded_match": custom_match is not None and custom_match.get("similarity", 0) >= 0.5,
        }
        
        # If we have a good custom match, prefer it
        if custom_match and custom_match.get("similarity", 0) >= 0.5:
            result["recommended_format"] = custom_match["format_id"]
            result["recommendation"] = f"Matches onboarded format: {custom_match['format_name']}"
        else:
            result["recommended_format"] = heuristic_result.get("format_type", "unknown")
            if custom_match and custom_match.get("similarity", 0) > 0:
                result["recommendation"] = f"Closest onboarded format: {custom_match['format_name']} ({custom_match['similarity']:.0%} match)"
            else:
                result["recommendation"] = "No onboarded format matches. Consider adding this format."
        
        return result
    except Exception as e:
        return {"error": str(e)}


@app.post("/agent/approve-format")
def approve_format(request: ApproveFormatRequest):
    """Save an approved format configuration to Redis."""
    try:
        store = get_config_store()
        config = {
            "format_name": request.format_name,
            "format_type": request.format_type,
            "detection_rules": request.detection_rules,
            "field_mappings": request.field_mappings,
            "unmapped_fields": request.unmapped_fields or [],
        }
        store.save_format(request.format_id, config, approved_by=request.approved_by)
        return {"ok": True, "format_id": request.format_id}
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb}


@app.get("/agent/formats")
def list_formats():
    """List all registered format configurations."""
    try:
        store = get_config_store()
        formats = store.get_all_formats()
        # Return summary info
        return {
            "formats": [
                {
                    "format_id": fmt_id,
                    "format_name": cfg.get("format_name", "Unknown"),
                    "format_type": cfg.get("format_type", "unknown"),
                    "approved_at": cfg.get("_approved_at"),
                    "approved_by": cfg.get("_approved_by"),
                }
                for fmt_id, cfg in formats.items()
            ]
        }
    except Exception as e:
        return {"error": str(e), "formats": []}


@app.get("/agent/formats/{format_id}")
def get_format(format_id: str):
    """Get details of a specific format configuration."""
    try:
        store = get_config_store()
        config = store.get_format(format_id)
        if config is None:
            raise HTTPException(status_code=404, detail=f"Format '{format_id}' not found")
        return config
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@app.delete("/agent/formats/{format_id}")
def delete_format(format_id: str):
    """Delete a format configuration."""
    try:
        store = get_config_store()
        deleted = store.delete_format(format_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Format '{format_id}' not found")
        return {"ok": True, "deleted": format_id}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@app.post("/agent/suggest-metrics")
def suggest_metrics(request: MetricSuggestionRequest):
    """Get metric suggestions for a format based on available fields."""
    try:
        chat_client = choose_chat()
        agent = MetricSuggestionAgent(chat_client)
        metrics = agent.suggest(
            available_fields=request.available_fields,
            unmapped_fields=request.unmapped_fields,
            sample_stats=request.sample_stats,
        )
        return {"metrics": metrics}
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb, "metrics": []}


@app.post("/agent/save-metrics")
def save_metrics(request: SaveMetricsRequest):
    """Save approved metric configuration for a format."""
    try:
        store = get_config_store()
        store.save_metric_config(request.format_id, request.metrics)
        return {"ok": True, "format_id": request.format_id}
    except Exception as e:
        return {"error": str(e)}


@app.get("/agent/metrics/{format_id}")
def get_metrics(format_id: str):
    """Get saved metric configuration for a format."""
    try:
        store = get_config_store()
        metrics = store.get_metric_config(format_id)
        return {"format_id": format_id, "metrics": metrics or []}
    except Exception as e:
        return {"error": str(e), "metrics": []}


@app.get("/agent/health")
def agent_health():
    """Check agent system health including Redis connectivity."""
    try:
        store = get_config_store()
        redis_ok = store.ping()
        return {
            "status": "healthy" if redis_ok else "degraded",
            "redis": "connected" if redis_ok else "disconnected",
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/agent/scan-data-formats")
def scan_data_formats():
    """
    Scan all files in DATA_DIR and check their format status.
    Returns which files match onboarded formats and which don't.
    """
    from .universal_logs.sniffers import find_best_matching_format, sniff_format
    
    try:
        store = get_config_store()
        redis_ok = store.ping() if store else False
    except Exception:
        store = None
        redis_ok = False
    
    files = [p for p in DATA_DIR.rglob("*") if p.is_file()]
    results = {
        "total_files": len(files),
        "matched_files": [],
        "unmatched_files": [],
        "unknown_files": [],
        "redis_available": redis_ok,
    }
    
    for f in files:
        try:
            # Read sample lines
            with f.open("r", encoding="utf-8", errors="ignore") as fp:
                sample_lines = []
                for _ in range(50):
                    ln = fp.readline()
                    if not ln:
                        break
                    sample_lines.append(ln)
            
            if not sample_lines:
                results["unknown_files"].append({
                    "file": f.name,
                    "path": str(f.relative_to(DATA_DIR)),
                    "reason": "Empty file",
                })
                continue
            
            # Check custom formats
            custom_match = None
            if store and redis_ok:
                format_id, config, similarity = find_best_matching_format(
                    sample_lines, store, threshold=0.3
                )
                if format_id:
                    custom_match = {
                        "format_id": format_id,
                        "format_name": config.get("format_name", format_id),
                        "similarity": round(similarity, 2),
                    }
            
            # Check built-in formats
            builtin_format = sniff_format(sample_lines)
            
            file_info = {
                "file": f.name,
                "path": str(f.relative_to(DATA_DIR)),
                "builtin_format": builtin_format,
                "custom_match": custom_match,
            }
            
            # Categorize the file
            if custom_match and custom_match["similarity"] >= 0.5:
                file_info["status"] = "matched"
                file_info["matched_format"] = custom_match["format_name"]
                results["matched_files"].append(file_info)
            elif builtin_format in {"rba", "jsonl", "csv", "syslog"}:
                file_info["status"] = "builtin"
                file_info["matched_format"] = builtin_format
                results["matched_files"].append(file_info)
            else:
                file_info["status"] = "unmatched"
                if custom_match:
                    file_info["closest_match"] = custom_match
                results["unmatched_files"].append(file_info)
                
        except Exception as e:
            results["unknown_files"].append({
                "file": f.name,
                "path": str(f.relative_to(DATA_DIR)),
                "reason": str(e),
            })
    
    # Summary
    results["summary"] = {
        "matched": len(results["matched_files"]),
        "unmatched": len(results["unmatched_files"]),
        "unknown": len(results["unknown_files"]),
        "all_formats_known": len(results["unmatched_files"]) == 0,
    }
    
    return results


if __name__ == "__main__":
    uvicorn.run("app.run_worker:app", host="0.0.0.0", port=8081, reload=False)