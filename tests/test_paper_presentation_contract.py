from __future__ import annotations

import importlib.util
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


SCRIPT = Path(__file__).resolve().parents[1] / "paper-presentation-builder/scripts/audit_deck.py"
SPEC = importlib.util.spec_from_file_location("paper_deck_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


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
