"""Read-only checks for an explicitly declared PPTX editing contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import BadZipFile, ZipFile


P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def resolve_part(owner: str, target: str) -> str:
    return target.lstrip("/") if target.startswith("/") else posixpath.normpath(
        posixpath.join(posixpath.dirname(owner), target)
    )


def relationships(archive: ZipFile, owner: str) -> list[dict[str, str]]:
    path = posixpath.join(posixpath.dirname(owner), "_rels", posixpath.basename(owner) + ".rels")
    if path not in archive.namelist():
        return []
    return [dict(node.attrib) for node in ET.fromstring(archive.read(path))
            if node.tag == f"{{{PKG}}}Relationship"]


def paragraph_text(root: ET.Element) -> str:
    return "\n".join("".join(t.text or "" for t in paragraph.iter(f"{{{A}}}t"))
                     for paragraph in root.iter(f"{{{A}}}p"))


def ordered_slides(archive: ZipFile) -> tuple[list[str], tuple[int, int]]:
    owner = "ppt/presentation.xml"
    root = ET.fromstring(archive.read(owner))
    rels = {rel["Id"]: rel for rel in relationships(archive, owner)}
    slide_ids = root.find(f"{{{P}}}sldIdLst")
    if slide_ids is None:
        raise ValueError("Presentation has no slide list")
    parts = []
    for item in slide_ids:
        rel = rels[item.attrib[f"{{{R}}}id"]]
        if rel.get("TargetMode") == "External" or not rel["Type"].endswith("/slide"):
            raise ValueError("Slide list contains an invalid relationship")
        part = resolve_part(owner, rel["Target"])
        archive.getinfo(part)
        parts.append(part)
    size = root.find(f"{{{P}}}sldSz")
    if size is None:
        raise ValueError("Presentation has no slide dimensions")
    return parts, (int(size.attrib["cx"]), int(size.attrib["cy"]))


def part_digest(archive: ZipFile, part: str) -> str:
    value = archive.read(part)
    if part.endswith((".xml", ".rels")):
        # Namespace prefixes and attribute ordering can change on export without
        # changing the slide. Preserve text/coordinates while normalizing XML.
        value = ET.canonicalize(value, rewrite_prefixes=True).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def protected_signature(archive: ZipFile, part: str) -> tuple[str, tuple]:
    """Normalized slide XML and direct dependencies, excluding removable notes."""
    digest = part_digest(archive, part)
    dependencies = []
    for rel in relationships(archive, part):
        if rel["Type"].endswith("/notesSlide"):
            continue
        external = rel.get("TargetMode") == "External"
        identity = rel["Target"] if external else part_digest(archive, resolve_part(part, rel["Target"]))
        dependencies.append((rel["Id"], rel["Type"], external, identity))
    return digest, tuple(sorted(dependencies))


def audit_deck(
    deck: Path,
    source: Path | None = None,
    preserve: list[tuple[int, int]] | None = None,
    expected_count: int | None = None,
    no_notes: bool = False,
    forbidden: list[str] | None = None,
    required: list[str] | None = None,
) -> dict:
    errors: list[str] = []
    with ZipFile(deck) as archive:
        slides, size = ordered_slides(archive)
        texts = [paragraph_text(ET.fromstring(archive.read(part))) for part in slides]
        if expected_count is not None and len(slides) != expected_count:
            errors.append(f"Expected {expected_count} slides, found {len(slides)}")
        for term in forbidden or []:
            hits = [i for i, text in enumerate(texts, 1) if term.casefold() in text.casefold()]
            if hits:
                errors.append(f"Forbidden slide text {term!r} on pages {hits}")
        all_text = "\n".join(texts)
        for term in required or []:
            if term not in all_text:
                errors.append(f"Required slide text missing: {term!r}")
        notes_pages = []
        for index, part in enumerate(slides, 1):
            for rel in relationships(archive, part):
                if not rel["Type"].endswith("/notesSlide"):
                    continue
                note = ET.fromstring(archive.read(resolve_part(part, rel["Target"])))
                for shape in note.iter(f"{{{P}}}sp"):
                    placeholder = shape.find(f".//{{{P}}}ph")
                    if placeholder is not None and placeholder.get("type") == "sldNum":
                        continue
                    if paragraph_text(shape).strip():
                        notes_pages.append(index)
                        break
        if no_notes and notes_pages:
            errors.append(f"Speaker note text remains on pages {sorted(set(notes_pages))}")
        if preserve and source is None:
            raise ValueError("Protected page mappings require --source")
        if source is not None:
            with ZipFile(source) as original:
                source_slides, source_size = ordered_slides(original)
                if source_size != size:
                    errors.append(f"Source slide dimensions changed: {source_size} -> {size}")
                for before, after in preserve or []:
                    if not (1 <= before <= len(source_slides) and 1 <= after <= len(slides)):
                        errors.append(f"Protected page mapping outside slide range: {before}:{after}")
                    elif protected_signature(original, source_slides[before - 1]) != protected_signature(
                        archive, slides[after - 1]
                    ):
                        errors.append(f"Protected slide parts differ: {before}:{after}; inspect the change")
    return {
        "status": "failed" if errors else "passed",
        "slide_count": len(slides),
        "slide_size_emu": size,
        "pages_with_note_text": sorted(set(notes_pages)),
        "protected_mappings_checked": len(preserve or []),
        "errors": errors,
        "evidence_limit": "Static slide-contract checks only; no source interpretation, rendering, "
                          "full master/theme comparison or native PowerPoint verification.",
    }


def page_pair(value: str) -> tuple[int, int]:
    try:
        before, after = map(int, value.split(":"))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use SOURCE:OUTPUT one-based page numbers") from exc
    if before < 1 or after < 1:
        raise argparse.ArgumentTypeError("Page numbers must be positive")
    return before, after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--preserve", type=page_pair, action="append", default=[])
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--no-notes", action="store_true")
    parser.add_argument("--forbid-text", action="append", default=[])
    parser.add_argument("--require-text", action="append", default=[])
    args = parser.parse_args()
    try:
        result = audit_deck(args.deck, args.source, args.preserve, args.expected_count,
                            args.no_notes, args.forbid_text, args.require_text)
    except (OSError, ValueError, KeyError, ET.ParseError, BadZipFile) as exc:
        result = {"status": "failed", "errors": [str(exc)]}
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
