#!/usr/bin/env python3
"""
Convert legal markdown under kb/ into higher-quality LoRA JSONL.

Key improvements over naive chunk conversion:
- Prefer full-article supervision over chunk-level supervision
- Grouped train/val split by source/article to avoid leakage
- Remove irrelevant prompt metadata
- Support structured task variants for legal instruction tuning
- Allow gold summaries/checklists from a sidecar annotations file (not implemented yet)
- Use fallback extractive key-point generation only when gold targets are absent

Expected optional annotations file format (JSON):
{
  "kb/path/to/file.md::Article 21": {
    "summary": "Article 21 requires entities to implement proportionate cybersecurity risk-management measures.",
    "obligations": [
      "Carry out risk analysis and maintain security policies",
      "Implement incident handling processes",
      "Ensure business continuity, backup, and disaster recovery",
      "Address supply chain security risks",
      "Use secure authentication, communications, and training"
    ],
    "plain_english": "This article says organisations covered by NIS2 must put real cybersecurity controls in place, not just policies on paper.",
    "checklist": [
      "Document a cybersecurity risk-management policy",
      "Maintain incident response procedures",
      "Test backup and recovery processes",
      "Assess supplier cybersecurity risks",
      "Deploy MFA or equivalent secure authentication"
    ]
  }
}

Examples:
  python scripts/kb_to_lora_dataset_v2.py --kb-dir kb --out LoRA/data/train.jsonl --mode plain_summary
  python scripts/kb_to_lora_dataset_v2.py --kb-dir kb --out LoRA/data/train.jsonl --mode multi_task --annotations gold.json
  python scripts/kb_to_lora_dataset_v2.py --kb-dir kb --out LoRA/data/train.jsonl --mode obligations --val-ratio 0.1
"""

import argparse
import json
import random
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ----------------------------
# Utility helpers
# ----------------------------

