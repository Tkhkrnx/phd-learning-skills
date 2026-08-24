from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SCAFFOLD_MARKERS = [
    "写作提示：",
    "这是写给当前主模型",
    "这是给当前主模型",
    "当前版本先保证映射正确",
    "Source note draft",
    "原始导入稿",
]

READING_HEADINGS = [
    "What is the problem?",
    "Why it matters?",
    "Why existing works fail?",
    "What is the key idea?",
    "What is the design?",
    "What is the experimental plan?",
    "What is the takeaway?",
    "你当前笔记的遗漏与纠偏",
]

REVIEW_HEADINGS = [
    "Summary and High Level Discussion",
    "Strengths",
    "Weaknesses",
    "Comments for Rebuttal",
    "Detailed Comments for Authors",
    "Scored Review Questions",
    "Reproducibility",
    "Confidential Comments to the Program Committee",
    "你当前审稿笔记的遗漏与纠偏",
]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def frontmatter_value(text: str, key: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, flags=re.DOTALL)
    if not match:
        return ""
    field = re.search(rf"(?mi)^{re.escape(key)}\s*:\s*(.+?)\s*$", match.group(1))
    return field.group(1).strip().strip("\"'") if field else ""


def validate_note_text(
    text: str,
    kind: str,
    expected_title: str,
    original_text: str = "",
    forbid_terms: list[str] | None = None,
    expected_paper_id: str = "",
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    required = READING_HEADINGS if kind == "reading" else REVIEW_HEADINGS
    minimum_chars = 5000 if kind == "reading" else 4500
    compact = normalize(text)

    if len(compact) < minimum_chars:
        errors.append(f"final note is too short: {len(compact)} < {minimum_chars}")
    for heading in required:
        if heading not in text:
            errors.append(f"missing required heading: {heading}")
    for marker in SCAFFOLD_MARKERS:
        if marker in text:
            errors.append(f"scaffold marker remains: {marker}")
    title_terms = [token.lower() for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9-]*", expected_title) if len(token) > 2]
    if title_terms and not any(term in text.lower() for term in title_terms[:4]):
        errors.append("expected paper title is not represented in final note")
    actual_paper_id = frontmatter_value(text, "paper_id")
    if expected_paper_id and actual_paper_id != expected_paper_id:
        errors.append(f"frontmatter paper_id mismatch: {actual_paper_id or '<missing>'} != {expected_paper_id}")
    for term in forbid_terms or []:
        if term and term.lower() in text.lower():
            errors.append(f"forbidden cross-paper term found: {term}")
    evidence_hits = len(re.findall(r"(?i)(?:正文\s*§|§\s*\d|figure\s*\d|table\s*\d|algorithm\s*\d|图\s*\d|表\s*\d)", text))
    if evidence_hits < 6:
        errors.append(f"too few evidence anchors: {evidence_hits} < 6")
    if original_text:
        source = normalize(original_text)
        for start in range(0, max(0, len(source) - 600), 600):
            fragment = source[start : start + 600]
            if len(fragment) >= 500 and fragment in compact:
                errors.append("large verbatim block copied from original note")
                break
    return {
        "status": "passed" if not errors else "failed",
        "kind": kind,
        "characters": len(compact),
        "evidence_anchors": evidence_hits,
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
) -> dict[str, Any]:
    if not path.is_file():
        return {"status": "failed", "errors": [f"final note does not exist: {path}"], "warnings": []}
    original_text = original.read_text(encoding="utf-8", errors="ignore") if original and original.is_file() else ""
    return validate_note_text(
        path.read_text(encoding="utf-8", errors="ignore"),
        kind,
        expected_title,
        original_text,
        forbid_terms,
        expected_paper_id,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["reading", "review"], required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--expected-title", required=True)
    parser.add_argument("--expected-paper-id", default="")
    parser.add_argument("--original")
    parser.add_argument("--forbid-term", action="append", default=[])
    args = parser.parse_args()
    report = validate_note_file(
        Path(args.path),
        args.kind,
        args.expected_title,
        Path(args.original) if args.original else None,
        args.forbid_term,
        args.expected_paper_id,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("status") == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
