"""Regression for labels lost during entrypoint/guide simplification.

This guards the presentation contract. The independent first-response cases
check whether the actual prose and literature comparison are useful.
"""
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FormulationDeliveryTests(unittest.TestCase):
    def test_both_delivery_routes_specify_the_chinese_labels_in_question_one(self):
        for relative, marker in [
            ("research-problem-formulation/SKILL.md", "1. **What the problem is."),
            ("shared/expert-skill-references/seven_question_research_outputs.md", "1. **问题是什么？"),
        ]:
            with self.subTest(relative=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                first_answer = text.split(marker, 1)[1].split("\n2. ", 1)[0]
                self.assertRegex(first_answer, r"\*\*背景：\*\*.*?\*\*问题：\*\*")

    def test_literature_table_separates_method_category_and_papers_on_each_route(self):
        header = "类别 | 相关工作文章 | 已解决的问题与优势 | 为什么仍不足以解决本文问题"
        for relative in (
            "research-problem-formulation/SKILL.md",
            "research-problem-formulation/references/deep-workflow.md",
            "shared/expert-skill-references/seven_question_research_outputs.md",
        ):
            with self.subTest(relative=relative):
                self.assertIn(header, (ROOT / relative).read_text(encoding="utf-8"))

    def test_accepted_example_renders_two_distinct_paragraphs(self):
        text = (ROOT / "shared/tests/research_workflow_requirements_zh.md").read_text(encoding="utf-8")
        first_answer = text.split("1. **问题是什么？**", 1)[1].split("\n2. ", 1)[0]
        self.assertRegex(first_answer, re.compile(
            r"^   \*\*背景：\*\*[^。！？\n]+。\n\n   \*\*问题：\*\*[^。！？\n]+。$", re.M
        ))
