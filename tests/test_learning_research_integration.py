from __future__ import annotations

from copy import deepcopy
from datetime import date
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

from shared.search import academic_records as academic
from shared.writing.revision_tracker import validate_revision_map

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


learning = load_module("learning_session", "targeted-knowledge-closure/scripts/learning_session.py")
verification = load_module("reference_verification", "reference-validation-report/scripts/verify_references.py")
report = load_module("reference_report", "reference-validation-report/scripts/generate_reference_validation_report.py")
pipeline = load_module("reference_pipeline", "reference-validation-report/scripts/run_reference_validation_pipeline.py")


class LearningSessionTests(unittest.TestCase):
    def test_stale_writer_cannot_erase_new_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            state = learning.create_session("learn", [])
            original = json.dumps(state)
            path.write_text(original, encoding="utf-8")
            newer = deepcopy(state)
            newer["goal"] = "newer goal"
            learning.save_session(path, newer, original)
            with self.assertRaises(ValueError):
                learning.save_session(path, state, original)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["goal"], "newer goal")
            self.assertFalse(path.with_suffix(".json.tmp").exists())

    def test_resume_retains_attempts_errors_and_source_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            material = Path(tmp) / "chapter.md"
            material.write_text("request A prefill precedes request A decode", encoding="utf-8")
            state = learning.create_session("Understand interleaved requests", [material])
            learning.set_plan(state, [{"id": "order", "title": "Request-local order", "source": "chapter.md:1", "prerequisites": []}])
            learning.add_exercise(state, {"id": "a", "concept": "order", "prompt": "Can B decode while A prefills?", "answer": "Yes if B finished its own prefill", "source": "chapter.md:1"})
            learning.record_attempt(state, exercise="a", response="A decodes before prefill", assessment="incorrect", feedback="A and B are different requests", error_type="actor identity", review_on="2026-10-29")
            resumed = json.loads(json.dumps(state))
            status = learning.session_status(resumed, date(2026, 10, 29))
            self.assertEqual(status["last_attempt"]["error_type"], "actor identity")
            self.assertEqual(len(status["due"]), 1)
            self.assertFalse(status["source_review_required"])
            material.write_text("changed source", encoding="utf-8")
            self.assertTrue(learning.session_status(resumed)["source_review_required"])
            self.assertEqual(len(resumed["attempts"]), 1)
            self.assertIn("not inferred", status["mastery"])

    def test_graph_rejects_cycles_unknown_prerequisites_and_orphans(self):
        state = learning.create_session("learn", [])
        for graph in (
            [{"id": "a", "title": "A", "source": "p1", "prerequisites": ["b"]}],
            [{"id": "a", "title": "A", "source": "p1", "prerequisites": ["a"]}],
        ):
            with self.assertRaises(ValueError):
                learning.set_plan(state, graph)
        learning.set_plan(state, [{"id": "a", "title": "A", "source": "p1"}])
        learning.add_exercise(state, {"id": "e", "concept": "a", "prompt": "Q", "answer": "A", "source": "p1"})
        with self.assertRaises(ValueError):
            learning.set_plan(state, [{"id": "b", "title": "B", "source": "p2"}])

    def test_cli_creates_and_resumes_without_overwriting_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state, exported = root / "state.json", root / "guide.md"
            command = [sys.executable, str(ROOT / "targeted-knowledge-closure/scripts/learning_session.py"), "--state", str(state)]
            created = subprocess.run(command + ["init", "--goal", "Learn a concept"], capture_output=True, text=True)
            self.assertEqual(created.returncode, 0, created.stderr)
            duplicate = subprocess.run(command + ["init", "--goal", "wrong overwrite"], capture_output=True, text=True)
            self.assertNotEqual(duplicate.returncode, 0)
            status = subprocess.run(command + ["status"], capture_output=True, text=True)
            self.assertEqual(json.loads(status.stdout)["goal"], "Learn a concept")
            result = subprocess.run(command + ["export", "--output", str(exported)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            original = exported.read_bytes()
            result = subprocess.run(command + ["export", "--output", str(exported)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(original, exported.read_bytes())


class AcademicDiscoveryTests(unittest.TestCase):
    def record(self, provider="crossref", **updates):
        raw = {"title": "A grounded method", "year": 2025, "authors": [{"name": "A Author"}],
               "externalIds": {"DOI": "10.1234/test"}, "url": "https://doi.org/10.1234/test"}
        raw.update(updates)
        return academic.normalized_record(raw, provider)

    def test_dedup_normalizes_doi_and_retains_conflicting_metadata(self):
        first = self.record()
        second = self.record("openalex", year=2026, externalIds={"DOI": "https://doi.org/10.1234/TEST"})
        rows = academic.merge_records([first, second])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["doi"], "10.1234/test")
        self.assertEqual(rows[0]["status"], "candidate")
        self.assertEqual(len(rows[0]["provenance"]), 2)
        self.assertEqual(rows[0]["conflicts"][0]["field"], "year")

    def test_same_title_different_doi_or_year_is_not_collapsed(self):
        rows = academic.merge_records([self.record(), self.record(externalIds={"DOI": "10.1234/other"})])
        self.assertEqual(len(rows), 2)
        rows = academic.merge_records([self.record(externalIds={}), self.record(externalIds={}, year=2024)])
        self.assertEqual(len(rows), 2)

    def test_partial_coverage_and_empty_success_are_distinct(self):
        with patch.object(academic, "query_crossref", side_effect=RuntimeError("unavailable")), patch.object(academic, "query_pubmed", return_value=[]):
            payload = academic.discover("adaptive learning", ["crossref", "pubmed"], 3)
        self.assertEqual([c["status"] for c in payload["coverage"]], ["failed", "ok"])
        self.assertEqual(payload["coverage"][1]["count"], 0)
        self.assertEqual(payload["verification"], "not performed")

    def test_export_can_enter_verifier_without_fake_compiled_files(self):
        records = academic.merge_records([self.record(type="journal-article", venue="Venue")])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "selected.bib").write_text(academic.export_records(records, "bib"), encoding="utf-8")
            entries, _ = verification.load_local_entries(root, "selected.bib", "missing.bbl", "missing.tex", bibliography_only=True)
            self.assertEqual(entries[0].fields["doi"], "10.1234/test")
            self.assertEqual(entries[0].key, records[0]["id"])
            self.assertEqual(entries[0].fields["title"], "A grounded method")
            with self.assertRaises(ValueError):
                verification.load_local_entries(root, "selected.bib", "missing.bbl", "missing.tex")

    def test_export_preserves_unknown_fields_and_escapes_prose(self):
        records = academic.merge_records([self.record(title="A & B: 50%", year=None, authors=[], externalIds={})])
        bib = academic.export_records(records, "bib")
        self.assertIn(r"A \& B: 50\%", bib)
        self.assertNotIn("year =", bib)
        self.assertNotIn("author =", bib)
        self.assertNotIn("doi =", bib)
        ris = academic.export_records(records, "ris")
        self.assertIn("TY  - GEN", ris)
        self.assertIn("TI  - A & B: 50%", ris)

    def test_export_does_not_latex_escape_identifiers(self):
        records = academic.merge_records([self.record(externalIds={"DOI": "10.1234/a_b"}, url="https://example.test/a_b?x=1&y=2")])
        bib = academic.export_records(records, "bib")
        self.assertIn("doi = {10.1234/a_b}", bib)
        parsed = verification.parse_bib_entry(bib)
        self.assertEqual(parsed[2]["doi"], "10.1234/a_b")
        self.assertEqual(parsed[2]["url"], "https://example.test/a_b?x=1&y=2")

    def test_crossref_and_pubmed_parse_primary_metadata(self):
        item = {"title": ["Title"], "issued": {"date-parts": [[2025]]}, "DOI": "10.1234/a", "author": [{"given": "Ada", "family": "L"}]}
        self.assertEqual(academic.crossref_record(item)["year"], 2025)
        self.assertEqual(academic.crossref_record(item)["authors"], [{"name": "Ada L"}])
        query = Mock()
        query.json.return_value = {"esearchresult": {"idlist": ["42"]}}
        full = Mock(text='<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>42</PMID><Article><ArticleTitle>Study <i>title</i></ArticleTitle><Journal><Title>J</Title><JournalIssue><PubDate><Year>2025</Year></PubDate></JournalIssue></Journal></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>')
        session = Mock()
        session.get.side_effect = [query, full]
        with patch.object(academic.search, "make_session", return_value=session):
            rows = academic.query_pubmed("test", 1)
        self.assertEqual(rows[0]["title"], "Study title")
        self.assertEqual(rows[0]["year"], 2025)
        self.assertEqual(rows[0]["externalIds"]["PMID"], "42")


class RevisionTrackingTests(unittest.TestCase):
    def test_verified_requires_existing_anchored_changes_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.tex").write_text("Observed on one GPU only.\n", encoding="utf-8")
            (root / "results.md").write_text("Local run: one GPU.\n", encoding="utf-8")
            row = {"id": "R1.2", "concern": "Clarify hardware scope", "action": "State single GPU", "status": "verified",
                   "locations": [{"path": "main.tex", "line": 1, "anchor": "one GPU"}],
                   "evidence": [{"path": "results.md", "line": 1, "anchor": "one GPU"}], "verification": "Compared sentence with run record"}
            self.assertEqual(validate_revision_map({"revisions": [row]}, root), [])
            stale = deepcopy(row)
            stale["locations"][0]["anchor"] = "multi GPU"
            self.assertTrue(validate_revision_map({"revisions": [stale]}, root))
            absent = deepcopy(row)
            absent.pop("evidence")
            self.assertTrue(validate_revision_map({"revisions": [absent]}, root))
            escaped = deepcopy(row)
            escaped["locations"][0]["path"] = "../outside.tex"
            self.assertTrue(validate_revision_map({"revisions": [escaped]}, root))


class ReferenceHandoffTests(unittest.TestCase):
    def test_collection_report_does_not_claim_manuscript_coverage(self):
        options = dict(paper_title="References", venue="N/A", verification_date="2026-10-29", tool_text="test",
                       entries=[report.Entry("k", "", "A paper", "confirmed")], all_real=True, no_metadata_errors=True)
        standard = report.render_html(**options)
        collection = report.render_html(**options, input_scope="bibliography-only")
        self.assertIn("本文所有", standard)
        self.assertNotIn("本文所有", collection)
        self.assertIn("未核查正文引用覆盖与论据支撑", collection)

    def test_pipeline_forwards_collection_mode_without_fake_bbl(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ["pipeline", "--project-dir", tmp, "--bib", "selected.bib", "--bibliography-only", "--paper-title", "References"]
            with patch.object(sys, "argv", args), patch.object(pipeline.subprocess, "run") as runner:
                self.assertEqual(pipeline.main(), 0)
            verification_command, report_command = [call.args[0] for call in runner.call_args_list]
            self.assertIn("--bibliography-only", verification_command)
            self.assertIn("selected.bib", verification_command)
            self.assertIn("--verification-json", report_command)
            self.assertIn("AI 自动参考文献完整性检测（文献清单）", report_command)
            self.assertFalse((Path(tmp) / "main.bbl").exists())


if __name__ == "__main__":
    unittest.main()
