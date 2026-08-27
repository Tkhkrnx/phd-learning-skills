from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from shared.search.discovery import discover_open_query
from shared.search.paper_search import query_papers_ensemble


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "topic-paper-finder" / "scripts" / "topic_finder.py"
SPEC = importlib.util.spec_from_file_location("topic_finder", MODULE_PATH)
assert SPEC and SPEC.loader
topic_finder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(topic_finder)


class TopicFinderPolicyTests(unittest.TestCase):
    def test_study_mode_keeps_recent_default_and_taxonomy(self):
        policy = topic_finder.resolve_search_policy(
            mode="study", recent_years=3, min_year=None, current_year=2026
        )
        self.assertEqual(policy["min_year"], 2024)
        self.assertTrue(policy["taxonomy_filter"])
        self.assertEqual(policy["vault_duplicate_policy"], "skip")

    def test_evidence_modes_have_no_implicit_year_or_venue_filter(self):
        for mode in ("problem-boundary", "mechanism-inspiration"):
            policy = topic_finder.resolve_search_policy(
                mode=mode, recent_years=3, min_year=None, current_year=2026
            )
            self.assertIsNone(policy["min_year"])
            self.assertFalse(policy["taxonomy_filter"])
            self.assertFalse(policy["venue_filter"])
            self.assertEqual(policy["vault_duplicate_policy"], "retain-and-annotate")

    def test_explicit_year_floor_overrides_mode_default(self):
        policy = topic_finder.resolve_search_policy(
            mode="study", recent_years=3, min_year=1998, current_year=2026
        )
        self.assertEqual(policy["min_year"], 1998)
        self.assertEqual(policy["year_policy"], "explicit")

    def test_query_portfolio_merges_duplicates_and_records_provenance(self):
        older = SimpleNamespace(title="Shared: Paper", paper_id="p1", url="u1", score=10, year=2020)
        stronger = SimpleNamespace(title="Shared   Paper", paper_id="p1", url="u1", score=50, year=2021)
        other = SimpleNamespace(title="Other Paper", paper_id="p2", url="u2", score=20, year=2022)
        merged = topic_finder.merge_query_results(
            [("direct query", [older, other]), ("counter query", [stronger])], limit=5
        )
        self.assertEqual([row.title for row, _ in merged], ["Shared   Paper", "Other Paper"])
        self.assertEqual(merged[0][1], ["direct query", "counter query"])

    def test_academic_ensemble_merges_indexes_and_records_coverage(self):
        semantic_row = {
            "title": "A: Mechanism",
            "year": 2020,
            "abstract": None,
            "authors": [],
            "externalIds": {"DOI": "10.1/a"},
            "openAccessPdf": {},
            "url": "https://example.test/semantic",
            "paperId": "semantic-a",
        }
        openalex_row = {
            "title": "A Mechanism",
            "year": 2020,
            "abstract": "causal details",
            "authors": [{"name": "A. Author"}],
            "externalIds": {"DOI": "10.1/a"},
            "openAccessPdf": {"url": "https://example.test/a.pdf"},
            "url": "https://example.test/openalex",
            "paperId": "openalex-a",
        }
        with (
            patch("shared.search.paper_search.query_semantic_scholar", return_value=[semantic_row]),
            patch("shared.search.paper_search.query_openalex", return_value=[openalex_row]),
            patch("shared.search.paper_search.query_dblp", return_value=[]),
            patch("shared.search.paper_search.query_arxiv", return_value=[]),
        ):
            rows, notes = query_papers_ensemble("mechanism", limit=5, min_year=None)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["abstract"], "causal details")
        self.assertEqual(rows[0]["discoverySources"], ["semantic_scholar", "openalex"])
        self.assertEqual(len(notes), 4)

    @patch("shared.search.discovery.query_papers_ensemble")
    def test_open_discovery_passes_through_no_year_floor(self, query_mock):
        query_mock.return_value = (
            [
                {
                    "title": "LLM for an unrelated application",
                    "year": 2026,
                    "venue": "Unknown",
                    "abstract": None,
                    "authors": [],
                    "externalIds": {},
                    "openAccessPdf": {},
                    "url": "https://example.test/noise",
                    "paperId": "noise",
                    "discoverySources": ["openalex"],
                },
                {
                    "title": "Seminal Mechanism",
                    "year": 1985,
                    "venue": "Unknown",
                    "abstract": "adaptive control mechanism",
                    "authors": [],
                    "externalIds": {},
                    "openAccessPdf": {},
                    "url": "https://example.test/paper",
                    "paperId": "seminal",
                    "discoverySources": ["semantic_scholar"],
                }
            ],
            ["semantic_scholar:ok:1", "openalex:ok:0"],
        )
        rows, notes = discover_open_query(
            query="adaptive control mechanism",
            min_year=None,
            limit=4,
            evidence_mode="mechanism-inspiration",
        )
        self.assertEqual(rows[0].year, 1985)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].subtopic_id, "mechanism-inspiration")
        self.assertEqual(notes, ["semantic_scholar:ok:1", "openalex:ok:0"])
        self.assertIsNone(query_mock.call_args.kwargs["min_year"])


if __name__ == "__main__":
    unittest.main()
