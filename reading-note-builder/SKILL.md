---
name: reading-note-builder
description: "Explicit skill-use request only: top-level activation requires the user to explicitly ask to use, call, or apply a reading-note, PaperQuay-reading-note, 阅读笔记, or equivalent skill to a stated note task; the exact identifier is optional. An ordinary request to write or enhance a note is not authorization. An already authorized primary skill may invoke this skill as a bounded supporting dependency for the same goal; this does not create a new primary activation. Build a formal Obsidian reading note from a PaperQuay note and mapped MinerU正文缓存 with 导师七问、理解纠偏、正文校验, and note-to-paper mapping."
---

Read `scripts/build_reading_note.py` and run it with a real `--note-id`.

Workflow:
- Resolve the note from `paperquay-notes.sqlite`.
- Resolve the source paper with `anchors` first, then linked paper ids, then `note.paper_id`.
- Refuse generation when these sources disagree. Re-run with an explicit `--paper-id` only after inspecting the conflict report.
- Resolve the MinerU cache from `.mineru-cache`.
- Export the raw PaperQuay markdown import.
- Collect a structured evidence bundle for the current main model to read.
- Use the current skill-running model to write the final formal note; the script itself must not call another model.
- Keep the user's raw PaperQuay note at `Research/Papers/<short-name>/Support/original.md`.
- Never overwrite an existing `Support/original.md`; use it as the preserved user record.
- Write the final note to `Research/Papers/<short-name>/Reading/enhanced.md` after the current main model reads the external work bundle (`paper_summary.json`, `evidence_bundle.json`, `mapping_report.json`, and `writer_prompt.md`).
- Run `shared/obsidian/note_quality.py` after writing. The task is incomplete until the validator passes.

Rules:
- Treat `content_list_v2.json` and `full.md` as the正文 evidence layer.
- Do not trust `note.paper_id` alone for `ai-chat` notes.
- Treat PaperQuay authors, year, and venue as locator metadata, not authoritative bibliography. Verify them from the PDF title page or the first parsed page before writing frontmatter; record uncertainty instead of copying contradictory metadata.
- Keep output filenames short and stable; do not use long raw titles directly.
- Do not put evidence JSON, prompts, logs, or temporary reports in the Obsidian Vault. They belong under `%LOCALAPPDATA%/phd-learning-skills/work` (or `PHD_SKILL_WORK_ROOT`).
- If the cache is missing, still export the note, but mark the output as note-only.
- The final reading note should be organized around 导师七问 plus `你当前笔记的遗漏与纠偏`.
- The final reading note should borrow the rigor of a systems top-conference reviewer, but its first job is to correct and strengthen the user's note rather than attack the paper itself.
- `What is the design?` and `What is the experimental plan?` are the two most important questions and should receive the richest evidence-backed writing.
- Do not copy the raw note into the final note. First correct and strengthen the user note with正文 evidence, then fill the formal structure.
- Every correction in `你当前笔记的遗漏与纠偏` should point back to正文 evidence rather than intuition.

Default command:

```powershell
$env:PYTHONPATH="."
python reading-note-builder\scripts\build_reading_note.py --note-id <note_id>
```

When the report says `mapping-failed` because PaperQuay metadata conflicts with anchors, inspect the candidates and rerun explicitly:

```powershell
python reading-note-builder\scripts\build_reading_note.py --note-id <note_id> --paper-id <verified_paper_id>
```

After writing `enhanced.md`:

```powershell
python shared\obsidian\note_quality.py --kind reading --path <enhanced.md> --expected-title <paper-title> --expected-paper-id <verified-paper-id> --original <Support/original.md>
```
