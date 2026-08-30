---
name: vault-note-finder
description: "Explicit skill-use request only: top-level activation requires the user to explicitly ask to use, call, or apply a vault-note, Obsidian-note-search, 笔记搜索, or equivalent skill to a stated task; the exact identifier is optional. An ordinary request to find a note is not authorization. An already authorized primary skill may invoke this skill as a bounded supporting dependency for the same goal; this does not create a new primary activation. Search existing Obsidian reading and review notes for prior notes, drafts, or related markdown in the PhD paper workflow."
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
