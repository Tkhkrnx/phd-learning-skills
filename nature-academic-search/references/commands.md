# Commands and handoff

Run from the installed skills root or use absolute script paths. `requests` is already a shared dependency. Proxy use follows the shared `PAPER_SEARCH_TRUST_ENV` setting; do not change global network settings.

```powershell
python nature-academic-search/scripts/academic_search.py search --query "paged attention memory management" --limit 10 --output work/candidates.json
python nature-academic-search/scripts/academic_search.py search --query "retrieval learning" --sources crossref,pubmed --output work/biomedical-candidates.json
python nature-academic-search/scripts/academic_search.py lookup --doi "10.1145/3600006.3613165" --output work/doi.json
python nature-academic-search/scripts/academic_search.py export --input work/candidates.json --format bib --ids <record-id> --output work/selected.bib
python nature-academic-search/scripts/academic_search.py export --input work/candidates.json --format ris --output work/candidates.ris
```

Output JSON contains query, requested providers, per-provider status/count/error, deduplicated records, provenance, and field conflicts. All records remain candidates. A partial result can be used with its limitations; all providers failing returns a failure exit code and still preserves the failure JSON. Outputs use exclusive creation: select a new path rather than overwriting user files.

DOI is normalized before deduplication. Same-title records with conflicting DOI/year stay separate; conflicting fields on a shared DOI are recorded for later verification. Export writes only retrieved metadata. BibTeX keys are stable record IDs, not invented citation counts or author/year guesses. Inspect selected records and repair metadata from authoritative sources, preserving provenance.

For a requested verification report, feed `selected.bib` as the actual `--bib` to `reference-validation-report/scripts/verify_references.py` or its combined pipeline (see that skill's commands). Without a compiled manuscript bibliography, pass `--bibliography-only` explicitly; this verifies the whole selected collection, not manuscript citation coverage. Do not assert an export passed verification. Keep the candidate JSON as a discovery receipt outside the canonical vault notes. A complete existing `.bib` skips discovery.

Upstream inspiration: <https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-academic-search>. The integration is independently implemented and shares this repository's existing search clients; it does not vendor the upstream MCP server or claim its complete feature inventory.
