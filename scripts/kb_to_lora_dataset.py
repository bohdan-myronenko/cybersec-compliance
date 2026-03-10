#!/usr/bin/env python3
"""
Convert NIS2/legal markdown under kb/ into LoRA-ready JSONL.

Modes:
  - completion: raw text corpus for continued pretraining / domain adaptation
  - grounded_summary: instruction tuning with source text in input and summary in output
  - qa: instruction tuning with legal Q/A examples

Examples:
  python scripts/kb_to_lora_dataset.py --kb-dir kb --out LoRA/data/train.jsonl --mode completion
  python scripts/kb_to_lora_dataset.py --kb-dir kb --out LoRA/data/train.jsonl --mode grounded_summary
  python scripts/kb_to_lora_dataset.py --kb-dir kb --out LoRA/data/train.jsonl --mode qa --val-ratio 0.1
"""

import argparse
import json
import random
import re
from pathlib import Path


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if not text or not text.strip():
        return []

    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - overlap, start + 1)

    return chunks


def chunk_markdown(content: str, chunk_size: int, overlap: int) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", content)
    chunks = []
    current = []
    current_len = 0

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        # If a single paragraph is too large, split it directly.
        if len(p) > chunk_size:
            if current:
                chunks.append("\n\n".join(current))
                current = []
                current_len = 0
            chunks.extend(chunk_text(p, chunk_size, overlap))
            continue

        if current and current_len + len(p) + 2 > chunk_size:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = len(p)
        else:
            current.append(p)
            current_len += len(p) + 2

    if current:
        chunks.append("\n\n".join(current))

    return chunks if chunks else chunk_text(content, chunk_size, overlap)


def extract_title_and_article(body: str, fallback_title: str) -> tuple[str, str | None]:
    title = fallback_title
    article = None

    lines = body.splitlines()
    for line in lines[:20]:
        s = line.strip()
        if not s:
            continue

        if s.startswith("#"):
            title = re.sub(r"^#+\s*", "", s).strip()
            break

    m = re.search(r"\bArticle\s+(\d+[A-Za-z]?)\b", body, flags=re.IGNORECASE)
    if m:
        article = m.group(1)

    return title, article


def collect_chunks(kb_dir: Path, chunk_size: int, chunk_overlap: int) -> list[dict]:
    records = []

    for p in sorted(kb_dir.rglob("*.md")):
        if not p.is_file():
            continue

        try:
            body = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        title, article = extract_title_and_article(body, p.stem)
        chunks = chunk_markdown(body, chunk_size, chunk_overlap)

        for i, chunk in enumerate(chunks):
            records.append(
                {
                    "source": str(p),
                    "title": title,
                    "article": article,
                    "chunk_index": i,
                    "text": chunk,
                }
            )

    return records


def summarize_chunk_rule_based(record: dict) -> str:
    """
    Placeholder summarizer.
    Replace with human-written summaries or a trusted generation pipeline.
    For legal work, human-reviewed summaries are strongly preferred.
    """
    title = record.get("title") or "this provision"
    article = record.get("article")
    prefix = f"Article {article}" if article else title

    text = re.sub(r"\s+", " ", record["text"]).strip()

    # Simple extractive fallback: first 2 sentences max.
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(sentences[:2]).strip()

    if not summary:
        summary = text[:300].strip()

    return f"{prefix} concerns the following: {summary}"


def make_grounded_summary_example(record: dict) -> dict:
    article = record.get("article")
    title = record.get("title") or "Legal provision"

    if article:
        instruction = f"Summarize Article {article} of the NIS2 Directive in plain English."
    else:
        instruction = f"Summarize the following legal provision in plain English."

    input_text = (
        f"Title: {title}\n"
        f"Source: {record['source']}\n"
        f"Chunk: {record['chunk_index']}\n\n"
        f"{record['text']}"
    )

    output_text = summarize_chunk_rule_based(record)

    return {
        "instruction": instruction,
        "input": input_text,
        "output": output_text,
    }


def make_qa_examples(record: dict) -> list[dict]:
    article = record.get("article")
    title = record.get("title") or "Legal provision"

    label = f"Article {article}" if article else title

    context = (
        f"Title: {title}\n"
        f"Source: {record['source']}\n"
        f"Chunk: {record['chunk_index']}\n\n"
        f"{record['text']}"
    )

    summary = summarize_chunk_rule_based(record)

    examples = [
        {
            "instruction": f"What does {label} say?",
            "input": context,
            "output": summary,
        },
        {
            "instruction": f"Explain {label} in plain English.",
            "input": context,
            "output": summary,
        },
        {
            "instruction": f"Summarize the obligations in {label}.",
            "input": context,
            "output": summary,
        },
    ]

    return examples


def to_examples(record: dict, mode: str) -> list[dict]:
    if mode == "completion":
        enriched = ""
        if record.get("article"):
            enriched += f"Article {record['article']}\n"
        enriched += f"{record['title']}\n\n{record['text']}"
        return [{"text": enriched.strip()}]

    if mode == "grounded_summary":
        return [make_grounded_summary_example(record)]

    if mode == "qa":
        return make_qa_examples(record)

    raise ValueError(f"Unsupported mode: {mode}")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Convert kb markdown into LoRA-ready JSONL")
    parser.add_argument("--kb-dir", type=Path, default=Path("kb"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--chunk-size", type=int, default=1200)
    parser.add_argument("--chunk-overlap", type=int, default=200)
    parser.add_argument("--mode", choices=["completion", "grounded_summary", "qa"], default="grounded_summary")
    parser.add_argument("--val-ratio", type=float, default=0.0)
    args = parser.parse_args()

    kb_dir = args.kb_dir.resolve()
    out_path = args.out.resolve()

    if not kb_dir.exists():
        raise SystemExit(f"KB dir not found: {kb_dir}")

    records = collect_chunks(kb_dir, args.chunk_size, args.chunk_overlap)
    if not records:
        raise SystemExit(f"No markdown chunks found under: {kb_dir}")

    rows = []
    for record in records:
        rows.extend(to_examples(record, args.mode))

    if not rows:
        raise SystemExit("No rows generated")

    if args.val_ratio > 0:
        random.seed(42)
        idx = list(range(len(rows)))
        random.shuffle(idx)
        n_val = max(1, int(len(rows) * args.val_ratio))
        val_idx = set(idx[:n_val])

        train_rows = [r for i, r in enumerate(rows) if i not in val_idx]
        val_rows = [r for i, r in enumerate(rows) if i in val_idx]

        train_path = out_path.parent / "train.jsonl"
        val_path = out_path.parent / "val.jsonl"

        write_jsonl(train_path, train_rows)
        write_jsonl(val_path, val_rows)

        print(f"Wrote {len(train_rows)} train rows -> {train_path}")
        print(f"Wrote {len(val_rows)} val rows -> {val_path}")
    else:
        write_jsonl(out_path, rows)
        print(f"Wrote {len(rows)} rows -> {out_path}")


if __name__ == "__main__":
    main()