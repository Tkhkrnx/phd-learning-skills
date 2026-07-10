---
name: vault-note-finder
description: Search existing Obsidian reading and review notes for the PhD paper workflow. Use when Codex needs to find prior notes, drafts, or related markdown already in the vault before creating or enhancing new paper notes.
---

Read `scripts/find_notes.py` and search the vault directly.

Workflow:
- Search markdown files in the vault by filename and content.
- Rank reading/review notes slightly higher.
- Return the most relevant note paths.

Default command:

```powershell
$env:PYTHONPATH="."
python vault-note-finder\scripts\find_notes.py --query "DSPARK"
```
