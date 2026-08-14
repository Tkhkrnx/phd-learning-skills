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

## Expert Collaboration Skills

明确表达对应的协作意图时进入 skill；不必念出 skill 名称：

```text
用 research-problem-formulation 带我一起判断这个现象能否成为研究问题。
用 research-method-design 带我一起 defend 这个机制，不要直接替我写完整方案。
用 engineering-task-decomposition 带我读懂相关架构并选择第一执行切片。
用 targeted-knowledge-closure 帮我真正弄懂 chunked prefill，并让我做一次迁移判断。
帮我分析一下这个需求，先澄清真实需求和验收标准，不要立即写代码。
我有一个研究想法，帮我判断它究竟是否构成学术问题。
这个研究问题已经明确了，但我不知道有什么好办法解决，带我一起设计。
这个概率是什么意思？请带我理解并让我用自己的话讲回来。
```

每轮只推进一个阶段，AI 提出一个开放式问题并等待你展开推理；是/否和裸选项不算完成该轮。

普通工作请求不会因为任务复杂或领域相关而触发这四个 skill。例如下面的请求应直接执行：

```text
按已经确认的方案同步实验计划、写作指南、论文和代码。
修复这个 bug 并跑测试。
审阅这篇论文并给出修改意见。
解释这段代码在做什么。
```

若在协作过程中切换到直接执行，只需直接提出执行要求。skill 应静默退出，不输出暂停或运行结果标记。

修改这四个 skill 后，同步并验证四处安装副本：

```powershell
.\shared\scripts\sync_expert_skills.ps1
python shared\tests\validate_expert_skills.py
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
