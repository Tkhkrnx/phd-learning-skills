---
name: reading-note-builder
description: Build a formal Obsidian reading note from a PaperQuay note and its mapped MinerU正文缓存. Use when Codex needs to convert a PaperQuay读书笔记 into a正式 Obsidian 阅读笔记, especially with 导师七问、理解纠偏、正文校验, and PaperQuay note-to-paper mapping.
---

Read `scripts/build_reading_note.py` and run it with a real `--note-id`.

Workflow:
- Resolve the note from `paperquay-notes.sqlite`.
- Resolve the source paper with `anchors` first, then linked paper ids, then `note.paper_id`.
- Resolve the MinerU cache from `.mineru-cache`.
- Export the raw PaperQuay markdown import.
- Collect a structured evidence bundle for the current main model to read.
- Use the current skill-running model to write the final formal note; the script itself must not call another model.
- The final note should be written into `enhanced.md` by the current main model after it reads `original.md`, `paper_summary.json`, `evidence_bundle.json`, `mapping_report.json`, and `writer_prompt.md`.

Rules:
- Treat `content_list_v2.json` and `full.md` as the正文 evidence layer.
- Do not trust `note.paper_id` alone for `ai-chat` notes.
- Keep output filenames short and stable; do not use long raw titles directly.
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
