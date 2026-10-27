from __future__ import annotations

import os
import re
import unicodedata
from collections.abc import Iterator
from pathlib import Path

import yaml

from shared.obsidian.vault_paths import DEFAULT_VAULT


def normalize_title_for_match(text: str) -> str:
    lowered = unicodedata.normalize("NFKC", text or "").casefold()
    lowered = re.sub(r"\[[^\]]+\]", " ", lowered)
    lowered = "".join(char if char.isalnum() else " " for char in lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def classify_note_path(path: Path) -> str:
    parts = [part.casefold() for part in re.split(r"[/\\]+", str(path))]
    in_reading = "reading" in parts[:-1]
    in_review = "review" in parts[:-1]
    name = parts[-1] if parts else ""
    if name == "enhanced.md" and in_reading:
        return "reading_note_final"
    if in_review and name == "analysis.md":
        return "review_analysis"
    if in_review and name == "formal-review.md":
        return "review_report"
    if name == "enhanced.md" and in_review:
        # The legacy name alone does not identify the review stage.
        return "review_note_legacy"
    if name == "enhanced.md":
        return "enhanced_support"
    if name == "original.md":
        return "original_support"
    if name == "writer_prompt.md":
        return "prompt_support"
    if in_reading:
        return "reading_note_support"
    if in_review:
        return "review_note_support"
    return "other"


def classification_score(kind: str) -> int:
    return {
        "reading_note_final": 80,
        "review_report": 75,
        "review_analysis": 75,
        "review_note_legacy": 70,
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


def _note_title(text: str) -> str:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", text, re.S)
    if match:
        try:
            data = yaml.safe_load(match[1])
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict) and isinstance(data.get("title"), str):
            return data["title"]
    return ""


def _note_files(vault: Path) -> Iterator[Path]:
    # Obsidian's local Skill mirrors and configuration are not user notes.
    root = vault.resolve()
    for directory, names, files in os.walk(root, followlinks=False):
        names[:] = [name for name in names
                    if not name.startswith(".")
                    and name not in {"node_modules", "__pycache__", "venv"}
                    and not (Path(directory) / name).is_symlink()
                    and not getattr(Path(directory) / name, "is_junction", lambda: False)()]
        for name in sorted(files):
            candidate = Path(directory) / name
            if name.startswith(".") or candidate.suffix.lower() != ".md" or candidate.is_symlink():
                continue
            if candidate.resolve().is_relative_to(root):
                yield candidate


def search_vault_notes(query: str, vault: Path = DEFAULT_VAULT, limit: int = 20) -> list[dict]:
    lowered = query.strip().lower()
    if not lowered or limit <= 0:
        return []
    hits: list[dict] = []
    for candidate in _note_files(vault):
        try:
            text = candidate.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            continue
        if lowered not in text.lower() and lowered not in candidate.name.lower():
            continue
        score, kind = score_note_hit(candidate, text, query.strip())
        hits.append({"path": str(candidate), "score": score, "kind": kind, "title": _note_title(text)})
    hits.sort(key=lambda item: (-item["score"], item["kind"], item["path"]))
    return hits[:limit]


def has_probable_duplicate(title: str, hits: list[dict]) -> bool:
    target = normalize_title_for_match(title)
    if not target:
        return False
    for hit in hits:
        for label in (hit.get("title", ""), Path(hit["path"]).stem):
            candidate = normalize_title_for_match(label)
            if candidate == target:
                return True
            if candidate and (candidate in target or target in candidate):
                if hit.get("score", 0) >= 90:
                    return True
    return False
