from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from shared.obsidian.note_search import (
    classify_note_path, classification_score, has_probable_duplicate,
    normalize_title_for_match, search_vault_notes,
)


class NoteSearchTests(unittest.TestCase):
    def test_vault_search_ignores_skill_mirrors_configuration_and_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            note = vault / "Learning" / "lesson.md"
            note.parent.mkdir()
            note.write_text("declarative condition", encoding="utf-8")
            for folder in (".agents/skills/rpf", ".codex/skills/rpf", ".claude/skills/rpf",
                           ".obsidian", ".trash", "node_modules", "venv"):
                path = vault / folder / "SKILL.md"
                path.parent.mkdir(parents=True)
                path.write_text("declarative condition", encoding="utf-8")
            before = {p: p.read_bytes() for p in vault.rglob("*.md")}
            hits = search_vault_notes("declarative", vault)
            self.assertEqual([str(note)], [hit["path"] for hit in hits])
            self.assertEqual(before, {p: p.read_bytes() for p in vault.rglob("*.md")})

    def test_stage_paths_rank_above_legacy_without_inferring_its_stage(self):
        for separator in ("/", "\\"):
            prefix = separator.join(("vault", "Research", "Papers", "Paper", "Review"))
            kinds = [classify_note_path(Path(prefix + separator + name))
                     for name in ("analysis.md", "formal-review.md", "enhanced.md")]
            self.assertEqual(["review_analysis", "review_report", "review_note_legacy"], kinds)
            self.assertGreater(classification_score(kinds[0]), classification_score(kinds[2]))
            self.assertGreater(classification_score(kinds[1]), classification_score(kinds[2]))

    def test_unicode_titles_match_without_collapsing_distinct_chinese_titles(self):
        self.assertEqual("昇腾 推理 npu", normalize_title_for_match("昇腾：推理 ＮＰＵ"))
        self.assertTrue(has_probable_duplicate("昇腾推理知识笔记", [
            {"path":"Learning/昇腾推理知识笔记.md", "score":75}]))
        self.assertFalse(has_probable_duplicate("昇腾推理知识笔记", [
            {"path":"Learning/显存管理知识笔记.md", "score":100}]))

    def test_canonical_filename_uses_explicit_metadata_title_not_directory_as_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            note = vault / "Research/Papers/Paper/Reading/enhanced.md"
            note.parent.mkdir(parents=True)
            note.write_text('---\ntitle: "昇腾推理知识笔记"\n---\n# 正文\n', encoding="utf-8")
            hits = search_vault_notes("昇腾推理知识笔记", vault)
            self.assertTrue(has_probable_duplicate("昇腾推理知识笔记", hits))
            self.assertFalse(has_probable_duplicate("完全不同的笔记", hits))

    def test_empty_query_and_invalid_limit_do_not_match_everything(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "note.md").write_text("text", encoding="utf-8")
            self.assertEqual([], search_vault_notes("  ", vault))
            self.assertEqual([], search_vault_notes("text", vault, 0))


if __name__ == "__main__":
    unittest.main()
