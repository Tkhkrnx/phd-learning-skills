from __future__ import annotations

import json
from typing import Any


def _text(node: dict[str, Any]) -> str:
    if node.get("type") == "text":
        return node.get("text", "")
    return "".join(_text(child) for child in node.get("content", []) or [])


def tiptap_to_markdown(content_json: Any) -> str:
    if not content_json:
        return ""
    if isinstance(content_json, str):
        try:
            content_json = json.loads(content_json)
        except Exception:
            return content_json
    lines: list[str] = []
    for node in content_json.get("content", []) or []:
        node_type = node.get("type")
        text = _text(node).strip()
        if not text:
            continue
        if node_type == "heading":
            level = int(node.get("attrs", {}).get("level", 1))
            lines.append(f"{'#' * max(1, min(level, 6))} {text}")
        elif node_type == "bulletList":
            for item in node.get("content", []) or []:
                item_text = _text(item).strip()
                if item_text:
                    lines.append(f"- {item_text}")
        elif node_type == "orderedList":
            idx = 1
            for item in node.get("content", []) or []:
                item_text = _text(item).strip()
                if item_text:
                    lines.append(f"{idx}. {item_text}")
                    idx += 1
        elif node_type == "blockquote":
            lines.append(f"> {text}")
        elif node_type == "noteAnchorBlock":
            label = node.get("attrs", {}).get("label", "文献摘录")
            lines.append(f"> [!quote] {label}")
            lines.append(f"> {text}")
        else:
            lines.append(text)
        lines.append("")
    return "\n".join(lines).strip() + "\n"
