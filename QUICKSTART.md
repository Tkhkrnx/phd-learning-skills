# Quickstart

## Requirements

- Python 3.11+
- [PaperQuay](https://github.com/WangQrkkk/PaperQuay)
- 一个可写的 Obsidian vault

以下命令默认在仓库根目录执行：

```powershell
pip install -r requirements.txt
$env:PYTHONPATH="."
```

## Weekly Radar

```powershell
python weekly-paper-radar\scripts\weekly_radar.py --candidate-pool-total 20 --weekly-target 10 --deep-read-target 4 --download-pdf
```

说明：

- 生成机器可读候选池
- 由主模型读取结果并直接在对话里给出“本周推荐 10 篇”和“建议细读 4 篇”
- 如果启用 `--download-pdf`，会同时返回下载成功列表和手动补链列表

## Topic Search

```powershell
python topic-paper-finder\scripts\topic_finder.py --query "hardware aware llm serving" --limit 5 --download-pdf
```

适合用户提供的信息：

- 具体问题或方向
- 若干关键词 / 子方向
- 目标会议、期刊或 venue 层级
- 年份范围
- 是否顺手下载 PDF

如果用户请求比较模糊，调用 skill 的主模型应先把它收敛成更精确的检索条件，再执行脚本。

## Reading Note Builder

```powershell
python reading-note-builder\scripts\build_reading_note.py --note-id <paperquay_note_id>
```

脚本会导出证据包，随后由主模型基于 `writer_prompt.md` 写正式 `enhanced.md`。

## Review Note Builder

```powershell
python review-note-builder\scripts\build_review_note.py --note-id <paperquay_note_id>
```

脚本同样只负责导出证据包；正式 review note 由主模型完成。

## Vault Note Search

```powershell
python vault-note-finder\scripts\find_notes.py --query "DSPARK"
```

## Notes

- `weekly-paper-radar` 和 `topic-paper-finder` 共享同一套搜索、恢复、去重和 PDF 下载底座。
- 若返回 `publisher_blocked_or_login_required`、`listing_page_only` 或 `pdf_not_found_manual_search_needed`，表示仍需用户手动补链。
- `reading-note-builder` 和 `review-note-builder` 的核心是“先收证据，再由当前主模型完成正式写作”，而不是脚本内部再调一个模型。
