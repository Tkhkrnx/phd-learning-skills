from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


READING_HEADINGS = [
    "What is the problem?",
    "Why it matters?",
    "Why existing works fail?",
    "What is the key idea?",
    "What is the design?",
    "What is the experimental plan?",
    "What is the takeaway?",
]

REVIEW_HEADINGS = [
    "Problem Definition",
    "Why It Matters",
    "Existing Work",
    "Key Idea and Design",
    "Experimental Support",
    "Writing and Presentation Details",
    "Overall Assessment",
]

SCAFFOLD_MARKERS = (
    "写作提示：",
    "这是写给当前主模型",
    "这是给当前主模型",
    "Source note draft",
    "TODO",
    "TBD",
)


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def frontmatter_value(text: str, key: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, flags=re.DOTALL)
    if not match:
        return ""
    field = re.search(rf"(?mi)^{re.escape(key)}\s*:\s*(.+?)\s*$", match.group(1))
    return field.group(1).strip().strip("\"'") if field else ""


def _heading_bodies(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^#{2,4}\s+(.+?)\s*$", text))
    return [
        (match.group(1), text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)])
        for index, match in enumerate(matches)
    ]


def validate_note_text(
    text: str,
    kind: str,
    expected_title: str,
    original_text: str = "",
    forbid_terms: list[str] | None = None,
    expected_paper_id: str = "",
    venue_format: bool = False,
) -> dict[str, Any]:
    if kind not in {"reading", "review"}:
        raise ValueError(f"Unknown kind: {kind}")
    errors: list[str] = []
    warnings: list[str] = []
    headings = _heading_bodies(text)
    required = READING_HEADINGS if kind == "reading" else REVIEW_HEADINGS

    if not normalize(text):
        errors.append("deliverable is empty")
    if not headings:
        errors.append("deliverable has no substantive sections")
    for marker in SCAFFOLD_MARKERS:
        if marker.lower() in text.lower():
            errors.append(f"scaffold marker remains: {marker}")
    if not venue_format or kind == "reading":
        for marker in required:
            matching = [(heading, body) for heading, body in headings if marker.casefold() in heading.casefold()]
            if not matching:
                errors.append(f"missing required heading: {marker}")
            elif all(len(normalize(body)) < 30 for _, body in matching):
                errors.append(f"section lacks an answer: {marker}")

    title_terms = [term.casefold() for term in re.findall(r"[A-Za-z0-9][A-Za-z0-9-]*", expected_title) if len(term) > 2]
    if title_terms and not any(term in text.casefold() for term in title_terms[:4]):
        errors.append("expected paper title is not represented in deliverable")
    actual_paper_id = frontmatter_value(text, "paper_id")
    if expected_paper_id and actual_paper_id != expected_paper_id:
        errors.append(f"frontmatter paper_id mismatch: {actual_paper_id or '<missing>'} != {expected_paper_id}")
    for term in forbid_terms or []:
        if term and term.casefold() in text.casefold():
            errors.append(f"forbidden cross-paper term found: {term}")

    if not original_text and re.search(r"原笔记表述|原审稿笔记|你原来(认为|写道|误以为)", text):
        errors.append("claims about a user's prior note without a supplied note")
    if kind == "review" and re.search(r"你当前.*(笔记|审稿).*纠偏", text):
        errors.append("private correction ledger appears in formal review")

    anchors = len(re.findall(r"(?i)(?:§\s*\d|figure\s*\d|table\s*\d|algorithm\s*\d|图\s*\d|表\s*\d|p\.\s*\d)", text))
    if anchors < 3:
        warnings.append(f"few inspectable paper anchors: {anchors}; verify the evidence manually")

    return {
        "status": "passed" if not errors else "failed",
        "kind": kind,
        "characters": len(normalize(text)),
        "evidence_anchors": anchors,
        "errors": errors,
        "warnings": warnings,
    }


def validate_note_file(
    path: Path,
    kind: str,
    expected_title: str,
    original: Path | None = None,
    forbid_terms: list[str] | None = None,
    expected_paper_id: str = "",
    venue_format: bool = False,
) -> dict[str, Any]:
    if not path.is_file():
        return {"status": "failed", "errors": [f"deliverable does not exist: {path}"], "warnings": []}
    original_text = original.read_text(encoding="utf-8-sig") if original and original.is_file() else ""
    return validate_note_text(
        path.read_text(encoding="utf-8-sig"),
        kind,
        expected_title,
        original_text,
        forbid_terms,
        expected_paper_id,
        venue_format,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["reading", "review"], required=True)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--expected-title", required=True)
    parser.add_argument("--expected-paper-id", default="")
    parser.add_argument("--original", type=Path)
    parser.add_argument("--forbid-term", action="append", default=[])
    parser.add_argument("--venue-format", action="store_true")
    args = parser.parse_args()
    report = validate_note_file(
        args.path,
        args.kind,
        args.expected_title,
        args.original,
        args.forbid_term,
        args.expected_paper_id,
        args.venue_format,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
