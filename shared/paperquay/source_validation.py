from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


STOPWORDS = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "the", "to", "with"}


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", str(value or "").lower()).strip()


def title_tokens(value: str) -> set[str]:
    return {token for token in normalize_title(value).split() if len(token) > 1 and token not in STOPWORDS}


def first_markdown_heading(text: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text or "")
    return match.group(1).strip() if match else ""


def title_score(left: str, right: str) -> float:
    a = normalize_title(left)
    b = normalize_title(right)
    if not a or not b:
        return 0.0
    seq = SequenceMatcher(None, a, b).ratio()
    ta, tb = title_tokens(a), title_tokens(b)
    overlap = len(ta & tb) / max(1, len(ta | tb))
    return max(seq, overlap)


def _anchor_titles(note: dict[str, Any]) -> list[str]:
    raw = note.get("anchors")
    if not raw:
        return []
    try:
        anchors = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return []
    return [str(item.get("sourceTitle") or "").strip() for item in anchors if isinstance(item, dict) and item.get("sourceTitle")]


def validate_source_alignment(note: dict[str, Any], paper: dict[str, Any] | None, cache: dict[str, Any] | None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    paper_title = str((paper or {}).get("title") or "")
    full_md_path = Path(str((cache or {}).get("full_md_path") or ""))
    full_md = full_md_path.read_text(encoding="utf-8", errors="ignore") if full_md_path.is_file() else ""
    cache_title = first_markdown_heading(full_md)
    cache_title_score = title_score(paper_title, cache_title)

    if not paper:
        errors.append("paper record is missing")
    if not full_md:
        errors.append("MinerU full.md is missing")
    elif cache_title_score < 0.55:
        errors.append("paper title does not align with MinerU full.md title")

    anchor_scores = [title_score(paper_title, item) for item in _anchor_titles(note)]
    if anchor_scores and max(anchor_scores) < 0.55:
        errors.append("selected paper title does not align with note anchors")

    note_text = str(note.get("content_text") or "")
    expected_tokens = title_tokens(paper_title)
    note_tokens = title_tokens(note_text)
    if note_text and expected_tokens and not (expected_tokens & note_tokens):
        warnings.append("note text has no direct title-token overlap; manual semantic review required")

    if paper and cache_title and cache_title_score < 0.8:
        warnings.append("paper/cache titles are similar but not identical")

    return {
        "status": "passed" if not errors else "failed",
        "paper_title": paper_title,
        "cache_title": cache_title,
        "cache_title_score": round(cache_title_score, 4),
        "errors": errors,
        "warnings": warnings,
    }
