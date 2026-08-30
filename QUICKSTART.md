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

必须明确说“使用某类 skill/技能处理某件事”才进入 skill；不必记住英文全名，自然语言类别即可：

```text
用问题定义的 skill 带我判断这个现象能否成为研究问题。
这个研究问题已经明确了，请用研究方法的 skill 先给我几个可行方案，再带我比较和 defend。
调用需求分析那个技能，带我读懂相关架构并选择第一执行切片。
用教学 skill 帮我真正弄懂 chunked prefill，并让我做一次迁移判断。
```

以下语义虽然分别对应四类能力，但没有明确要求“使用 skill”，因此必须按普通请求处理，不能触发：

```text
帮我分析一下这个需求，先澄清真实需求和验收标准，不要立即写代码。
我有一个研究想法，帮我判断它究竟是否构成学术问题。
这个研究问题已经明确了，但我不知道有什么好办法解决，带我一起设计。
这个概率是什么意思？请带我理解并让我用自己的话讲回来。
```

AI 可以先给完整候选问题、若干方案、系统模型或示范讲解，再通过聚焦的纠正、选择、复述、质疑或应用和你共同收敛。不是强迫用户从空白构造，也不是 AI 给完答案就自行宣布结束。进入执行、设计冻结或知识迁移前，双方应对关键结论达到约 90% 的把握，并明确仍未解决的不确定性。

问题定义和方法设计必须先获取证据。问题定义会先把候选表述当成检索假设，覆盖最接近工作和反证后再判断；方法设计会按根源挑战的结构特征同时搜索本领域、相邻领域、远距离类比和真实实现证据。搜索失败或覆盖不足时只能给临时判断，不能宣称“没人做过”或“这个方案最好”。

只需对顶层主 skill 做一次明确授权。同一目标内，主 skill 可以受限调用必要的辅助 skill，例如研究方法 skill 调用论文搜索 skill；辅助结果必须返回主 skill，由主 skill 继续和你交互。另起目标、切换主专家角色或进入普通执行不继承这项授权。

普通工作请求不会因为任务复杂或领域相关而触发这四个 skill。例如下面的请求应直接执行：

```text
按已经确认的方案同步实验计划、写作指南、论文和代码。
继续修复 action replay，并按冻结的实验方案收集结果。
修复这个 bug 并跑测试。
审阅这篇论文并给出修改意见。
解释这段代码在做什么。
```

一次显式授权可持续覆盖同一协作中的追问和回答，不必每轮重复。若切换到直接执行、换任务或协作已经完成，授权立即失效，skill 应静默退出且不能在以后自行恢复；切换到另一个 skill 也必须重新明确提出。

具体工作产物的说明不是教学流程。比如“说明一下 PR9 做了什么，我先了解后再审阅”应直接回答；只有用户要学习某个概念、原理、关系或机制，并明确希望自己复述或应用时，才进入 `targeted-knowledge-closure`。即使正确进入 skill，阶段名和运行状态也只在内部维护，不显示机器协议行。

修改这四个 skill 或其文献证据后端后，同步并验证五处安装副本：

```powershell
.\shared\scripts\sync_expert_skills.ps1
.\shared\scripts\sync_explicit_skill_policy.ps1
python shared\tests\validate_expert_skills.py
python shared\tests\validate_explicit_skill_policy.py
```

## Weekly Radar

```powershell
python weekly-paper-radar\scripts\weekly_radar.py --candidate-pool-total 20 --weekly-target 10 --deep-read-target 4 --download-pdf
```

## Topic Search

近三年 taxonomy-aligned 学习检索：

```powershell
python topic-paper-finder\scripts\topic_finder.py --mode study --query "hardware aware llm serving" --limit 5 --download-pdf
```

问题边界检索默认不设年份、venue 和 taxonomy 限制，可重复给查询：

```powershell
python topic-paper-finder\scripts\topic_finder.py --mode problem-boundary --query "state reuse tail latency agent inference" --query "context reuse overhead negative results"
```

跨领域机制启发检索：

```powershell
python topic-paper-finder\scripts\topic_finder.py --mode mechanism-inspiration --query "reversible resource activation delayed feedback control" --query "adaptive caching pressure tail latency"
```

## Reading Note Builder

```powershell
python reading-note-builder\scripts\build_reading_note.py --note-id <paperquay_note_id>
```

## Review Note Builder

```powershell
python review-note-builder\scripts\build_review_note.py --note-id <paperquay_note_id>
```

修改 reading/review builder 或其共享依赖后，同步并验证五处安装副本：

```powershell
.\shared\scripts\sync_paper_note_skills.ps1
python -m unittest discover -s tests -v
```

## Vault Note Search

```powershell
python vault-note-finder\scripts\find_notes.py --query "DSPARK"
```
