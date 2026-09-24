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
    "Experimental Setup and Figure/Table Map",
    "Writing and Presentation Details",
    "What is the takeaway?",
]

REVIEW_ANALYSIS_HEADINGS = [
    "Problem Definition",
    "Why It Matters",
    "Existing Work",
    "Key Idea",
    "Experiment Plan",
    "Experimental Setup and Figure/Table Map",
    "Writing and Presentation Details",
    "Overall Assessment",
]

REVIEW_HEADINGS = [
    "Summary and High Level Discussion",
    "Strengths",
    "Weaknesses",
    "Comments for Rebuttal",
    "Detailed Comments for Authors",
    "Overall Recommendation",
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
    matches = list(re.finditer(r"(?m)^(#{2,4})\s+(.+?)\s*$", text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        level = len(match.group(1))
        next_sibling = next(
            (
                candidate
                for candidate in matches[index + 1 :]
                if len(candidate.group(1)) <= level
            ),
            None,
        )
        end = next_sibling.start() if next_sibling else len(text)
        sections.append((match.group(2), text[match.end() : end]))
    return sections


def _recommendation(text: str, kind: str) -> str:
    overall = "Overall Assessment" if kind == "review-analysis" else "Overall Recommendation"
    relevant = next(
        (body for heading, body in _heading_bodies(text) if overall.casefold() in heading.casefold()),
        "",
    )
    labels = (
        (r"(?i)\brating\s*:?\s*6\b|\bmarginally\s+above\s+acceptance\s+threshold\b", "weak accept"),
        (r"(?i)\bstrong\s+accept\b|强接收", "strong accept"),
        (r"(?i)\bweak\s+accept\b|弱接收", "weak accept"),
        (r"(?i)\bborderline\b|边缘", "borderline"),
        (r"(?i)\bweak\s+reject\b|弱拒", "weak reject"),
        (r"(?i)\bstrong\s+reject\b|强拒", "strong reject"),
        (r"(?i)\baccept\b|接收", "accept"),
        (r"(?i)\breject\b|拒绝", "reject"),
    )
    return next((canonical for pattern, canonical in labels if re.search(pattern, relevant)), "")


def validate_review_pair(analysis_text: str, formal_text: str) -> dict[str, Any]:
    analysis_recommendation = _recommendation(analysis_text, "review-analysis")
    formal_recommendation = _recommendation(formal_text, "review")
    errors: list[str] = []
    if not analysis_recommendation or not formal_recommendation:
        errors.append("both review artifacts need a recognizable overall recommendation")
    elif analysis_recommendation != formal_recommendation:
        errors.append(
            f"review recommendation mismatch: {analysis_recommendation} != {formal_recommendation}"
        )
    return {
        "status": "passed" if not errors else "failed",
        "analysis_recommendation": analysis_recommendation,
        "formal_recommendation": formal_recommendation,
        "errors": errors,
        "warnings": ["manually compare finding severity, evidence, and requested fixes"],
    }


def validate_note_text(
    text: str,
    kind: str,
    expected_title: str,
    original_text: str = "",
    forbid_terms: list[str] | None = None,
    expected_paper_id: str = "",
    venue_format: bool = False,
) -> dict[str, Any]:
    if kind not in {"reading", "review-analysis", "review"}:
        raise ValueError(f"Unknown kind: {kind}")
    errors: list[str] = []
    warnings: list[str] = []
    headings = _heading_bodies(text)
    required = {
        "reading": READING_HEADINGS,
        "review-analysis": REVIEW_ANALYSIS_HEADINGS,
        "review": REVIEW_HEADINGS,
    }[kind]

    if not normalize(text):
        errors.append("deliverable is empty")
    if not headings:
        errors.append("deliverable has no substantive sections")
    for marker in SCAFFOLD_MARKERS:
        if marker.lower() in text.lower():
            errors.append(f"scaffold marker remains: {marker}")
    if not venue_format or kind == "reading":
        required_positions: list[int] = []
        for marker in required:
            matching = [
                (position, heading, body)
                for position, (heading, body) in enumerate(headings)
                if marker.casefold() in heading.casefold()
            ]
            if not matching:
                errors.append(f"missing required heading: {marker}")
            elif all(len(normalize(body)) < 30 for _, _, body in matching):
                errors.append(f"section lacks an answer: {marker}")
            else:
                required_positions.append(matching[0][0])
        if len(required_positions) == len(required) and required_positions != sorted(required_positions):
            errors.append("required sections are not in the prescribed presentation order")

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
    parser.add_argument("--kind", choices=["reading", "review-analysis", "review"], required=True)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--expected-title", required=True)
    parser.add_argument("--expected-paper-id", default="")
    parser.add_argument("--original", type=Path)
    parser.add_argument("--forbid-term", action="append", default=[])
    parser.add_argument("--venue-format", action="store_true")
    parser.add_argument("--companion", type=Path, help="Five-question analysis note paired with a formal review")
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
    if args.companion:
        if args.kind != "review":
            report["errors"].append("--companion applies only to a formal review")
        elif not args.companion.is_file():
            report["errors"].append(f"companion analysis note does not exist: {args.companion}")
        else:
            analysis = args.companion.read_text(encoding="utf-8-sig")
            analysis_report = validate_note_text(analysis, "review-analysis", args.expected_title)
            report["errors"].extend(f"companion: {error}" for error in analysis_report["errors"])
            formal = args.path.read_text(encoding="utf-8-sig") if args.path.is_file() else ""
            pair = validate_review_pair(analysis, formal)
            report["errors"].extend(pair["errors"])
            report["warnings"].extend(pair["warnings"])
            report["companion"] = str(args.companion)
            report["recommendation_pair"] = [
                pair["analysis_recommendation"], pair["formal_recommendation"]
            ]
        report["status"] = "passed" if not report["errors"] else "failed"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
