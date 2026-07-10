from __future__ import annotations

import os
import re
from pathlib import Path


def _paperquay_root() -> Path:
    configured = os.environ.get("PAPERQUAY_ROOT", "").strip()
    if configured:
        return Path(configured)
    appdata = os.environ.get("APPDATA", "").strip()
    if appdata:
        return Path(appdata) / "PaperQuay" / "PaperQuay"
    return Path.home() / "AppData" / "Roaming" / "PaperQuay" / "PaperQuay"


PAPERQUAY_CACHE = _paperquay_root() / ".mineru-cache"


def fnv1a_hash(value: str) -> str:
    hashed = 2166136261
    for ch in value:
        hashed ^= ord(ch)
        hashed = (hashed * 16777619) & 0xFFFFFFFF
    return format(hashed, "08x")


def sanitize_path_segment(value: str) -> str:
    value = (value or "").strip().lower()
    if not value:
        return "document"
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:48] or "document"


def candidate_dirs(paper: dict) -> list[Path]:
    paper_id = paper["id"]
    title = paper.get("title") or ""
    pdf_path = ""
    for attachment in paper.get("attachments") or []:
        if attachment.get("kind") == "pdf":
            pdf_path = (attachment.get("stored_path") or attachment.get("original_path") or "").strip()
            break
    workspace_id = f"native-library:{paper_id}"
    item_key = paper_id
    stable_key = workspace_id or item_key or pdf_path or title or "document"
    candidates = [
        PAPERQUAY_CACHE / f"document-{fnv1a_hash(stable_key)}",
        PAPERQUAY_CACHE / f"{sanitize_path_segment(title)}-{fnv1a_hash(workspace_id)}",
        PAPERQUAY_CACHE / f"{sanitize_path_segment(title)}-{fnv1a_hash(item_key)}",
    ]
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in candidates:
        key = str(path)
        if key not in seen:
            seen.add(key)
            ordered.append(path)
    return ordered


def resolve_cache_bundle(paper: dict) -> dict | None:
    for directory in candidate_dirs(paper):
        full_md = directory / "full.md"
        content_json = directory / "content_list_v2.json"
        middle_json = directory / "middle.json"
        if full_md.exists() or content_json.exists() or middle_json.exists():
            layout_json = directory / "layout.json"
            images_dir = directory / "images"
            return {
                "cache_dir": str(directory),
                "full_md_path": str(full_md) if full_md.exists() else None,
                "content_json_path": str(content_json) if content_json.exists() else None,
                "middle_json_path": str(middle_json) if middle_json.exists() else None,
                "layout_json_path": str(layout_json) if layout_json.exists() else None,
                "images_dir": str(images_dir) if images_dir.exists() else None,
            }
    return None
