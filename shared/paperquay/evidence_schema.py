from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def clip(text: str, limit: int = 420) -> str:
    text = normalize_space(text)
    if len(text) <= limit:
        return text
    window = text[:limit]
    cut = max(window.rfind("."), window.rfind(";"), window.rfind("。"), window.rfind("；"), window.rfind("，"))
    if cut >= int(limit * 0.55):
        return window[: cut + 1].strip()
    return window.strip()


def load_json(path: str | Path | None) -> Any:
    if not path:
        return None
    real_path = Path(path)
    if not real_path.exists():
        return None
    return json.loads(real_path.read_text(encoding="utf-8"))


def load_text(path: str | Path | None) -> str:
    if not path:
        return ""
    real_path = Path(path)
    if not real_path.exists():
        return ""
    return real_path.read_text(encoding="utf-8", errors="ignore")


def split_markdown_sections(text: str) -> list[dict[str, Any]]:
    source = text.replace("\r\n", "\n").replace("\r", "\n")
    pattern = re.compile(r"(?m)^(#{1,6})\s+([^\n]+)\n")
    matches = list(pattern.finditer(source))
    if not matches:
        body = normalize_space(source)
        return [{"heading": "document", "level": 0, "body": body, "index": 0}] if body else []
    sections: list[dict[str, Any]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(source)
        body = normalize_space(source[start:end])
        sections.append(
            {
                "heading": normalize_space(match.group(2)),
                "level": len(match.group(1)),
                "body": body,
                "index": idx,
            }
        )
    return sections


def _tokenize(text: str) -> list[str]:
    lowered = str(text or "").lower()
    english = re.findall(r"[a-z0-9][a-z0-9._/-]*", lowered)
    chinese = re.findall(r"[\u4e00-\u9fff]{2,}", lowered)
    return [token for token in [*english, *chinese] if len(token) >= 2]


def _counter(tokens: Iterable[str]) -> Counter[str]:
    return Counter(token for token in tokens if token)


def _heading_weight(heading: str) -> float:
    lowered = str(heading or "").lower()
    score = 0.0
    if any(
        token in lowered
        for token in [
            "introduction",
            "background",
            "preliminar",
            "motivation",
            "overview",
            "architecture",
            "method",
            "design",
            "approach",
            "implementation",
            "experiment",
            "evaluation",
            "analysis",
            "result",
            "discussion",
            "conclusion",
            "limitation",
        ]
    ):
        score += 1.0
    if any(
        token in lowered
        for token in ["appendix", "supplement", "counterexample", "proof", "acknowledg", "reference", "bibliography"]
    ):
        score -= 1.5
    if re.match(r"^[a-z]\.\s", lowered) or lowered.startswith("appendix"):
        score -= 0.8
    return score


def _best_matches(query: str, candidates: list[dict[str, Any]], text_key: str, top_k: int = 3) -> list[dict[str, Any]]:
    query_counter = _counter(_tokenize(query))
    ranked: list[tuple[float, dict[str, Any]]] = []
    for item in candidates:
        haystack = normalize_space(f"{item.get('heading', '')} {item.get(text_key, '')}")
        if not haystack:
            continue
        item_counter = _counter(_tokenize(haystack))
        overlap = sum(min(count, item_counter.get(token, 0)) for token, count in query_counter.items())
        if overlap <= 0:
            continue
        heading = str(item.get("heading", "")).lower()
        heading_bonus = 1.0 if any(token in heading for token in query_counter.keys()) else 0.0
        score = overlap + heading_bonus + _heading_weight(heading)
        if score <= 0:
            continue
        ranked.append((score, item))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in ranked[:top_k]]


