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
    cleaned = _safe_title(title)
    if ":" in cleaned:
        cleaned = cleaned.split(":", 1)[0].strip()
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .-_")
    cleaned = cleaned[:64].rstrip(" .-_") or "Untitled"

    if paper_id:
        normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", paper_id).strip("-")
        if normalized.startswith("paper_"):
            normalized = normalized.removeprefix("paper_")
        if normalized:
            return f"{cleaned} [{normalized[:16]}]"
    if note_id:
        normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", note_id).strip("-")
        if normalized:
            return f"{cleaned} [{normalized[:12]}]"
    return cleaned


def import_reading_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    stem = build_note_stem(title, paper_id=paper_id, note_id=note_id)
    return vault / "20_Research" / "Papers" / "_imports" / "paperquay" / "reading" / f"{stem}.md"


def import_review_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    stem = build_note_stem(title, paper_id=paper_id, note_id=note_id)
    return vault / "20_Research" / "Papers" / "_imports" / "paperquay" / "review" / f"{stem}.md"


def formal_reading_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    stem = build_note_stem(title, paper_id=paper_id, note_id=note_id)
    return vault / "20_Research" / "Papers" / "Reading Notes" / stem / "enhanced.md"


def formal_review_path(title: str, vault: Path = DEFAULT_VAULT, paper_id: str | None = None, note_id: str | None = None) -> Path:
    stem = build_note_stem(title, paper_id=paper_id, note_id=note_id)
    return vault / "20_Research" / "Papers" / "Review Notes" / stem / "enhanced.md"
