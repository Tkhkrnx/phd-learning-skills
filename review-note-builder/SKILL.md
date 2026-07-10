---
name: review-note-builder
description: Build a strict Obsidian review note from a PaperQuay审稿笔记 and its mapped MinerU正文缓存. Use when Codex needs to convert a PaperQuay review draft into a更严苛、更完整的正式审稿笔记 with缺陷补抓、证据校验、rebuttal-sensitive points, and mapping diagnostics.
---

Read `scripts/build_review_note.py` and run it with a real `--note-id`.

Workflow:
- Resolve the note from `paperquay-notes.sqlite`.
- Resolve the paper through anchors-first mapping.
- Resolve `.mineru-cache` and bind the review to the正文 evidence source.
- Export the raw import note.
- Collect a structured evidence bundle for the current main model to read.
- Use the current skill-running model to write the final formal review; the script itself must not call another model.
- The final review should be written into `enhanced.md` by the current main model after it reads `original.md`, `paper_summary.json`, `evidence_bundle.json`, `mapping_report.json`, and `writer_prompt.md`.
- The model should first build an internal seven-question understanding of the paper, then translate that understanding into the review submission structure.

Rules:
- Prioritize evidence-backed weaknesses, missing evaluations, and threats to validity.
- Explicitly note when the current review is too strong, too weak, or unsupported.
- Keep filenames short and stable.
- If正文 cache is unavailable, keep the output but mark it as note-only.
- Every important criticism must be traceable back to正文 Markdown evidence.
- Focus on main-paper evidence first; Appendix is not the default battlefield.
- The internal seven-question understanding used by review should match the reading-note workflow in depth, coverage, and rigor before it is translated into review structure.
- Review should be written from a systems top-conference reviewer perspective: strict, skeptical, rigorous, detailed, and careful about evidence boundaries.
- The final review should not merely restate the raw review draft. It should re-check, tighten, and supplement it from正文 evidence.
- The review workflow should share the same deep understanding backbone as the reading-note workflow; the difference is the final output format, not the evidence standard.

Default command:

```powershell
$env:PYTHONPATH="."
python review-note-builder\scripts\build_review_note.py --note-id <note_id>
```
