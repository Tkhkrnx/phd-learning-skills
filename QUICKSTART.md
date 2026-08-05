# Quickstart

## Requirements

- Python 3.11+
- [PaperQuay](https://github.com/WangQrkkk/PaperQuay)
- 一个可写的 Obsidian vault

以下命令默认在仓库根目录执行：

```powershell
pip install -r requirements.txt
$env:PYTHONPATH="."
$env:PAPERQUAY_DATA_DIR="$HOME\\Documents\\PHR\\Intellistream\\papers\\read"
```

## Weekly Radar

```powershell
python weekly-paper-radar\scripts\weekly_radar.py --candidate-pool-total 20 --weekly-target 10 --deep-read-target 4 --download-pdf
```

## Topic Search

```powershell
python topic-paper-finder\scripts\topic_finder.py --query "hardware aware llm serving" --limit 5 --download-pdf
```

## Reading Note Builder

```powershell
python reading-note-builder\scripts\build_reading_note.py --note-id <paperquay_note_id>
```

## Review Note Builder

```powershell
python review-note-builder\scripts\build_review_note.py --note-id <paperquay_note_id>
```

## Vault Note Search

```powershell
python vault-note-finder\scripts\find_notes.py --query "DSPARK"
```
