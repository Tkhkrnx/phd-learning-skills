---
name: topic-paper-finder
description: Search papers by topic, subtopic, venue, and recent years for the user's PhD study workflow. Use when Codex needs a targeted paper search with recent-year filtering, optional PDF download to PaperQuay, and alignment to the shared runtime/hardware taxonomy.
---

Read `finder_config.yaml`, `weekly-paper-radar/radar_config.yaml`, and `scripts/topic_finder.py`.

Workflow:
- First turn a fuzzy user request into explicit search conditions: topic keywords, likely subtopics, target venues or venue classes, and year range.
- If the user did not specify all fields, infer reasonable defaults from the repo taxonomy and recent-year policy instead of waiting for perfect input.
- Search through the shared discovery engine used by `weekly-paper-radar`, so official sources are tried before aggregate fallback.
- For each hit, also call the vault search layer so the result shows whether a similar reading/review note may already exist.
- The script should return structured JSON results only.
- After the script returns, Codex should read those results and directly answer the user with the search conclusion in the conversation, rather than expecting the script to write a final markdown report.
- Report title, venue, year, authors, URL, PDF status, and vault de-duplication hints.
- Return structured `manual_pdf_followup` items whenever the PDF cannot be downloaded automatically.
- Optionally download the PDF to PaperQuay data.
- In the final user-facing answer, Codex should directly summarize:
  - which PDFs were downloaded successfully
  - the actual PaperQuay target directory
  - which papers still require manual follow-up
  - and should do so in the conversation itself, not by telling the user to open a JSON file

Rules:
- Keep the default search window aligned with the last 3 years.
- Help the user understand what fields are useful to specify:
  - topic or concrete problem
  - subtopic or keywords
  - venue, venue tier, or conference/journal family
  - year window
  - whether PDF download is wanted
- Do not force the user to provide all fields up front; Codex should narrow a vague request into concrete search terms before running the script.
- If a result is already covered by a high-confidence vault note, prefer skipping it and expose that decision in `duplicate_skips`.
- If the PDF cannot be found, return a clear manual-search-needed result instead of pretending success.
- Preserve the difference between:
  - `publisher_blocked_or_login_required`
  - `listing_page_only`
  - `pdf_not_found_manual_search_needed`

When the user invokes this skill in natural language, Codex should proactively normalize the request and, when useful, tell the user they can provide inputs like:
- “我想找什么问题/方向的论文”
- “希望限定哪些会议/期刊或 A 会层级”
- “近几年”
- “是否顺手下载 PDF 到 PaperQuay”

Default command:

```powershell
$env:PYTHONPATH="."
python topic-paper-finder\scripts\topic_finder.py --query "KV cache compression serving" --download-pdf
```
