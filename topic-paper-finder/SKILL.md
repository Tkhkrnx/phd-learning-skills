---
name: topic-paper-finder
description: Search academic papers in study, problem-boundary, or mechanism-inspiration mode when the user explicitly invokes this Skill.
---

Resolve paths relative to this skill directory and run `scripts/topic_finder.py` from the parent skill root. Load `finder_config.yaml` and `../weekly-paper-radar/radar_config.yaml` for policy decisions; inspect script or shared-module source only when modifying or debugging it. If a configured source or local vault is unavailable, report it and use available academic retrieval tools; identify the fallback and do not claim the configured engine ran.

## Modes

- `study`: retain the existing last-three-years default, shared taxonomy, venue policy, PDF workflow, and high-confidence vault duplicate skipping.
- `problem-boundary`: search arbitrary academic queries without the taxonomy, venue, or recent-year defaults. Use a query portfolio spanning the phenomenon, synonyms, seminal/current work, closest solution families, limitations, negative results, and exact-title follow-ups.
- `mechanism-inspiration`: search arbitrary same-field, adjacent-field, and structurally analogous academic mechanisms without taxonomy, venue, or recent-year defaults. Queries should describe causal structure and constraints, not only the target application.

An explicit `--min-year` applies in every mode. Evidence modes retain already-noted papers and annotate their vault matches because an existing note may still contain decisive evidence.

## Workflow

Anchor each search to the current question: object, phenomenon, comparison, source role, and failure condition. Existing favorite papers are seeds only, never a default answer set. For a benchmark question search benchmark/evaluation and measurement work directly; mechanism papers can supply context but cannot replace the closest evaluation alternatives. Keep study-mode filters out of boundary and inspiration searches unless the user requests them.

For shortlisted sources, explain the original problem, contribution, assumptions, relevant evidence and exact relation to the current question, including counterevidence. Distinguish inspected full text from abstract-only leads and blocked sources. Return uncovered query families as well as results. When the user changes the phenomenon or rejects a proposed connection, revise the query portfolio rather than recycling the same citations. For standalone use, ask a focused follow-up only when selection depends on user intent; supporting use returns evidence to the parent without a second interview.

1. Normalize the request into one or more focused academic queries. When the request is Chinese, derive established English terminology and synonyms rather than sending only a literal Chinese sentence. Use repeated `--query` arguments instead of one oversized Boolean query.
2. Select the mode from the user's intent. Do not apply the three-year study default to novelty-boundary or mechanism-inspiration work.
3. Run the shared discovery engine and read the structured JSON. Evidence modes combine Semantic Scholar, OpenAlex, DBLP, and arXiv when reachable; treat the merged results as an academic candidate pool.
4. Open and inspect decisive primary sources before using them to claim that a problem is unresolved or a method transfers. A title, abstract, snippet, or citation count is not sufficient.
5. Summarize the searched query families, strongest candidates and counterevidence, year/venue limits, recovery failures, vault matches, and remaining blind spots in the conversation.
6. If downloading, report successful local files, the actual PaperQuay directory, and every manual PDF follow-up reason.

The script outputs JSON only. It records `mode`, `queries`, `search_policy`, `coverage_status`, `matched_queries`, `discovery_sources`, recovery notes, duplicate policy, PDF status, and results. `configured_indexes_reached` is not a claim of exhaustive literature coverage. Do not pretend that an empty or partially failed search proves absence of prior work.

## Source Boundary

This skill covers academic candidate discovery. For method design, search repositories, official documentation, issues, pull requests, benchmarks, engineering articles, and technical blogs with the available web and code tools. Use those sources for implementation facts or inspiration, not as sole proof of academic novelty.

When `research-problem-formulation` or `research-method-design` is already authorized and delegates a bounded candidate-discovery subtask, that active primary authorization is sufficient for this supporting use. Act only as its internal academic evidence backend. Return the candidate pool, coverage, failures, and blind spots to the primary skill; do not open a second collaboration loop, emit a separate lifecycle marker, or replace the active skill's user interaction.

## Commands

Recent study search:

```powershell
$env:PYTHONPATH="."
python topic-paper-finder\scripts\topic_finder.py --mode study --query "KV cache compression serving" --download-pdf
```

Problem-boundary portfolio with no default year floor:

```powershell
$env:PYTHONPATH="."
python topic-paper-finder\scripts\topic_finder.py --mode problem-boundary --query "state reuse tail latency agent inference" --query "context reuse overhead negative results" --query "incremental computation serving seminal"
```

Cross-domain mechanism search with an explicit floor:

```powershell
$env:PYTHONPATH="."
python topic-paper-finder\scripts\topic_finder.py --mode mechanism-inspiration --min-year 2000 --query "reversible resource activation delayed feedback control" --query "adaptive caching pressure tail latency"
```
