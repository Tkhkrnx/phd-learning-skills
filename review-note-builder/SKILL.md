---
name: review-note-builder
description: Build a strict Obsidian review note from a PaperQuay审稿笔记 and its mapped MinerU正文缓存. Use when Codex needs to convert a PaperQuay review draft into a更严苛、更完整的正式审稿笔记 with缺陷补抓、证据校验、rebuttal-sensitive points, and mapping diagnostics.
---

Read `scripts/build_review_note.py` and run it with a real `--note-id`.

Workflow:
- Resolve the note from `paperquay-notes.sqlite`.
- Resolve the paper through anchors-first mapping.
- Refuse generation when note metadata conflicts with anchors unless the operator supplies a verified explicit `--paper-id`.
- Resolve `.mineru-cache` and bind the review to the正文 evidence source.
- Export the raw import note.
- Collect a structured evidence bundle for the current main model to read.
- Use the current skill-running model to write the final formal review; the script itself must not call another model.
- Support both PaperQuay-note mode and paper-only/local-draft mode. Use `--paper-id` with optional `--source-note` when PaperQuay has no review note.
- Keep a supplied local draft at `Research/Papers/<short-name>/Support/review_draft.md` and write the final review to `Research/Papers/<short-name>/Review/enhanced.md`.
- Store evidence bundles outside the Vault under `%LOCALAPPDATA%/phd-learning-skills/work` (or `PHD_SKILL_WORK_ROOT`).
- Run `shared/obsidian/note_quality.py` after writing. The task is incomplete until the validator passes.
- The model should first build an internal seven-question understanding of the paper, then translate that understanding into the review submission structure.

Rules:
- Prioritize evidence-backed weaknesses, missing evaluations, and threats to validity.
- Explicitly note when the current review is too strong, too weak, or unsupported.
- Keep filenames short and stable.
- If正文 cache is unavailable, keep the output but mark it as note-only.
- Every important criticism must be traceable back to正文 Markdown evidence.
- Treat PaperQuay authors, year, and venue as locator metadata only. Verify frontmatter bibliography from the PDF title page or the first parsed page; never copy contradictory library metadata into the final review.
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

Paper-only or local-draft mode:

```powershell
python review-note-builder\scripts\build_review_note.py --paper-id <paper_id> --source-note <draft.md>
```

After writing `enhanced.md`:

```powershell
python shared\obsidian\note_quality.py --kind review --path <enhanced.md> --expected-title <paper-title> --expected-paper-id <verified-paper-id> --original <Support/review_draft.md>
```
