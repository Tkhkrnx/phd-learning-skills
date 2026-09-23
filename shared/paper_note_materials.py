from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import BadZipFile, ZipFile


PRESENTATION_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
RELATIONSHIP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_RELATIONSHIP_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def file_record(path: Path) -> dict[str, object]:
    resolved = path.resolve(strict=True)
    if not resolved.is_file():
        raise ValueError(f"Not a file: {resolved}")
    digest = hashlib.sha256()
    with resolved.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"path": str(resolved), "size": resolved.stat().st_size, "sha256": digest.hexdigest()}


def markdown_record(path: Path) -> dict[str, object]:
    record = file_record(path)
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError(f"Expected a Markdown note: {path}")
    source = path.read_text(encoding="utf-8-sig")
    record["headings"] = re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", source)
    record["characters"] = len(source)
    return record


def _texts(xml: bytes) -> str:
    root = ET.fromstring(xml)
    return " ".join(
        node.text.strip()
        for node in root.iter(f"{{{DRAWING_NS}}}t")
        if node.text and node.text.strip()
    )


def _relationships(archive: ZipFile, path: str) -> dict[str, tuple[str, str]]:
    try:
        root = ET.fromstring(archive.read(path))
    except KeyError:
        return {}
    return {
        node.attrib["Id"]: (node.attrib["Target"], node.attrib.get("Type", ""))
        for node in root.iter(f"{{{PACKAGE_RELATIONSHIP_NS}}}Relationship")
    }


def pptx_record(path: Path) -> dict[str, object]:
    record = file_record(path)
    if path.suffix.lower() != ".pptx":
        raise ValueError(f"Expected a PowerPoint .pptx: {path}")
    slides: list[dict[str, object]] = []
    with ZipFile(path) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        relationships = _relationships(archive, "ppt/_rels/presentation.xml.rels")
        slide_ids = presentation.find(f"{{{PRESENTATION_NS}}}sldIdLst")
        if slide_ids is None:
            raise ValueError(f"No slide list found: {path}")
        for number, slide_id in enumerate(slide_ids, 1):
            rid = slide_id.attrib[f"{{{RELATIONSHIP_NS}}}id"]
            target, _ = relationships[rid]
            slide_path = (
                target.lstrip("/") if target.startswith("/ppt/")
                else posixpath.normpath(posixpath.join("ppt", target))
            )
            slide = {"number": number, "text": _texts(archive.read(slide_path))}
            slide_rels_path = posixpath.join(
                posixpath.dirname(slide_path), "_rels", posixpath.basename(slide_path) + ".rels"
            )
            for note_target, relation_type in _relationships(archive, slide_rels_path).values():
                if relation_type.endswith("/notesSlide"):
                    note_path = posixpath.normpath(
                        posixpath.join(posixpath.dirname(slide_path), note_target)
                    )
                    slide["speaker_notes"] = _texts(archive.read(note_path))
                    break
            slides.append(slide)
    record["slides"] = slides
    record["visual_review_required"] = True
    return record


def collect_materials(
    kind: str,
    paper: Path | None = None,
    note: Path | None = None,
    pptx: Path | None = None,
) -> dict[str, object]:
    if kind not in {"reading", "review"}:
        raise ValueError(f"Unknown kind: {kind}")
    if not any((paper, note, pptx)):
        raise ValueError("Provide a paper, Markdown note, or PPTX")
    result: dict[str, object] = {"kind": kind, "paper": None, "note": None, "pptx": None}
    if paper:
        if paper.suffix.lower() not in {".pdf", ".md", ".markdown"}:
            raise ValueError(f"Paper must be PDF or Markdown: {paper}")
        result["paper"] = markdown_record(paper) if paper.suffix.lower() != ".pdf" else file_record(paper)
    if note:
        result["note"] = markdown_record(note)
    if pptx:
        result["pptx"] = pptx_record(pptx)
    result["paper_source_available"] = paper is not None
    return result


def main(kind: str) -> int:
    parser = argparse.ArgumentParser(description="Inventory paper, optional Markdown note, and PPTX")
    parser.add_argument("--paper", type=Path, help="Source paper PDF or full-text Markdown")
    parser.add_argument("--note", type=Path, help="Optional user-authored Markdown note")
    parser.add_argument("--pptx", type=Path, help="Optional user-authored presentation")
    args = parser.parse_args()
    try:
        result = collect_materials(kind, args.paper, args.note, args.pptx)
    except (ValueError, OSError, KeyError, ET.ParseError, BadZipFile) as exc:
        print(f"Material inventory failed: {exc}", file=sys.stderr)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
