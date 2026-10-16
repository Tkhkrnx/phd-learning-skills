"""Read-only PPTX template selection: explicit template, existing deck, bundled default."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET

from audit_deck import ordered_slides


SKILL_ROOT = Path(__file__).resolve().parents[1]


def inspect_pptx(path: Path) -> dict:
    path = path.expanduser().resolve(strict=True)
    if path.suffix.lower() != ".pptx":
        raise ValueError(f"Expected a PPTX file: {path}")
    with ZipFile(path) as archive:
        broken = archive.testzip()
        if broken:
            raise ValueError(f"Corrupt PPTX member: {broken}")
        slides, size = ordered_slides(archive)
        if not slides:
            raise ValueError(f"PPTX has no slides: {path}")
        for part in slides:
            ET.fromstring(archive.read(part))
    return {
        "path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "slide_count": len(slides),
        "slide_size_emu": list(size),
    }


def resolve_template(template: Path | None = None, existing_deck: Path | None = None,
                     *, skill_root: Path = SKILL_ROOT) -> dict:
    existing = inspect_pptx(existing_deck) if existing_deck is not None else None
    if template is not None:
        selected, origin = inspect_pptx(template), "user-template"
    elif existing is not None:
        selected, origin = existing, "existing-deck"
    else:
        manifest = json.loads((skill_root / "assets/batchgen-template.json").read_text(encoding="utf-8"))
        selected = inspect_pptx(skill_root / "assets" / manifest["reference_file"])
        for key in ("sha256", "slide_count", "slide_size_emu"):
            if selected[key] != manifest[key]:
                raise ValueError(f"Bundled template {key} differs from its manifest")
        origin = "bundled-default"
    result = {
        "selection": origin,
        "template": selected,
        "existing_deck": existing,
        "requires_reference_content_replacement": origin == "bundled-default",
        "evidence_limit": "Template selection and package checks only; no authoring or visual verification.",
    }
    if origin == "bundled-default":
        result["reference_pages"] = manifest["reference_pages"]
        result["usage_guide"] = str((skill_root / "references/default-template.md").resolve())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, help="An explicitly selected new style template")
    parser.add_argument("--existing-deck", type=Path, help="The existing talk being continued")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        result = resolve_template(args.template, args.existing_deck)
    except (OSError, ValueError, KeyError, ET.ParseError, BadZipFile) as exc:
        print(json.dumps({"status": "failed", "errors": [str(exc)]}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "passed", **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
