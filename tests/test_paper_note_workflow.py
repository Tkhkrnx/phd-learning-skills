from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from shared.obsidian.note_quality import READING_HEADINGS, validate_note_text
from shared.obsidian.vault_paths import build_note_stem, formal_reading_path, formal_review_path
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

    def test_quality_gate_rejects_scaffold_and_accepts_complete_note(self):
        scaffold = "\n".join(f"## {heading}\n写作提示：todo" for heading in READING_HEADINGS)
        self.assertEqual(validate_note_text(scaffold, "reading", "DSpark")["status"], "failed")
        sections = []
        for heading in READING_HEADINGS:
            sections.append(f"## {heading}\nDSpark 的证据分析。正文 §3.1 与 Figure 2 支撑这一判断。" + "机制、边界与实验解释。" * 120)
        complete = "# DSpark\n" + "\n".join(sections)
        self.assertEqual(validate_note_text(complete, "reading", "DSpark")["status"], "passed")

    def test_quality_gate_rejects_wrong_frontmatter_paper_id(self):
        sections = []
        for heading in READING_HEADINGS:
            sections.append(f"## {heading}\nDSpark 的证据分析。正文 §3.1 与 Figure 2 支撑这一判断。" + "机制、边界与实验解释。" * 120)
        note = '---\npaper_id: "agents"\n---\n# DSpark\n' + "\n".join(sections)
        report = validate_note_text(note, "reading", "DSpark", expected_paper_id="dspark")
        self.assertEqual(report["status"], "failed")
        self.assertTrue(any("paper_id mismatch" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
