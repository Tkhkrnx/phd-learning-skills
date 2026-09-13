---
name: vault-note-finder
description: Search the PhD Obsidian vault for existing reading or review notes when the user explicitly invokes this Skill.
---

Run `scripts/find_notes.py` to search the vault. Inspect its source only when modifying or debugging it.

Workflow:
- Search markdown files in the vault by filename and content.
- Rank reading/review notes slightly higher.
- Return the most relevant note paths.

Default command:

```powershell
$env:PYTHONPATH="."
python vault-note-finder\scripts\find_notes.py --query "DSPARK"
```
