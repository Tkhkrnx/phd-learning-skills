from __future__ import annotations

import os
import re
from pathlib import Path


def _default_vault() -> Path:
    configured = os.environ.get("OBSIDIAN_VAULT", "").strip()
    if configured:
        return Path(configured)
    home = Path.home()
    return home / "Documents" / "PHR" / "obsidian_phr"


DEFAULT_VAULT = _default_vault()


def _safe_title(title: str) -> str:
    bad = '<>:"/\\|?*'
    cleaned = "".join("-" if c in bad else c for c in (title or "")).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "Untitled"


def build_note_stem(title: str, paper_id: str | None = None, note_id: str | None = None) -> str:
    primary = str(title or "")
    if ":" in primary:
        primary = primary.split(":", 1)[0].strip()
    cleaned = _safe_title(primary)
    if "," in cleaned:
        first_clause = cleaned.split(",", 1)[0].strip()
        if len(first_clause) >= 4:
            cleaned = first_clause
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .-_")
    return cleaned[:36].rstrip(" .-_") or "Untitled"


def paper_note_root(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    stem = build_note_stem(title, paper_id=paper_id, note_id=note_id)
    return vault / "Research" / "Papers" / stem


def import_reading_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    return paper_note_root(title, vault, paper_id=paper_id, note_id=note_id) / "Reading" / "original.md"


def import_review_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    return paper_note_root(title, vault, paper_id=paper_id, note_id=note_id) / "Review" / "original.md"


def formal_reading_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    return paper_note_root(title, vault, paper_id=paper_id, note_id=note_id) / "Reading" / "enhanced.md"


def formal_review_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    return paper_note_root(title, vault, paper_id=paper_id, note_id=note_id) / "Review" / "enhanced.md"
