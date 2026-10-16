from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "paper-presentation-builder/scripts/audit_deck.py"
SPEC = importlib.util.spec_from_file_location("paper_deck_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
TEMPLATE_SPEC = importlib.util.spec_from_file_location("paper_template_resolver", SCRIPT.with_name("resolve_template.py"))
TEMPLATE = importlib.util.module_from_spec(TEMPLATE_SPEC)
with patch.dict(sys.modules, {"audit_deck": MODULE}):
    TEMPLATE_SPEC.loader.exec_module(TEMPLATE)


def fixture(path: Path, *, image: bytes = b"image", note: bool = False, heading: str = "问题二"):
    p, a, r, pkg = MODULE.P, MODULE.A, MODULE.R, MODULE.PKG
    with ZipFile(path, "w") as archive:
        archive.writestr("ppt/presentation.xml", f'<p:presentation xmlns:p="{p}" xmlns:r="{r}">'
                         '<p:sldIdLst><p:sldId id="256" r:id="rId3"/>'
                         '<p:sldId id="257" r:id="rId1"/></p:sldIdLst>'
                         '<p:sldSz cx="12192000" cy="6858000"/></p:presentation>')
        archive.writestr("ppt/_rels/presentation.xml.rels", f'<Relationships xmlns="{pkg}">'
                         f'<Relationship Id="rId1" Type="{r}/slide" Target="slides/slide1.xml"/>'
                         f'<Relationship Id="rId3" Type="{r}/slide" Target="/ppt/slides/slide3.xml"/>'
                         '</Relationships>')
        for part, text in [(1, heading), (3, "Finished slide")]:
            archive.writestr(f"ppt/slides/slide{part}.xml",
                             f'<p:sld xmlns:p="{p}" xmlns:a="{a}"><a:p><a:r><a:t>{text}'
                             '</a:t></a:r></a:p></p:sld>')
        notes_rel = (f'<Relationship Id="rNotes" Type="{r}/notesSlide" '
                     'Target="/ppt/notesSlides/notesSlide1.xml"/>') if note else ""
        archive.writestr("ppt/slides/_rels/slide3.xml.rels", f'<Relationships xmlns="{pkg}">'
                         f'<Relationship Id="rImage" Type="{r}/image" '
                         f'Target="../media/image1.png"/>{notes_rel}</Relationships>')
        archive.writestr("ppt/media/image1.png", image)
        if note:
            archive.writestr("ppt/notesSlides/notesSlide1.xml",
                             f'<p:notes xmlns:p="{p}" xmlns:a="{a}"><p:sp><a:p>'
                             '<a:r><a:t>Hidden explanation</a:t></a:r></a:p></p:sp></p:notes>')


class PaperPresentationContractTests(unittest.TestCase):
    def test_bundled_template_is_the_pinned_complete_reference(self):
        result = TEMPLATE.resolve_template()
        self.assertEqual("bundled-default", result["selection"])
        self.assertTrue(result["requires_reference_content_replacement"])
        self.assertEqual(20, result["template"]["slide_count"])
        self.assertEqual([12192000, 6858000], result["template"]["slide_size_emu"])
        self.assertEqual([4], result["reference_pages"]["prior_work"])
        manifest = json.loads((TEMPLATE.SKILL_ROOT / "assets/batchgen-template.json").read_text(encoding="utf-8"))
        preview = TEMPLATE.SKILL_ROOT / "assets" / manifest["preview_file"]
        self.assertTrue(preview.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual("passed", MODULE.audit_deck(Path(result["template"]["path"]), no_notes=True)["status"])

    def test_explicit_template_overrides_existing_deck_and_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            custom, existing = Path(tmp) / "custom.pptx", Path(tmp) / "existing.pptx"
            fixture(custom, heading="New template")
            fixture(existing, heading="Existing work")
            before = custom.read_bytes(), existing.read_bytes()
            result = TEMPLATE.resolve_template(custom, existing, skill_root=Path(tmp) / "no-default")
            self.assertEqual("user-template", result["selection"])
            self.assertEqual(str(custom.resolve()), result["template"]["path"])
            self.assertEqual(str(existing.resolve()), result["existing_deck"]["path"])
            self.assertFalse(result["requires_reference_content_replacement"])
            self.assertEqual(before, (custom.read_bytes(), existing.read_bytes()))

    def test_existing_deck_is_not_reset_to_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "existing.pptx"
            fixture(existing)
            result = TEMPLATE.resolve_template(existing_deck=existing, skill_root=Path(tmp) / "no-default")
            self.assertEqual("existing-deck", result["selection"])
            self.assertEqual(str(existing.resolve()), result["template"]["path"])

    def test_invalid_user_input_never_silently_falls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing, corrupt = Path(tmp) / "missing.pptx", Path(tmp) / "corrupt.pptx"
            with self.assertRaises(FileNotFoundError):
                TEMPLATE.resolve_template(missing)
            corrupt.write_bytes(b"not a PPTX")
            from zipfile import BadZipFile
            with self.assertRaises(BadZipFile):
                TEMPLATE.resolve_template(corrupt)
            with self.assertRaises(FileNotFoundError):
                TEMPLATE.resolve_template(existing_deck=missing)

    def test_default_is_relocatable_and_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            relocated = Path(tmp) / "installed-skill"
            shutil.copytree(TEMPLATE.SKILL_ROOT / "assets", relocated / "assets")
            result = TEMPLATE.resolve_template(skill_root=relocated)
            self.assertTrue(Path(result["template"]["path"]).is_relative_to(relocated))
            manifest_path = relocated / "assets/batchgen-template.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "sha256 differs"):
                TEMPLATE.resolve_template(skill_root=relocated)

    def test_xml_reserialization_does_not_report_a_content_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, result = Path(tmp) / "source.pptx", Path(tmp) / "result.pptx"
            fixture(source)
            with ZipFile(source) as before, ZipFile(result, "w") as after:
                for name in before.namelist():
                    data = before.read(name)
                    if name.endswith((".xml", ".rels")):
                        data = ET.tostring(ET.fromstring(data), encoding="utf-8")
                    after.writestr(name, data)
            self.assertEqual("passed", MODULE.audit_deck(result, source, [(1, 1)])["status"])

    def test_display_order_and_preserved_media_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, result = Path(tmp) / "source.pptx", Path(tmp) / "result.pptx"
            fixture(source)
            fixture(result)
            report = MODULE.audit_deck(result, source, [(1, 1)], 2, True, [], ["问题二"])
            self.assertEqual("passed", report["status"])
            fixture(result, image=b"changed image")
            report = MODULE.audit_deck(result, source, [(1, 1)])
            self.assertEqual("failed", report["status"])
            self.assertIn("Protected slide parts differ", report["errors"][0])

    def test_notes_stale_content_and_missing_parent_title_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "result.pptx"
            fixture(deck, note=True, heading="OldPaper")
            report = MODULE.audit_deck(deck, expected_count=3, no_notes=True,
                                       forbidden=["oldpaper"], required=["问题二"])
            self.assertEqual("failed", report["status"])
            self.assertEqual([1], report["pages_with_note_text"])
            self.assertEqual(4, len(report["errors"]))

    def test_mapping_requires_source_and_rejects_invalid_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "result.pptx"
            fixture(deck)
            with self.assertRaises(ValueError):
                MODULE.audit_deck(deck, preserve=[(1, 1)])
            self.assertEqual("failed", MODULE.audit_deck(deck, deck, [(0, 1)])["status"])


if __name__ == "__main__":
    unittest.main()
