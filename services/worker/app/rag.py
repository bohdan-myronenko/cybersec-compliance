import os
import pickle
import re
import threading
from pathlib import Path
from typing import List, Optional

import faiss
import numpy as np

from . import config
from .llm_clients.embeddings_ollama import OllamaEmbeddingClient


def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks by size."""
    if not text or not text.strip():
        return []
    chunks = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end < len(text) else len(text)
    return chunks


def _chunk_markdown(content: str, chunk_size: int, overlap: int) -> List[str]:
    """Chunk markdown preferring paragraph boundaries."""
    paragraphs = re.split(r"\n\s*\n", content)
    chunks = []
    current = []
    current_len = 0
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if current_len + len(p) + 2 > chunk_size and current:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = len(p)
        else:
            current.append(p)
            current_len += len(p) + 2
    if current:
        chunks.append("\n\n".join(current))
    if not chunks:
        return _chunk_text(content, chunk_size, overlap)
    return chunks


class FaissStore:
    def __init__(self):
        self.index = None
        self.records = []

    def build(self, embeddings: np.ndarray, records):
        embeddings = (embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12)).astype(np.float32)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        self.records = list(records)

    def search(self, qvec: np.ndarray, k=6):
        if self.index is None or len(self.records) == 0:
            return []
        qvec = (qvec / (np.linalg.norm(qvec, axis=1, keepdims=True) + 1e-12)).astype(np.float32)
        k = min(k, len(self.records))
        D, I = self.index.search(qvec, k)
        return [(float(D[0][i]), self.records[I[0][i]]) for i in range(len(I[0])) if I[0][i] != -1]


def embed_texts(texts, base_url=None, model=None):
    base_url = base_url or config.OLLAMA_BASE_URL
    model = model or config.EMBED_MODEL
    client = OllamaEmbeddingClient(base_url, model)
    return client.embed(texts)


# ---------------------------------------------------------------------------
# RAG Engine: index KB + reports, search, get context
# ---------------------------------------------------------------------------

_index_lock = threading.Lock()
_index_status = {"status": "idle", "kb_count": 0, "reports_count": 0, "error": None}


class RAGEngine:
    """
    Indexes KB documents and generated reports; provides semantic search
    and formatted context for chat.
    """

    def __init__(
        self,
        kb_dir: Optional[Path] = None,
        out_dir: Optional[Path] = None,
        index_dir: Optional[Path] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        top_k: Optional[int] = None,
    ):
        self.kb_dir = Path(kb_dir) if kb_dir else Path(os.getenv("DEFAULT_KB_DIR", "/kb"))
        self.out_dir = Path(out_dir) if out_dir else Path(os.getenv("OUT_DIR", "/out"))
        self.index_dir = Path(index_dir) if index_dir else Path(config.DEFAULT_INDEX_DIR)
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        self.top_k = top_k or config.TOP_K
        self.store = FaissStore()
        self._records: List[dict] = []

    def _collect_docs(self, root: Path, source: str) -> List[dict]:
        """Collect doc chunks with source and id."""
        records = []
        for p in root.rglob("*.md"):
            if not p.is_file():
                continue
            try:
                body = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for i, chunk_text in enumerate(_chunk_markdown(body, self.chunk_size, self.chunk_overlap)):
                records.append({
                    "source": source,
                    "doc_id": str(p),
                    "title": p.stem,
                    "text": chunk_text,
                    "chunk_index": i,
                })
        return records

    def index_kb(self, kb_dir: Optional[Path] = None) -> int:
        """Index all .md files under kb_dir. Returns number of chunks indexed."""
        global _index_status
        dir_path = Path(kb_dir) if kb_dir else self.kb_dir
        if not dir_path.exists():
            with _index_lock:
                _index_status["status"] = "idle"
                _index_status["error"] = f"KB dir not found: {dir_path}"
            return 0
        with _index_lock:
            _index_status["status"] = "indexing"
            _index_status["error"] = None
        kb_records = self._collect_docs(dir_path, "kb")
        with _index_lock:
            _index_status["kb_count"] = len(kb_records)
        return len(kb_records)

    def index_reports(self, out_dir: Optional[Path] = None) -> int:
        """Index all .md reports under out_dir. Returns number of chunks indexed."""
        global _index_status
        dir_path = Path(out_dir) if out_dir else self.out_dir
        if not dir_path.exists():
            with _index_lock:
                _index_status["reports_count"] = 0
            return 0
        report_records = self._collect_docs(dir_path, "report")
        with _index_lock:
            _index_status["reports_count"] = len(report_records)
        return len(report_records)

    def rebuild_index(self, kb_dir: Optional[Path] = None, out_dir: Optional[Path] = None) -> dict:
        """
        Rebuild full index from KB and reports. Returns counts and status.
        """
        global _index_status
        kb_path = Path(kb_dir) if kb_dir else self.kb_dir
        out_path = Path(out_dir) if out_dir else self.out_dir
        with _index_lock:
            _index_status["status"] = "indexing"
            _index_status["error"] = None
        try:
            kb_records = self._collect_docs(kb_path, "kb") if kb_path.exists() else []
            report_records = self._collect_docs(out_path, "report") if out_path.exists() else []
            all_records = kb_records + report_records
            if not all_records:
                self._records = []
                self.store = FaissStore()
                with _index_lock:
                    _index_status["status"] = "idle"
                    _index_status["kb_count"] = 0
                    _index_status["reports_count"] = 0
                return {"kb_chunks": 0, "report_chunks": 0, "total": 0}
            texts = [r["text"] for r in all_records]
            embeddings = embed_texts(texts)
            self.store.build(embeddings, all_records)
            self._records = all_records
            with _index_lock:
                _index_status["status"] = "idle"
                _index_status["kb_count"] = len(kb_records)
                _index_status["reports_count"] = len(report_records)
                _index_status["error"] = None
            return {"kb_chunks": len(kb_records), "report_chunks": len(report_records), "total": len(all_records)}
        except Exception as e:
            with _index_lock:
                _index_status["status"] = "idle"
                _index_status["error"] = str(e)
            raise

    def search(self, query: str, k: Optional[int] = None) -> List[dict]:
        """Semantic search across KB and reports. Returns list of {score, record} dicts."""
        k = k or self.top_k
        if not self.store.records:
            return []
        try:
            qvec = embed_texts([query])
            hits = self.store.search(qvec, k=k)
            return [{"score": s, "record": r} for s, r in hits]
        except Exception:
            return []

    def get_context(self, query: str, max_chars: Optional[int] = None) -> str:
        """Return formatted context string from RAG search for the query."""
        max_chars = max_chars or getattr(config, "MAX_CONTEXT_CHARS", 9000)
        hits = self.search(query, k=self.top_k)
        if not hits:
            return ""
        parts = []
        total = 0
        for h in hits:
            r = h["record"]
            block = f"[{r['source']}:{r['title']}]\n{r['text']}"
            if total + len(block) > max_chars:
                break
            parts.append(block)
            total += len(block)
        return "\n\n---\n\n".join(parts)


def get_index_status() -> dict:
    """Return current RAG index status (thread-safe)."""
    with _index_lock:
        return dict(_index_status)