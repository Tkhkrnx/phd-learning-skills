---
name: nature-academic-search
description: Discover and export traceable academic references across indexes before bibliography validation when the user explicitly invokes this Skill.
---

# Academic Search and Reference Handoff

An adapted discovery/export stage inspired by the community `Yuan1z0825/nature-skills` project, not an official Nature service. Keep research-intent selection in `topic-paper-finder`; use this entry for cross-source metadata, identifier lookup, bibliography preparation, and export.

## Workflow

1. Recover the question, source scope, needed fields, and requested output. Reuse a supplied complete bibliography directly; do not force rediscovery before validation or network access before offline export.
2. For research relevance/boundaries, use the existing `topic-paper-finder` modes and query portfolio. For metadata discovery, run `scripts/academic_search.py search` with selected providers. Crossref plus the existing arXiv/OpenAlex/DBLP clients are the CS-oriented default; PubMed is opt-in for an appropriate subject. No implicit year/venue filter applies here.
3. Read coverage and provenance. A failed provider is not an empty successful search. Inspect decisive original sources and select relevant records before exporting a final bibliography. Preserve metadata conflicts rather than silently overwriting them.
4. Export selected records as BibTeX or RIS with `scripts/academic_search.py export`. Lookup an exact DOI with `lookup`. Do not generate missing authors, DOI, pages, venue, or publication year from model memory.
5. When the user requested an end-to-end citation report, pass the exported bibliography and actual project inputs to `reference-validation-report`. For search only, return candidates and gaps; do not create an unsolicited PDF.

## Evidence boundary

Discovery records are `candidate`, not `confirmed`. Identifier lookup locates metadata but does not certify all supplied manuscript fields. Bibliographic existence, source full-text inspection, and whether a claim is supported are distinct checks. Searching several indexes does not establish exhaustive coverage or novelty.

If an external API is blocked, report it and use available tools with explicit provenance. Optional Scopus/ScienceDirect require the user's licensed access; never silently enable paid services. For MeSH, citation networks, or independent-citation audits, use installed appropriate tools and primary records; this adaptation does not claim those upstream extensions are implemented by the local script.

Read [commands and handoff](references/commands.md) for execution and file contracts. For claim-level manuscript auditing, use [writing workflow](../shared/writing/paper-writing-workflow.md) only when that is part of the requested task.
