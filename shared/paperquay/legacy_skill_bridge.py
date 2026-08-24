from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from shared.obsidian.vault_paths import DEFAULT_VAULT, build_note_stem


def authors_to_string(paper: dict | None) -> str:
    if not paper:
        return "待确认"
    authors = paper.get("authors") or []
    names = [str(item.get("name") or "").strip() for item in authors if str(item.get("name") or "").strip()]
    return ", ".join(names) if names else "待确认"


def attachment_pdf_path(paper: dict | None) -> str:
    if not paper:
        return ""
    for attachment in paper.get("attachments") or []:
        if attachment.get("kind") != "pdf":
            continue
        for key in ("stored_path", "original_path", "relative_path"):
            value = str(attachment.get(key) or "").strip()
            if value:
                return value
    return ""


def find_translated_markdown(cache: dict | None) -> str | None:
    if not cache:
        return None
    cache_dir = Path(str(cache.get("cache_dir") or ""))
    candidates: list[Path] = []
    translations_dir = cache_dir / "translations"
    if translations_dir.exists():
        candidates.extend(sorted(translations_dir.rglob("*.md")))
    full_md = str(cache.get("full_md_path") or "")
    if full_md:
        base = Path(full_md)
        candidates.extend([base.with_suffix(".zh-CN.md"), base.with_name(base.stem + ".zh-CN.md")])
    seen: set[str] = set()
    for path in candidates:
        text = str(path)
        if text in seen:
            continue
        seen.add(text)
        if path.exists():
            return str(path)
    return None


def collect_image_aliases(cache: dict | None) -> list[dict[str, str]]:
    if not cache or not cache.get("images_dir"):
        return []
    images_dir = Path(str(cache["images_dir"]))
    aliases: list[dict[str, str]] = []
    for path in sorted(images_dir.iterdir()):
        if not path.is_file():
            continue
        aliases.append({"original": path.name, "alias": path.name, "path": str(path)})
    return aliases


def infer_domain(paper: dict | None) -> str:
    if not paper:
        return "LLM Inference Systems"
    haystack = " ".join(
        [
            str(paper.get("title") or ""),
            str(paper.get("publication") or ""),
            " ".join(str(item or "") for item in (paper.get("keywords") or [])),
        ]
    ).lower()
    if any(token in haystack for token in ["speculative decoding", "inference", "kv", "cache", "serving", "decode", "prefill"]):
        return "LLM Inference Systems"
    if any(token in haystack for token in ["runtime", "scheduler", "scheduling", "placement", "queue", "transaction"]):
        return "State-Centric Runtime Design"
    if any(token in haystack for token in ["gpu", "cpu", "numa", "hardware", "throughput", "latency", "kernel"]):
        return "Hardware-Conscious Execution"
    return "LLM Inference Systems"


def sanitize_line(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def support_dir(vault: Path, title: str, paper_id: str | None, note_id: str | None) -> Path:
    configured = os.environ.get("PHD_SKILL_WORK_ROOT", "").strip()
    if configured:
        base = Path(configured)
    else:
        local_appdata = os.environ.get("LOCALAPPDATA", "").strip()
        base = (Path(local_appdata) if local_appdata else Path.home() / "AppData" / "Local") / "phd-learning-skills" / "work"
    stem = build_note_stem(title, paper_id=paper_id, note_id=note_id)
    return base / stem


def ensure_assets_index(
    note: dict,
    paper: dict | None,
    cache: dict | None,
    resolution: dict | None,
    vault: Path = DEFAULT_VAULT,
) -> Path:
    title = (paper or {}).get("title") or note.get("title") or "Untitled Paper"
    paper_id = (paper or {}).get("id") or note.get("paper_id")
    note_id = note.get("id")
    target_dir = support_dir(vault, title, paper_id, note_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    assets_path = target_dir / "assets.md"

    lines = [
        "# PaperQuay Assets Index",
        "",
        f"- Title: {sanitize_line(title) or '待确认'}",
        f"- Paper ID: {sanitize_line(paper_id) or '待确认'}",
        f"- PaperQuay Note ID: {sanitize_line(note_id) or '待确认'}",
        f"- Source resolution: {sanitize_line((resolution or {}).get('strategy')) or '待确认'}",
        f"- Selected reasons: {', '.join((resolution or {}).get('selected_reasons') or []) or '待确认'}",
        f"- PDF: {attachment_pdf_path(paper) or '缺失'}",
        f"- MinerU Markdown: {str((cache or {}).get('full_md_path') or '缺失')}",
        f"- Content blocks: {str((cache or {}).get('content_json_path') or '缺失')}",
        f"- Layout JSON: {str((cache or {}).get('layout_json_path') or '缺失')}",
        f"- Images dir: {str((cache or {}).get('images_dir') or '缺失')}",
        f"- Translation Markdown: {find_translated_markdown(cache) or '缺失'}",
    ]
    assets_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return assets_path


def build_manifest_like(
    note: dict,
    paper: dict | None,
    cache: dict | None,
    resolution: dict | None,
    vault: Path = DEFAULT_VAULT,
) -> dict[str, Any]:
    title = (paper or {}).get("title") or note.get("title") or "Untitled Paper"
    assets_index = ensure_assets_index(note, paper, cache, resolution, vault)
    return {
        "paper_id": (paper or {}).get("id") or note.get("paper_id") or note.get("id") or "unknown-paper",
        "title": title,
        "authors": authors_to_string(paper),
        "year": str((paper or {}).get("year") or "待确认"),
        "venue": (paper or {}).get("publication") or "待确认",
        "domain": infer_domain(paper),
        "classification_reason": "PaperQuay note and MinerU cache matched through anchor-first paper resolution.",
        "source_url": (paper or {}).get("url") or "",
        "abstract": (paper or {}).get("abstract_text") or (paper or {}).get("ai_summary") or "",
        "pdf": attachment_pdf_path(paper),
        "mineru_md": str((cache or {}).get("full_md_path") or ""),
        "translated_md": find_translated_markdown(cache),
        "assets_index": str(assets_index),
        "asset_dir": str((cache or {}).get("cache_dir") or ""),
        "image_aliases": collect_image_aliases(cache),
        "created": str(note.get("created_at") or ""),
        "updated": str(note.get("updated_at") or ""),
        "paperquay_note_id": note.get("id"),
        "paperquay_cache_dir": (cache or {}).get("cache_dir"),
        "paperquay_resolution": resolution or {},
    }
