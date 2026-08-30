---
name: topic-paper-finder
description: "Explicit skill-use request only: activate only when the user explicitly asks to use, call, or apply a paper-search, literature-search, topic-paper-finder, or equivalent skill to a stated search task; the exact identifier is optional. An ordinary request to find papers is not authorization. Search academic papers for a recent taxonomy-aligned study, a problem-boundary evidence portfolio, or cross-domain mechanism inspiration, with optional PDF download and local-vault matching. This skill discovers candidates; it does not prove novelty, unresolved status, or method superiority, and it does not search repositories, documentation, articles, or blogs."
---

Read `finder_config.yaml`, `weekly-paper-radar/radar_config.yaml`, `scripts/topic_finder.py`, and the required `shared/search` and `shared/obsidian` modules before running the script.

## Modes

- `study`: retain the existing last-three-years default, shared taxonomy, venue policy, PDF workflow, and high-confidence vault duplicate skipping.
- `problem-boundary`: search arbitrary academic queries without the taxonomy, venue, or recent-year defaults. Use a query portfolio spanning the phenomenon, synonyms, seminal/current work, closest solution families, limitations, negative results, and exact-title follow-ups.
- `mechanism-inspiration`: search arbitrary same-field, adjacent-field, and structurally analogous academic mechanisms without taxonomy, venue, or recent-year defaults. Queries should describe causal structure and constraints, not only the target application.

An explicit `--min-year` applies in every mode. Evidence modes retain already-noted papers and annotate their vault matches because an existing note may still contain decisive evidence.

## Workflow

1. Normalize the request into one or more focused academic queries. When the request is Chinese, derive established English terminology and synonyms rather than sending only a literal Chinese sentence. Use repeated `--query` arguments instead of one oversized Boolean query.
2. Select the mode from the user's intent. Do not apply the three-year study default to novelty-boundary or mechanism-inspiration work.
3. Run the shared discovery engine and read the structured JSON. Evidence modes combine Semantic Scholar, OpenAlex, DBLP, and arXiv when reachable; treat the merged results as an academic candidate pool.
4. Open and inspect decisive primary sources before using them to claim that a problem is unresolved or a method transfers. A title, abstract, snippet, or citation count is not sufficient.
5. Summarize the searched query families, strongest candidates and counterevidence, year/venue limits, recovery failures, vault matches, and remaining blind spots in the conversation.
6. If downloading, report successful local files, the actual PaperQuay directory, and every manual PDF follow-up reason.

The script outputs JSON only. It records `mode`, `queries`, `search_policy`, `coverage_status`, `matched_queries`, `discovery_sources`, recovery notes, duplicate policy, PDF status, and results. `configured_indexes_reached` is not a claim of exhaustive literature coverage. Do not pretend that an empty or partially failed search proves absence of prior work.

## Source Boundary

This skill covers academic candidate discovery. For method design, search repositories, official documentation, issues, pull requests, benchmarks, engineering articles, and technical blogs with the available web and code tools. Use those sources for implementation facts or inspiration, not as sole proof of academic novelty.

When `research-problem-formulation` or `research-method-design` is already active, act only as its internal academic evidence backend. Do not open a second collaboration loop, emit a separate lifecycle marker, or replace the active skill's user interaction.

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
