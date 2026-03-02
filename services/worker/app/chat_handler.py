"""
Chat handler: RAG context assembly and LLM chat for the Chat UI.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import config
from .pipeline import choose_chat
from .rag import RAGEngine, get_index_status


# System prompt for chat when context is provided
CHAT_SYSTEM_WITH_CONTEXT = """You are a concise expert assistant for cybersecurity compliance.
Answer using the REFERENCE CONTEXT below when it is relevant to the user's question.
If the context does not contain relevant information, say so briefly.
Cite sources from the context when possible (e.g. "According to [report:access_control_report_...]...").
Keep answers focused and under 300 words unless the user asks for detail."""

CHAT_SYSTEM_NO_CONTEXT = """You are a concise expert assistant for cybersecurity compliance.
Answer briefly. If the user asks about knowledge base content or reports, suggest they ensure documents are uploaded and indexed."""


# Global RAG engine instance (singleton)
_rag_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    """Return a shared RAGEngine instance, initializing it if needed."""
    global _rag_engine
    if _rag_engine is None:
        kb_dir = Path(os.getenv("DEFAULT_KB_DIR", "/kb"))
        out_dir = Path(os.getenv("OUT_DIR", "/out"))
        _rag_engine = RAGEngine(kb_dir=kb_dir, out_dir=out_dir)
        # Auto-build index if KB files exist
        if kb_dir.exists() and any(kb_dir.rglob("*.md")):
            try:
                _rag_engine.rebuild_index(kb_dir=kb_dir, out_dir=out_dir)
            except Exception:
                pass  # Index build failed, but continue - will be empty
    return _rag_engine


# ---------------------------------------------------------------------------
# Confidence computation
# ---------------------------------------------------------------------------

def compute_confidence(
    hits: List[dict],
    context: str,
    index_status: dict,
) -> Dict[str, Any]:
    """
    Compute a confidence score (0-100) for a chat answer.

    Returns a dict with:
        confidence  – overall percentage (float, 0-100)
        factors     – list of {name, score, max, description} for the UI
    """
    factors: List[Dict[str, Any]] = []

    # 1. Index Health (25%) — are KB and report chunks indexed?
    kb_count = index_status.get("kb_count", 0)
    reports_count = index_status.get("reports_count", 0)
    has_kb = min(kb_count / 5, 1.0)            # saturates at 5+ chunks
    has_reports = min(reports_count / 3, 1.0)   # saturates at 3+ chunks
    index_score = (has_kb + has_reports) / 2
    factors.append({
        "name": "Index health",
        "score": round(index_score * 100, 1),
        "max": 100,
        "description": f"KB chunks: {kb_count}, Report chunks: {reports_count}",
    })

    # 2. Best match similarity (40%) — cosine similarity of the top hit
    if hits:
        top_score = max(h["score"] for h in hits)
        similarity_score = max(0.0, min(top_score, 1.0))
    else:
        top_score = 0.0
        similarity_score = 0.0
    factors.append({
        "name": "Best match similarity",
        "score": round(similarity_score * 100, 1),
        "max": 100,
        "description": f"Top cosine similarity: {top_score:.3f}" if hits else "No matching documents found",
    })

    # 3. Source coverage (15%) — do we have both KB *and* report hits?
    source_types = {h["record"]["source"] for h in hits} if hits else set()
    coverage_score = len(source_types) / 2  # 0, 0.5, or 1.0
    present = ", ".join(sorted(source_types)) if source_types else "none"
    factors.append({
        "name": "Source coverage",
        "score": round(coverage_score * 100, 1),
        "max": 100,
        "description": f"Source types present: {present}",
    })

    # 4. Context fill (20%) — how much of the context window was used
    max_chars = getattr(config, "MAX_CONTEXT_CHARS", 9000)
    fill_ratio = min(len(context) / max_chars, 1.0) if max_chars else 0.0
    factors.append({
        "name": "Context utilisation",
        "score": round(fill_ratio * 100, 1),
        "max": 100,
        "description": f"{len(context):,} / {max_chars:,} chars used",
    })

    # Weighted total
    confidence = (
        0.25 * index_score
        + 0.40 * similarity_score
        + 0.15 * coverage_score
        + 0.20 * fill_ratio
    )
    confidence_pct = round(confidence * 100, 1)

    return {"confidence": confidence_pct, "factors": factors}


# ---------------------------------------------------------------------------
# Main chat function
# ---------------------------------------------------------------------------

def chat(
    message: str,
    history: Optional[List[Dict[str, str]]] = None,
    include_context: bool = True,
) -> Dict[str, Any]:
    """
    Handle a chat message: retrieve RAG context, build prompt, call LLM.
    Returns {"response": str, "sources": list, "confidence": float, "confidence_factors": list}.
    """
    history = history or []
    engine = get_rag_engine()
    context = ""
    sources: List[dict] = []
    hits: List[dict] = []

    if include_context and message.strip():
        context = engine.get_context(message)
        hits = engine.search(message, k=config.TOP_K)
        sources = [
            {"source": h["record"]["source"], "title": h["record"]["title"], "score": h["score"]}
            for h in hits
        ]

    # Compute confidence
    index_status = get_index_status()
    conf = compute_confidence(hits, context, index_status)

    if context:
        system_prompt = CHAT_SYSTEM_WITH_CONTEXT + "\n\nREFERENCE CONTEXT:\n" + context
    else:
        system_prompt = CHAT_SYSTEM_NO_CONTEXT

    # Optional: prepend recent history as user/assistant turns for context
    user_prompt = message
    if history:
        history_block = "\n".join(
            f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}"
            for m in history[-10:]  # last 10 turns
        )
        user_prompt = f"Previous conversation:\n{history_block}\n\nUser: {message}"

    try:
        client = choose_chat()
        response = client.chat(system_prompt, user_prompt)
        return {
            "response": response,
            "sources": sources,
            "confidence": conf["confidence"],
            "confidence_factors": conf["factors"],
        }
    except Exception as e:
        return {
            "response": f"Error calling LLM: {str(e)}",
            "sources": [],
            "confidence": 0.0,
            "confidence_factors": [],
        }
