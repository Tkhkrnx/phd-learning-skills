from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from shared.obsidian.note_quality import (
    READING_HEADINGS,
    REVIEW_ANALYSIS_HEADINGS,
    REVIEW_HEADINGS,
    validate_note_text,
    validate_review_pair,
)
from shared.obsidian.vault_paths import build_note_stem, formal_reading_path, formal_review_path
from shared.paper_note_materials import collect_materials
from shared.paperquay.paper_matcher import PaperMatcher
from shared.paperquay.source_validation import validate_source_alignment


class FakeLibrary:
    def __init__(self, papers: dict[str, dict]):
        self.papers = papers

    def get_paper(self, paper_id: str):
        return self.papers.get(paper_id)


class PaperNoteWorkflowTests(unittest.TestCase):
    def test_conflicted_note_mapping_refuses_implicit_selection(self):
        note = {
            "paper_id": "native-library:agents",
            "anchors": json.dumps([{"paperId": "native-library:dspark"}]),
        }
        matcher = PaperMatcher(FakeLibrary({"agents": {"id": "agents"}, "dspark": {"id": "dspark"}}))
        result = matcher.resolve_from_note_details(note)
        self.assertIsNone(result["paper"])
        self.assertEqual(result["resolution"]["status"], "conflict")

    def test_explicit_paper_id_resolves_a_known_conflict(self):
        note = {
            "paper_id": "native-library:agents",
            "anchors": json.dumps([{"paperId": "native-library:dspark"}]),
        }
        matcher = PaperMatcher(FakeLibrary({"agents": {"id": "agents"}, "dspark": {"id": "dspark"}}))
        result = matcher.resolve_from_note_details(note, explicit_paper_id="dspark")
        self.assertEqual(result["paper"]["id"], "dspark")
        self.assertEqual(result["resolution"]["status"], "explicit-override")

    def test_current_vault_paths_are_short_and_semantic(self):
        vault = Path("C:/vault")
        dspark = formal_reading_path("DSpark: Confidence-Scheduled Speculative Decoding", vault)
        agents = formal_review_path("Agents as Edges, Context as Nodes: Reformulating Multi-Agent Workflow", vault)
        self.assertEqual(dspark, vault / "Research" / "Papers" / "DSpark" / "Reading" / "enhanced.md")
        self.assertEqual(agents, vault / "Research" / "Papers" / "Agents as Edges" / "Review" / "enhanced.md")
        self.assertEqual(build_note_stem("Agents as Edges, Context as Nodes: long subtitle"), "Agents as Edges")

    def test_source_validation_detects_cross_paper_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrong = Path(tmp) / "full.md"
            wrong.write_text("# Agents as Edges, Context as Nodes\nbody", encoding="utf-8")
            report = validate_source_alignment(
                {"content_text": "DSpark speculative decoding", "anchors": "[]"},
                {"id": "dspark", "title": "DSpark: Confidence-Scheduled Speculative Decoding"},
                {"full_md_path": str(wrong)},
            )
            self.assertEqual(report["status"], "failed")

    def test_quality_gate_rejects_scaffold_and_accepts_concise_seven_questions(self):
        scaffold = "\n".join(f"## {heading}\n写作提示：todo" for heading in READING_HEADINGS)
        self.assertEqual(validate_note_text(scaffold, "reading", "DSpark")["status"], "failed")
        sections = []
        for heading in READING_HEADINGS:
            sections.append(f"## {heading}\nDSpark 的这一判断见正文 §3.1 与 Figure 2；这里解释其机制、结果和适用条件。")
        complete = "# DSpark\n" + "\n".join(sections)
        self.assertEqual(validate_note_text(complete, "reading", "DSpark")["status"], "passed")
        self.assertNotIn("遗漏与纠偏", complete)

    def test_quality_gate_rejects_wrong_frontmatter_paper_id(self):
        sections = []
        for heading in READING_HEADINGS:
            sections.append(f"## {heading}\nDSpark 的这一判断见正文 §3.1 与 Figure 2；这里解释其机制、结果和适用条件。")
        note = '---\npaper_id: "agents"\n---\n# DSpark\n' + "\n".join(sections)
        report = validate_note_text(note, "reading", "DSpark", expected_paper_id="dspark")
        self.assertEqual(report["status"], "failed")
        self.assertTrue(any("paper_id mismatch" in error for error in report["errors"]))

    def test_review_outputs_have_distinct_shapes_and_no_private_correction(self):
        analysis_sections = [
            f"## {index}. {heading}\nAgents as Edges 的这一判断见正文 §3.2 与 Table 2；影响和修改建议在此说明。"
            for index, heading in enumerate(REVIEW_ANALYSIS_HEADINGS, 1)
        ]
        analysis = "# Review Analysis: Agents as Edges\n" + "\n".join(analysis_sections)
        analysis += "\nWeak Accept：主要是组合式创新。"
        formal_sections = [
            f"## {heading}\nAgents as Edges 的这一判断见正文 §3.2 与 Table 2；影响和修改建议在此说明。"
            for heading in REVIEW_HEADINGS
        ]
        formal = "# Review: Agents as Edges\n" + "\n".join(formal_sections)
        formal += "\nWeak Accept：主要是组合式创新。"
        self.assertEqual(validate_note_text(analysis, "review-analysis", "Agents as Edges")["status"], "passed")
        self.assertEqual(validate_note_text(formal, "review", "Agents as Edges")["status"], "passed")
        self.assertEqual(validate_review_pair(analysis, formal)["status"], "passed")
        self.assertEqual(validate_note_text(analysis, "review", "Agents as Edges")["status"], "failed")
        formal += "\n## 你当前审稿笔记的遗漏与纠偏\n原审稿笔记漏了一个问题。"
        self.assertEqual(validate_note_text(formal, "review", "Agents as Edges")["status"], "failed")

    def test_pair_gate_catches_divergent_recommendations(self):
        analysis = "# X\n## Overall Assessment\nWeak Accept，因为论文方法有效但创新偏组合。"
        formal = "# X\n## Overall Recommendation\nWeak Reject，因为方法根本错误。"
        report = validate_review_pair(analysis, formal)
        self.assertEqual(report["status"], "failed")
        self.assertTrue(any("mismatch" in error for error in report["errors"]))
        self.assertEqual(
            validate_review_pair(
                "## Overall Assessment\n弱接收，创新偏组合。",
                "## Overall Recommendation\nWeak Accept，系统有效。",
            )["status"],
            "passed",
        )

    def test_no_note_mode_does_not_allow_invented_prior_view(self):
        sections = [
            f"## {heading}\nDSpark 的判断见正文 §3 与 Figure 1；这里解释其机制和证据边界。"
            for heading in READING_HEADINGS
        ]
        text = "# DSpark\n" + "\n".join(sections) + "\n你原来误以为它只有一个模块。"
        report = validate_note_text(text, "reading", "DSpark")
        self.assertEqual(report["status"], "failed")
        self.assertTrue(any("prior note" in error for error in report["errors"]))

    def test_material_inventory_accepts_paper_without_note_and_preserves_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp) / "study.md"
            paper.write_text("# Example paper\n## Design\nText.", encoding="utf-8")
            before = paper.read_bytes()
            report = collect_materials("reading", paper=paper)
            self.assertIsNone(report["note"])
            self.assertIsNone(report["pptx"])
            self.assertTrue(report["paper_source_available"])
            self.assertEqual(report["paper"]["headings"], ["Example paper", "Design"])
            self.assertEqual(paper.read_bytes(), before)

    def test_ppt_inventory_keeps_slide_order_and_speaker_notes_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "review.pptx"
            presentation = (
                '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<p:sldIdLst><p:sldId r:id="rId2"/><p:sldId r:id="rId1"/></p:sldIdLst>'
                '</p:presentation>'
            )
            rels = (
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="slide" Target="slides/slide1.xml"/>'
                '<Relationship Id="rId2" Type="slide" Target="slides/slide2.xml"/>'
                '</Relationships>'
            )
            note_rels = (
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="x/notesSlide" Target="../notesSlides/notesSlide2.xml"/>'
                '</Relationships>'
            )
            def slide(label: str) -> str:
                return (
                    '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                    f'<p:sp><p:txBody><a:p><a:r><a:t>{label}</a:t></a:r></a:p></p:txBody></p:sp></p:sld>'
                )
            with ZipFile(deck, "w") as archive:
                archive.writestr("ppt/presentation.xml", presentation)
                archive.writestr("ppt/_rels/presentation.xml.rels", rels)
                archive.writestr("ppt/slides/slide1.xml", slide("older slide"))
                archive.writestr("ppt/slides/slide2.xml", slide("first slide"))
                archive.writestr("ppt/slides/_rels/slide2.xml.rels", note_rels)
                archive.writestr("ppt/notesSlides/notesSlide2.xml", slide("teacher note"))
            result = collect_materials("review", pptx=deck)
            slides = result["pptx"]["slides"]
            self.assertEqual([item["text"] for item in slides], ["first slide", "older slide"])
            self.assertEqual(slides[0]["speaker_notes"], "teacher note")
            self.assertIsNone(result["note"])
            self.assertFalse(result["paper_source_available"])


if __name__ == "__main__":
    unittest.main()
