---
name: weekly-paper-radar
description: Weekly paper radar for State-Centric Runtime Design and Hardware-Conscious Execution. Use when Codex needs to search近3年的系统A会论文, fall back to high-quality AI A venues only when needed, and optionally download PDFs into the local submission directory.
---

Read `radar_config.yaml` and `scripts/weekly_radar.py`.

Workflow:
- Load the topic taxonomy and subtopic keywords.
- Expand each of the three main directions through their full subtopic keyword coverage rather than one broad phrase.
- Search each direction by subtopic rather than by a single broad phrase.
- Prefer official venue pages first, then recover through the shared resilient search stack.
- Prefer system A venues from the config.
- Fall back to other well-known A venues only when system venues do not yield enough candidates; do not hard-code the fallback to AI venues only.
- For each candidate paper, also search the vault first so repeated recommendations can be surfaced as possible duplicates.
- Build a single total candidate pool of about 20 papers across the three directions.
- After the script finishes, Codex should read the candidate pool and directly produce the weekly recommendation in the conversation, rather than expecting the script to write a final recommendation markdown.
- If `--download-pdf` is enabled, save PDFs into the configured local submission directory.
- Expect machine-readable outputs only:
  - `candidate_pool.json`
  - `manual_pdf_followup.json`
- In the final user-facing answer, Codex should also directly summarize:
  - which PDFs were downloaded successfully
  - the actual local submission directory
  - which papers still require manual follow-up
  - and should present that summary in the conversation itself rather than asking the user to inspect output files

Rules:
- Keep the year range to the most recent 3 years.
- The three directions are fixed by repo policy:
  - `State-Aware Orchestration and Resource Governance`
  - `Hardware-Aware Memory Management and Semantic Consistency`
  - `State-Reuse Inference for Long Contexts and MoE`
- The script should produce a total candidate pool of about 20 papers, not pretend to be the final human-facing weekly recommendation by itself.
- The final recommendation layer should aim for about 10 weekly picks and 4 deep-read priorities.
- Codex should make that final recommendation live from `candidate_pool.json`, following this policy:
  - Prefer papers that directly serve the current PhD problem chain, not merely papers that are new or popular.
  - Cover all three main directions in the final 10-paper recommendation.
  - Avoid over-concentrating on one venue or one subtopic when near-equivalent alternatives exist.
  - For the 4 deep-read picks, favor papers whose mechanism, system framing, and experimental setup are most likely to sharpen the user's own research judgment.
- Treat output coverage and result quality separately. If the script fills the requested count with weakly related papers, that still requires manual review and possible taxonomy/source refinement.
- If no PDF is available, report that clearly so the user can search manually.
- Treat these PDF states as semantically different:
  - `downloaded`: PDF already saved to PaperQuay.
  - `publisher_blocked_or_login_required`: official DOI/ACM path exists but current environment cannot fetch it automatically.
  - `listing_page_only`: the official venue page exposes title/authors but no stable per-paper PDF link.
  - `pdf_not_found_manual_search_needed`: the page looked paper-specific, but no trustworthy PDF link was resolved.
- Do not ingest into Obsidian directly; the downstream reading flow stays in PaperQuay first.

Default command:

```powershell
$env:PYTHONPATH="."
python weekly-paper-radar\scripts\weekly_radar.py --download-pdf
```
