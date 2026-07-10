from __future__ import annotations

import re
from pathlib import Path

from shared.obsidian.vault_paths import DEFAULT_VAULT


def normalize_title_for_match(text: str) -> str:
    lowered = (text or "").lower()
    lowered = re.sub(r"\[[^\]]+\]", " ", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def classify_note_path(path: Path) -> str:
    path_text = str(path)
    name = path.name.lower()
    if name == "enhanced.md":
        return "enhanced_support"
    if name == "original.md":
        return "original_support"
    if name == "writer_prompt.md":
        return "prompt_support"
    if "_imports\\paperquay" in path_text:
        return "paperquay_import"
    if "\\Reading Notes\\" in path_text and "[" not in path.name:
        return "reading_note_final"
    if "\\Review Notes\\" in path_text and "[" not in path.name:
        return "review_note_final"
    if "\\Reading Notes\\" in path_text:
        return "reading_note_support"
    if "\\Review Notes\\" in path_text:
        return "review_note_support"
    return "other"


def classification_score(kind: str) -> int:
    return {
        "reading_note_final": 80,
        "review_note_final": 75,
        "enhanced_support": 45,
        "reading_note_support": 35,
        "review_note_support": 30,
        "original_support": 20,
        "paperquay_import": 10,
        "prompt_support": 0,
        "other": 5,
    }.get(kind, 0)


def score_note_hit(path: Path, text: str, query: str) -> tuple[int, str]:
    kind = classify_note_path(path)
    lowered = query.lower()
    score = classification_score(kind)
    if lowered in path.name.lower():
        score += 50
    if lowered in text.lower():
        score += 20
    if path.stem.lower() == lowered:
        score += 20
    if path.name.lower().startswith(lowered):
        score += 15
    return score, kind


def search_vault_notes(query: str, vault: Path = DEFAULT_VAULT, limit: int = 20) -> list[dict]:
    lowered = query.lower()
    hits: list[dict] = []
    for candidate in vault.rglob("*.md"):
        try:
            text = candidate.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if lowered not in text.lower() and lowered not in candidate.name.lower():
            continue
        score, kind = score_note_hit(candidate, text, query)
        hits.append({"path": str(candidate), "score": score, "kind": kind})
    hits.sort(key=lambda item: (item["score"], item["kind"]), reverse=True)
    return hits[:limit]


def has_probable_duplicate(title: str, hits: list[dict]) -> bool:
    target = normalize_title_for_match(title)
    if not target:
        return False
    for hit in hits:
        candidate = normalize_title_for_match(Path(hit["path"]).stem)
        if candidate == target:
            return True
        if candidate and (candidate in target or target in candidate):
            if hit.get("score", 0) >= 90:
                return True
    return False
