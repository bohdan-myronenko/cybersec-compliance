from pathlib import Path

def load_kb(root="/kb"):
    docs = []
    for p in Path(root).rglob("*.md"):
        docs.append({"id": str(p), "title": p.stem, "body": p.read_text(encoding="utf-8", errors="ignore")})
    return docs