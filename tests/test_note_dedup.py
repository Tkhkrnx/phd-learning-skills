from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from shared.obsidian.note_dedup import compare_notes


class NoteDedupTests(unittest.TestCase):
    def test_storage_only_changes_do_not_create_new_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left, right = root / "old.md", root / "vault.md"
            (root / "a.png").write_bytes(b"same image")
            (root / "b.png").write_bytes(b"same image")
            left.write_bytes(b'\xef\xbb\xbf---\r\nstatus: draft\r\n---\r\n# Paper\r\n\r\n![Plot](a.png)\r\nRating 6\r\n')
            right.write_text('# Paper\n\n![Plot](b.png)\nRating 6\n', encoding="utf-8")
            before = left.read_bytes(), right.read_bytes()
            result = compare_notes(left, right)
            self.assertFalse(result["raw_bytes_equal"])
            self.assertTrue(result["equivalent_body_and_images"])
            self.assertFalse(result["frontmatter_equal"])
            self.assertEqual("draft", result["candidate"]["frontmatter"]["status"])
            self.assertEqual(before, (left.read_bytes(), right.read_bytes()))

    def test_newer_mtime_does_not_hide_changed_verdict_or_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left, right = root / "newer.md", root / "approved.md"
            left.write_text('# Paper\nRating 5\nSpeedup 2.1\n', encoding="utf-8")
            right.write_text('# Paper\nRating 6\nSpeedup 1.2\n', encoding="utf-8")
            os.utime(left, (2000000000, 2000000000))
            result = compare_notes(left, right)
            self.assertGreater(result["candidate"]["modified_ns"], result["existing"]["modified_ns"])
            self.assertFalse(result["body_equal_after_storage_normalization"])

    def test_same_image_caption_with_different_or_missing_image_is_not_equivalent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left, right = root / "a.md", root / "b.md"
            left.write_text('![same caption](a.png)', encoding="utf-8")
            right.write_text('![same caption](b.png)', encoding="utf-8")
            (root / "a.png").write_bytes(b"old plot")
            (root / "b.png").write_bytes(b"new plot")
            result = compare_notes(left, right)
            self.assertTrue(result["body_equal_after_storage_normalization"])
            self.assertFalse(result["equivalent_body_and_images"])
            (root / "b.png").unlink()
            self.assertFalse(compare_notes(left, right)["all_image_bytes_verified"])

    def test_external_citation_and_code_changes_are_not_erased(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left, right = root / "a.md", root / "b.md"
            left.write_text('[Evidence](https://example.com/a)\n```\n![Code](a.png)\n```', encoding="utf-8")
            right.write_text('[Evidence](https://example.com/b)\n```\n![Code](b.png)\n```', encoding="utf-8")
            self.assertFalse(compare_notes(left, right)["body_equal_after_storage_normalization"])


if __name__ == "__main__":
    unittest.main()
