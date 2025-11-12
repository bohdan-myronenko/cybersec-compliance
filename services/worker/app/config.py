import os

def getenv(key, default=None):
    v = os.getenv(key, default)
    if v is None:
        raise RuntimeError(f"Missing env var: {key}")
    return v

API_MODE = getenv("API_MODE", "LOCAL").upper()
OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://ollama:11434")
EMBED_MODEL = getenv("EMBED_MODEL", "nomic-embed-text")
LLM_MODEL = getenv("LLM_MODEL", "llama3.1:8b")

API_URL = getenv("API_URL", "https://llm.chutes.ai/v1/chat/completions")
API_KEY = getenv("API_KEY")
API_MODEL = getenv("API_MODEL", "deepseek-ai/DeepSeek-V3-0324")

DEFAULT_DATA_DIR = getenv("DEFAULT_DATA_DIR", "/data")
DEFAULT_INDEX_DIR = getenv("DEFAULT_INDEX_DIR", "/index")
CHUNK_SIZE = int(getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(getenv("CHUNK_OVERLAP", "200"))
TOP_K = int(getenv("TOP_K", "6"))
MAX_CONTEXT_CHARS = int(getenv("MAX_CONTEXT_CHARS", "9000"))

SYSTEM_PROMPT = getenv("SYSTEM_PROMPT",
    "You are a concise, expert assistant. Answer using ONLY provided context when relevant.")