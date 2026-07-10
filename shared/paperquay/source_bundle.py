from __future__ import annotations

import json
from pathlib import Path


def read_text(path: str | None) -> str:
    if not path:
        return ""
    real_path = Path(path)
    return real_path.read_text(encoding="utf-8", errors="ignore") if real_path.exists() else ""


def build_source_bundle(note: dict, paper: dict | None, cache: dict | None) -> dict:
    full_md = read_text(cache.get("full_md_path") if cache else None)
    content_json_text = read_text(cache.get("content_json_path") if cache else None)
    blocks = []
    if content_json_text.strip():
        try:
            blocks = json.loads(content_json_text)
        except Exception:
            blocks = []
    return {
        "note": note,
        "paper": paper,
        "cache": cache,
        "full_md_text": full_md,
        "content_json_text": content_json_text,
        "content_blocks": blocks,
    }
