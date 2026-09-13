---
name: reference-validation-report
description: Verify a LaTeX bibliography and generate the Chinese reference-validation PDF when the user explicitly invokes this Skill.
---

# Reference Validation Report

Verify bibliography entries before generating the report. Never infer “no fabricated or AI-hallucinated references” from formatting or an unverified bibliography.

## Workflow

1. Locate the relevant `.tex`, `.bib`, and `.bbl` inputs.
2. Run `scripts/verify_references.py` and preserve the per-entry evidence status.
3. Generate the report with `scripts/generate_reference_validation_report.py`, or use the combined pipeline.
4. Render and inspect the first page plus at least one representative body page.
5. Repair mismatches between the PDF, HTML, and verification JSON, then regenerate and recheck.

## Evidence boundary

Prefer DOI/Crossref records, arXiv records, publisher pages, and official venue pages. Aggregators and search snippets may locate a source but are not final authority.

- Say all references are confirmed only when every entry is `confirmed` or when the user explicitly attests that every entry was manually checked.
- If any entry is `pending`, `missing`, or materially inconsistent, keep the conclusion conservative and surface it in the report.
- Do not invent evidence links, normalize away a real metadata conflict, or mark an unverified entry as passed.

## Load on demand

- Read [commands and input modes](references/commands.md) when running the normal pipeline, using the manual-attestation path, or handling non-standard bibliography input.
- Read `references/format-spec.md` only when generating or repairing the accepted PDF layout.
- Inspect script source only when modifying it or diagnosing a failure.

## Completion

Finish when the verification JSON, HTML, and PDF agree; Chinese text and evidence links render correctly; the conclusion matches the verification status; and inspected pages contain no clipping, placeholder glyphs, or local-file footer leakage.