def _prefer_main_paper_hits(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not items:
        return []
    preferred = [item for item in items if _heading_weight(str(item.get("heading") or "")) >= 0]
    return preferred or items


def extract_note_points(note_markdown: str, limit: int = 16) -> list[dict[str, str]]:
    lines = note_markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    points: list[dict[str, str]] = []
    current_heading = ""
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            current_heading = line.lstrip("#").strip()
            continue
        if line.startswith(("- ", "* ")):
            text = line[2:].strip()
        elif re.match(r"^\d+\.\s+", line):
            text = re.sub(r"^\d+\.\s+", "", line)
        elif line.startswith(">"):
            text = line.lstrip(">").strip()
        else:
            text = line
        text = normalize_space(text)
        if len(text) < 12:
            continue
        points.append({"heading": current_heading or "note", "text": text})
        if len(points) >= limit:
            break
    return points


def _extract_node_text(node: Any) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return " ".join(part for part in (_extract_node_text(item) for item in node) if part)
    if isinstance(node, dict):
        parts: list[str] = []
        for key in (
            "content",
            "text",
            "title_content",
            "paragraph_content",
            "table_caption",
            "image_caption",
            "chart_caption",
            "table_body",
            "img_caption",
            "algorithm_content",
            "equation_content",
        ):
            value = node.get(key)
            if value is None:
                continue
            parts.append(_extract_node_text(value))
        return normalize_space(" ".join(parts))
    return ""


def _extract_captions(node: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("image_caption", "table_caption", "chart_caption", "caption", "img_caption"):
        value = node.get("content", {}).get(key) if isinstance(node.get("content"), dict) else node.get(key)
        text = _extract_node_text(value)
        if text:
            parts.append(text)
    return normalize_space(" ".join(parts))


def flatten_content_list(payload: Any) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []

    def visit(node: Any, page_index: int | None = None) -> None:
        if isinstance(node, list):
            for item in node:
                visit(item, page_index=page_index)
            return
        if not isinstance(node, dict):
            return

        node_type = str(node.get("type") or "").strip().lower()
        if node_type and node_type != "page":
            content = node.get("content", {})
            flattened.append(
                {
                    "type": node_type,
                    "page": page_index,
                    "text": _extract_node_text(content),
                    "caption": _extract_captions(node),
                    "bbox": node.get("bbox"),
                    "image_path": (
                        content.get("img_path")
                        if isinstance(content, dict)
                        else None
                    )
                    or node.get("img_path"),
                }
            )

        next_page = page_index
        if node_type == "page":
            raw_page = node.get("page_idx") or node.get("page") or node.get("page_index")
            try:
                next_page = int(raw_page)
            except Exception:
                next_page = page_index

        for key in ("blocks", "items", "children", "content"):
            value = node.get(key)
            if isinstance(value, list):
                visit(value, page_index=next_page)

    visit(payload)
    results: list[dict[str, Any]] = []
    for index, item in enumerate(flattened):
        text = normalize_space(item.get("text") or "")
        caption = normalize_space(item.get("caption") or "")
        if not text and not caption and item.get("type") not in {"image", "table", "chart", "algorithm"}:
            continue
        item["index"] = index
        item["text"] = text
        item["caption"] = caption
        results.append(item)
    return results


def build_figure_index(full_md_text: str, blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    figures: list[dict[str, Any]] = []
    seen: set[str] = set()

    md_pattern = re.compile(
        r"(?is)(figure|table|algorithm)\s+(\d+[a-z]?)[:.]?\s*(.+?)(?=\n\s*(?:figure|table|algorithm)\s+\d+[a-z]?[:.]?|^##\s+|\Z)",
    )
    for match in md_pattern.finditer(full_md_text):
        key = f"{match.group(1).lower()}-{match.group(2).lower()}"
        if key in seen:
            continue
        seen.add(key)
        figures.append(
            {
                "kind": match.group(1).lower(),
                "number": match.group(2).lower(),
                "caption": clip(match.group(3), 260),
                "page": None,
                "image_path": None,
            }
        )

    for block in blocks:
        if block.get("type") not in {"image", "table", "chart", "algorithm"}:
            continue
        caption = block.get("caption") or block.get("text") or ""
        if not caption:
            continue
        matched = re.search(r"(?i)(figure|table|algorithm)\s+(\d+[a-z]?)", caption)
        key = (
            f"{matched.group(1).lower()}-{matched.group(2).lower()}"
            if matched
            else f"{block.get('type')}-{block.get('index')}"
        )
        if key in seen:
            continue
        seen.add(key)
        figures.append(
            {
                "kind": (matched.group(1).lower() if matched else str(block.get("type") or "")),
                "number": matched.group(2).lower() if matched else None,
                "caption": clip(caption, 260),
                "page": block.get("page"),
                "image_path": block.get("image_path"),
            }
        )
    return figures[:32]


def build_note_anchor_index(note: dict[str, Any]) -> list[dict[str, Any]]:
    raw = note.get("anchors")
    if not raw:
        return []
    try:
        anchors = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return []
    items: list[dict[str, Any]] = []
    for anchor in anchors if isinstance(anchors, list) else []:
        if not isinstance(anchor, dict):
            continue
        location = anchor.get("pdfLocation") or {}
        items.append(
            {
                "label": normalize_space(anchor.get("label") or ""),
                "excerpt": clip(anchor.get("excerpt") or "", 280),
                "page": location.get("pageNumber"),
                "paper_id": normalize_space(anchor.get("paperId") or anchor.get("workspaceId") or ""),
                "source_title": normalize_space(anchor.get("sourceTitle") or ""),
            }
        )
    return items


def compact_sections(sections: list[dict[str, Any]], limit: int = 12, body_limit: int = 420) -> list[dict[str, Any]]:
    return [
        {
            "heading": item["heading"],
            "level": item["level"],
            "index": item["index"],
            "snippet": clip(item["body"], body_limit),
        }
        for item in sections[:limit]
    ]


def _pick_sections(sections: list[dict[str, Any]], keywords: list[str], fallback: int = 4) -> list[dict[str, Any]]:
    selected = [
        item
        for item in sections
        if item.get("level", 0) >= 2 and any(keyword in item["heading"].lower() for keyword in keywords)
    ]
    selected.sort(key=lambda item: (_heading_weight(item["heading"]), -item["index"]), reverse=True)
    if selected:
        return compact_sections(selected, limit=fallback, body_limit=520)
    filtered = [item for item in sections if item.get("level", 0) >= 2]
    filtered.sort(key=lambda item: (_heading_weight(item["heading"]), -item["index"]), reverse=True)
    return compact_sections(filtered or sections, limit=fallback, body_limit=520)


def _pick_blocks(blocks: list[dict[str, Any]], keywords: list[str], limit: int = 8) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for block in blocks:
        haystack = f"{block.get('caption', '')} {block.get('text', '')}".lower()
        if any(keyword in haystack for keyword in keywords):
            output.append(
                {
                    "type": block.get("type"),
                    "page": block.get("page"),
                    "caption": clip(block.get("caption") or "", 260),
                    "snippet": clip(block.get("text") or "", 300),
                    "image_path": block.get("image_path"),
                }
            )
        if len(output) >= limit:
            break
    return output


def _pick_main_figures(figures: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    ranked: list[tuple[float, dict[str, Any]]] = []
    for index, item in enumerate(figures):
        caption = normalize_space(item.get("caption") or "")
        kind = str(item.get("kind") or "").lower()
        score = 0.0
        if kind == "table":
            score += 1.8
        if kind == "algorithm":
            score += 1.6
        if any(
            token in caption.lower()
            for token in [
                "overview",
                "framework",
                "architecture",
                "workflow",
                "pipeline",
                "main result",
                "overall",
                "ablation",
                "latency",
                "throughput",
                "acceptance",
                "online",
                "offline",
                "serving",
            ]
        ):
            score += 1.2
        if any(token in caption.lower() for token in ["appendix", "supplementary"]):
            score -= 1.5
        score += max(0.0, 0.4 - index * 0.03)
        ranked.append((score, item))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in ranked[:limit]]


def build_note_alignment(note_markdown: str, sections: list[dict[str, Any]], blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    section_candidates = [{"heading": s["heading"], "body": s["body"], "index": s["index"]} for s in sections]
    block_candidates = [{"heading": f"page {b.get('page')}", "body": f"{b.get('caption', '')} {b.get('text', '')}", "index": b["index"]} for b in blocks]
    aligned: list[dict[str, Any]] = []
    for point in extract_note_points(note_markdown):
        section_hits = _prefer_main_paper_hits(_best_matches(point["text"], section_candidates, "body", top_k=3))[:2]
        block_hits = _best_matches(point["text"], block_candidates, "body", top_k=2)
        aligned.append(
            {
                "note_heading": point["heading"],
                "note_text": point["text"],
                "section_evidence": [
                    {"heading": item["heading"], "snippet": clip(item["body"], 260), "index": item["index"]}
                    for item in section_hits
                ],
                "block_evidence": [
                    {"anchor": item["heading"], "snippet": clip(item["body"], 220), "index": item["index"]}
                    for item in block_hits
                ],
            }
        )
    return aligned


def build_paperquay_evidence_bundle(
    note: dict[str, Any],
    paper: dict[str, Any] | None,
    cache: dict[str, Any] | None,
    note_markdown: str,
) -> dict[str, Any]:
    full_md_text = load_text((cache or {}).get("full_md_path"))
    content_payload = load_json((cache or {}).get("content_json_path"))
    sections = split_markdown_sections(full_md_text)
    blocks = flatten_content_list(content_payload)
    figures = build_figure_index(full_md_text, blocks)
    note_alignment = build_note_alignment(note_markdown, sections, blocks)
    method_keywords = [
        "method",
        "design",
        "architecture",
        "framework",
        "algorithm",
        "system",
        "pipeline",
        "workflow",
        "scheduler",
        "verification",
        "decode",
        "decoding",
        "execution",
        "implementation",
    ]
    experiment_keywords = [
        "experiment",
        "evaluation",
        "result",
        "analysis",
        "latency",
        "throughput",
        "ablation",
        "benchmark",
        "serving",
        "deployment",
        "online",
        "offline",
        "performance",
    ]
    related_keywords = ["related work", "background", "motivation", "preliminar", "challenge"]
    gap_keywords = ["limitation", "discussion", "conclusion", "future work", "failure", "threat", "boundary"]
    return {
        "metadata": {
            "paper_id": (paper or {}).get("id") or note.get("paper_id"),
            "title": (paper or {}).get("title") or note.get("title"),
            "authors": [item.get("name") for item in ((paper or {}).get("authors") or []) if item.get("name")],
            "year": (paper or {}).get("year"),
            "venue": (paper or {}).get("publication"),
            "abstract": clip((paper or {}).get("abstract_text") or (paper or {}).get("ai_summary") or "", 5000),
            "paper_url": (paper or {}).get("url"),
            "note_id": note.get("id"),
        },
        "full_md_path": (cache or {}).get("full_md_path"),
        "content_json_path": (cache or {}).get("content_json_path"),
        "cache_dir": (cache or {}).get("cache_dir"),
        "note_anchor_index": build_note_anchor_index(note),
        "note_alignment": note_alignment,
        "section_index": compact_sections(sections, limit=20, body_limit=360),
        "method_sections": _pick_sections(sections, method_keywords, fallback=6),
        "experiment_sections": _pick_sections(sections, experiment_keywords, fallback=6),
        "related_sections": _pick_sections(sections, related_keywords, fallback=4),
        "gap_sections": _pick_sections(sections, gap_keywords, fallback=4),
        "method_blocks": _pick_blocks(blocks, method_keywords, limit=10),
        "experiment_blocks": _pick_blocks(blocks, experiment_keywords, limit=10),
        "figure_index": figures,
        "main_figures": _pick_main_figures(figures, limit=8),
        "block_stats": {
            "total_blocks": len(blocks),
            "image_like_blocks": sum(1 for block in blocks if block.get("type") in {"image", "table", "chart", "algorithm"}),
        },
    }