def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def write_jsonl(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def sentence_split(text: str) -> List[str]:
    text = normalize_ws(text)
    if not text:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def bullet_split(text: str) -> List[str]:
    """
    Rough extraction of list items and semi-structured legal subpoints.
    """
    lines = [ln.strip() for ln in text.splitlines()]
    items = []
    for ln in lines:
        if not ln:
            continue
        if re.match(r"^[-*•]\s+", ln):
            items.append(re.sub(r"^[-*•]\s+", "", ln).strip())
        elif re.match(r"^\(?[a-z0-9]+\)\s+", ln, flags=re.IGNORECASE):
            items.append(re.sub(r"^\(?[a-z0-9]+\)\s+", "", ln, flags=re.IGNORECASE).strip())
    return items


# ----------------------------
# Markdown / article parsing
# ----------------------------

ARTICLE_HEADING_RE = re.compile(
    r"(?im)^(#{1,6}\s*)?Article\s+(\d+[A-Za-z]?)\b[^\n]*$"
)


def extract_doc_title(body: str, fallback_title: str) -> str:
    for line in body.splitlines()[:30]:
        s = line.strip()
        if s.startswith("#"):
            return re.sub(r"^#+\s*", "", s).strip()
    return fallback_title


def split_markdown_into_articles(body: str, fallback_title: str) -> List[dict]:
    """
    Splits a markdown file into article-level records where possible.
    If no article headings are found, returns one record for the whole file.
    """
    title = extract_doc_title(body, fallback_title)
    matches = list(ARTICLE_HEADING_RE.finditer(body))

    if not matches:
        clean_body = body.strip()
        if not clean_body:
            return []
        return [{
            "title": title,
            "article": None,
            "text": clean_body,
        }]

    records = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        article_num = m.group(2)
        article_text = body[start:end].strip()
        if article_text:
            records.append({
                "title": title,
                "article": article_num,
                "text": article_text,
            })

    return records


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
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


def chunk_by_paragraph(text: str, chunk_size: int, overlap: int) -> List[str]:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = []
    current_len = 0

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        if len(p) > chunk_size:
            if current:
                chunks.append("\n\n".join(current).strip())
                current = []
                current_len = 0
            chunks.extend(chunk_text(p, chunk_size, overlap))
            continue

        if current and current_len + len(p) + 2 > chunk_size:
            chunks.append("\n\n".join(current).strip())
            current = [p]
            current_len = len(p)
        else:
            current.append(p)
            current_len += len(p) + 2

    if current:
        chunks.append("\n\n".join(current).strip())

    return chunks


def collect_records(
    kb_dir: Path,
    max_input_chars: int,
    chunk_size: int,
    chunk_overlap: int
) -> List[dict]:
    """
    Prefer article-level records. Only chunk if an article is too large.
    """
    records = []

    for p in sorted(kb_dir.rglob("*.md")):
        if not p.is_file():
            continue

        try:
            body = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for art in split_markdown_into_articles(body, p.stem):
            article_text = art["text"]
            group_id = f"{str(p)}::Article {art['article']}" if art["article"] else str(p)

            if len(article_text) <= max_input_chars:
                records.append({
                    "source": str(p),
                    "group_id": group_id,
                    "title": art["title"],
                    "article": art["article"],
                    "chunk_index": None,
                    "chunk_total": None,
                    "text": article_text,
                    "is_chunked": False,
                })
            else:
                chunks = chunk_by_paragraph(article_text, chunk_size, chunk_overlap)
                for i, chunk in enumerate(chunks):
                    records.append({
                        "source": str(p),
                        "group_id": group_id,
                        "title": art["title"],
                        "article": art["article"],
                        "chunk_index": i,
                        "chunk_total": len(chunks),
                        "text": chunk,
                        "is_chunked": True,
                    })

    return records


# ----------------------------
# Optional gold annotations
# ----------------------------

def load_annotations(path: Optional[Path]) -> Dict[str, dict]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Annotations file must be a JSON object")
    return data


def annotation_key(record: dict) -> str:
    if record.get("article"):
        return f"{record['source']}::Article {record['article']}"
    return record["source"]


# ----------------------------
# Better fallback target generation
# ----------------------------

def fallback_summary(record: dict) -> str:
    """
    Conservative fallback. Still weaker than gold summaries, but better than
    'first 2 sentences' because it prefers heading + list-style content.
    """
    article = record.get("article")
    label = f"Article {article}" if article else (record.get("title") or "This provision")
    text = record["text"].strip()

    # Remove markdown headings for cleaner extraction
    cleaned = re.sub(r"(?m)^#{1,6}\s*", "", text).strip()

    bullets = bullet_split(cleaned)
    if bullets:
        bullets = [normalize_ws(b) for b in bullets[:5]]
        joined = "; ".join(bullets)
        return f"{label} sets out the following main requirements: {joined}."

    sents = sentence_split(cleaned)
    if not sents:
        return f"{label} sets out legal requirements."
    if len(sents) == 1:
        return f"{label} provides that {sents[0][0].lower() + sents[0][1:]}" if len(sents[0]) > 1 else f"{label} sets out legal requirements."
    return f"{label} mainly requires that {sents[0][0].lower() + sents[0][1:]} {sents[1]}"


def fallback_obligations(record: dict) -> List[str]:
    """
    Extract rough obligations from bullets or semicolon-heavy prose.
    """
    text = record["text"].strip()
    cleaned = re.sub(r"(?m)^#{1,6}\s*", "", text).strip()

    items = bullet_split(cleaned)
    if items:
        return [normalize_ws(x).rstrip(".") for x in items[:8]]

    # Split legal lists introduced by colon/semicolon
    semis = [normalize_ws(x).rstrip(".") for x in cleaned.split(";") if normalize_ws(x)]
    if len(semis) >= 2:
        return semis[:8]

    sents = sentence_split(cleaned)
    return [normalize_ws(s).rstrip(".") for s in sents[:5]]


def fallback_plain_english(record: dict) -> str:
    article = record.get("article")
    label = f"Article {article}" if article else "This provision"
    summary = fallback_summary(record)
    summary = re.sub(rf"^{re.escape(label)}\s+(sets out|mainly requires that|provides that)\s*", "", summary, flags=re.IGNORECASE)
    return f"In practical terms, {label} means {summary[0].lower() + summary[1:]}" if len(summary) > 1 else f"In practical terms, {label} creates legal obligations."


def fallback_checklist(record: dict) -> List[str]:
    obligations = fallback_obligations(record)
    out = []
    for item in obligations[:8]:
        item = item.strip()
        item = re.sub(r"^(that|the following main requirements:)\s*", "", item, flags=re.IGNORECASE)
        item = item[0].upper() + item[1:] if item else item
        if not item.lower().startswith(("document", "implement", "maintain", "ensure", "assess", "establish", "adopt", "use")):
            item = f"Review whether the organisation has measures to {item[0].lower() + item[1:]}" if len(item) > 1 else "Review compliance"
        out.append(item.rstrip("."))
    return out


# ----------------------------
# Example builders
# ----------------------------

def build_context(record: dict) -> str:
    """
    Keep prompt context focused on the legal text itself.
    Avoid teaching the model to depend on irrelevant metadata.
    """
    title = record.get("title") or "Legal provision"
    article = record.get("article")

    header_parts = [f"Title: {title}"]
    if article:
        header_parts.append(f"Article: {article}")
    if record.get("is_chunked"):
        header_parts.append(
            f"Note: this is part {record['chunk_index'] + 1} of {record['chunk_total']} of the same article."
        )

    header = "\n".join(header_parts)
    return f"{header}\n\nText:\n{record['text'].strip()}"


def get_targets(record: dict, annotations: Dict[str, dict]) -> dict:
    key = annotation_key(record)
    ann = annotations.get(key, {})

    return {
        "summary": ann.get("summary") or fallback_summary(record),
        "obligations": ann.get("obligations") or fallback_obligations(record),
        "plain_english": ann.get("plain_english") or fallback_plain_english(record),
        "checklist": ann.get("checklist") or fallback_checklist(record),
    }


def make_plain_summary_example(record: dict, annotations: Dict[str, dict]) -> dict:
    article = record.get("article")
    instruction = (
        f"Summarise Article {article} of the NIS2 Directive in plain English in 2-4 sentences."
        if article else
        "Summarise the following legal provision in plain English in 2-4 sentences."
    )

    targets = get_targets(record, annotations)
    return {
        "instruction": instruction,
        "input": build_context(record),
        "output": targets["summary"],
        "group_id": record["group_id"],
    }


def make_obligations_example(record: dict, annotations: Dict[str, dict]) -> dict:
    article = record.get("article")
    instruction = (
        f"List the main obligations created by Article {article} of the NIS2 Directive as bullet points."
        if article else
        "List the main obligations created by the following legal provision as bullet points."
    )

    targets = get_targets(record, annotations)
    output = "\n".join(f"- {x}" for x in targets["obligations"])
    return {
        "instruction": instruction,
        "input": build_context(record),
        "output": output,
        "group_id": record["group_id"],
    }


def make_checklist_example(record: dict, annotations: Dict[str, dict]) -> dict:
    article = record.get("article")
    instruction = (
        f"Turn Article {article} of the NIS2 Directive into a compliance checklist."
        if article else
        "Turn the following legal provision into a compliance checklist."
    )

    targets = get_targets(record, annotations)
    output = "\n".join(f"- {x}" for x in targets["checklist"])
    return {
        "instruction": instruction,
        "input": build_context(record),
        "output": output,
        "group_id": record["group_id"],
    }


def make_plain_english_example(record: dict, annotations: Dict[str, dict]) -> dict:
    article = record.get("article")
    instruction = (
        f"Explain Article {article} of the NIS2 Directive in plain English for a security manager."
        if article else
        "Explain the following legal provision in plain English for a security manager."
    )

    targets = get_targets(record, annotations)
    return {
        "instruction": instruction,
        "input": build_context(record),
        "output": targets["plain_english"],
        "group_id": record["group_id"],
    }


def make_completion_example(record: dict) -> dict:
    article = record.get("article")
    title = record.get("title") or "Legal provision"

    lines = []
    if title:
        lines.append(title)
    if article:
        lines.append(f"Article {article}")
    lines.append(record["text"].strip())

    return {
        "text": "\n\n".join(lines).strip(),
        "group_id": record["group_id"],
    }


def to_examples(record: dict, mode: str, annotations: Dict[str, dict]) -> List[dict]:
    if mode == "completion":
        return [make_completion_example(record)]
    if mode == "plain_summary":
        return [make_plain_summary_example(record, annotations)]
    if mode == "obligations":
        return [make_obligations_example(record, annotations)]
    if mode == "checklist":
        return [make_checklist_example(record, annotations)]
    if mode == "plain_english":
        return [make_plain_english_example(record, annotations)]
    if mode == "multi_task":
        return [
            make_plain_summary_example(record, annotations),
            make_obligations_example(record, annotations),
            make_checklist_example(record, annotations),
            make_plain_english_example(record, annotations),
        ]
    raise ValueError(f"Unsupported mode: {mode}")


# ----------------------------
# Train/val split by group
# ----------------------------

def grouped_split(rows: List[dict], val_ratio: float, seed: int = 42) -> Tuple[List[dict], List[dict]]:
    if val_ratio <= 0:
        return rows, []

    groups = {}
    for row in rows:
        gid = row.get("group_id", f"row-{id(row)}")
        groups.setdefault(gid, []).append(row)

    group_ids = list(groups.keys())
    random.Random(seed).shuffle(group_ids)

    n_val = max(1, int(len(group_ids) * val_ratio))
    val_groups = set(group_ids[:n_val])

    train_rows, val_rows = [], []
    for gid, items in groups.items():
        if gid in val_groups:
            val_rows.extend(items)
        else:
            train_rows.extend(items)

    return train_rows, val_rows


def strip_internal_fields(rows: List[dict]) -> List[dict]:
    cleaned = []
    for row in rows:
        row = dict(row)
        row.pop("group_id", None)
        cleaned.append(row)
    return cleaned


# ----------------------------
# Main
# ----------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert legal markdown into LoRA-ready JSONL")
    parser.add_argument("--kb-dir", type=Path, default=Path("kb"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--mode", choices=[
        "completion",
        "plain_summary",
        "obligations",
        "checklist",
        "plain_english",
        "multi_task",
    ], default="multi_task")
    parser.add_argument("--annotations", type=Path, default=None, help="Optional JSON file containing gold targets")
    parser.add_argument("--max-input-chars", type=int, default=6000, help="Prefer full-article records up to this size")
    parser.add_argument("--chunk-size", type=int, default=3000, help="Fallback chunk size for long articles")
    parser.add_argument("--chunk-overlap", type=int, default=300, help="Fallback chunk overlap")
    parser.add_argument("--val-ratio", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    kb_dir = args.kb_dir.resolve()
    out_path = args.out.resolve()

    if not kb_dir.exists():
        raise SystemExit(f"KB dir not found: {kb_dir}")

    annotations = load_annotations(args.annotations.resolve()) if args.annotations else {}

    records = collect_records(
        kb_dir=kb_dir,
        max_input_chars=args.max_input_chars,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    if not records:
        raise SystemExit(f"No records found under: {kb_dir}")

    rows = []
    for record in records:
        rows.extend(to_examples(record, args.mode, annotations))

    if not rows:
        raise SystemExit("No rows generated")

    train_rows, val_rows = grouped_split(rows, args.val_ratio, seed=args.seed)
    train_rows = strip_internal_fields(train_rows)
    val_rows = strip_internal_fields(val_rows)

    if args.val_ratio > 0:
        train_path = out_path.parent / "train.jsonl"
        val_path = out_path.parent / "val.jsonl"
        write_jsonl(train_path, train_rows)
        write_jsonl(val_path, val_rows)
        print(f"Wrote {len(train_rows)} train rows -> {train_path}")
        print(f"Wrote {len(val_rows)} val rows -> {val_path}")
    else:
        write_jsonl(out_path, train_rows)
        print(f"Wrote {len(train_rows)} rows -> {out_path}")


if __name__ == "__main__":
    main()