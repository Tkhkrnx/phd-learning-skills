# PhD Learning Skills

This repository now contains three skill families:

1. expert-facing PhD collaboration skills
2. paper discovery and note-building workflow skills
3. systems and HPC paper-writing skills

## Expert-Facing Collaboration Skills

These four skills are designed to solve real work while improving the user's own research, engineering, and learning ability:

- `research-problem-formulation`
- `research-method-design`
- `engineering-task-decomposition`
- `targeted-knowledge-closure`

They are intentionally expert-role skills, not generic templates:

- `research-problem-formulation`
  - acts like an LLM inference systems domain expert
  - converges on:
    - what the problem is
    - why it matters
    - why existing work still fails
- `research-method-design`
  - acts like a systems-method and experiment-design expert
  - converges on:
    - mechanism
    - alternatives
    - trade-offs
    - kill criterion
- `engineering-task-decomposition`
  - acts like a senior engineer or architect
  - converges on:
    - real codebase understanding
    - best current implementation path
    - first execution slice
- `targeted-knowledge-closure`
  - acts like a subject-matter teacher with scaffolding discipline
  - converges on:
    - real concept understanding
    - user restatement
    - small transfer

The design blueprint lives in [AGENT_COLLABORATION_SKILL_BLUEPRINT.md](./AGENT_COLLABORATION_SKILL_BLUEPRINT.md).

The LLM inference layer framework used by the research skills lives in [shared/expert-skill-references/llm_inference_three_layer_framework.md](./shared/expert-skill-references/llm_inference_three_layer_framework.md).

## Systems and HPC Paper-Writing Skills

- `systems-paper-writing`: structure, draft, revise, and audit systems papers for venues such as OSDI, SOSP, EuroSys, ATC, and NSDI. It enforces a problem → mechanism → evidence argument chain.
- `hpc-paper-writing`: structure, draft, revise, and audit HPC papers for venues such as SC, PPoPP, ICS, and HPDC. It enforces a profiling → optimization → hardware-limit evidence chain.

Each skill includes the supplied source guide as a local reference so detailed writing and submission checks remain available without external access.

## Paper Workflow Skills

The existing paper workflow family remains in the repository:

- `weekly-paper-radar`
- `topic-paper-finder`
- `vault-note-finder`
- `reading-note-builder`
- `review-note-builder`

Its goal is to stabilize this chain:

1. search papers
2. download PDFs into the local paper directory when possible
3. read and annotate in PaperQuay
4. turn PaperQuay notes plus MinerU cache into formal Obsidian reading or review notes

## Default PDF Directory

默认 PDF 下载目录：

- `~/Documents/PHR/Intellistream/papers/submission`

可用环境变量覆盖：

- `PAPERQUAY_DATA_DIR`
- `PHD_PAPER_SUBMISSION_DIR`

## Dependency

本仓库默认依赖 [PaperQuay](https://github.com/WangQrkkk/PaperQuay) 作为阅读、标注和正文缓存来源。

主要输入包括：

- `paperquay-notes.sqlite`
- `paperquay-library.sqlite`
- `.mineru-cache/document-*/full.md`
- `.mineru-cache/document-*/content_list_v2.json`

本仓库不再负责旧式 `paper-ingest` / `paper-translate` 流水线。

## Paper-Workflow Skill Details

### `weekly-paper-radar`

- 面向近 3 年论文做每周雷达搜索
- 覆盖 3 个固定研究方向
- 优先官方会议页面，再走聚合恢复链路
- 只产出机器可读候选池，最终推荐由调用 skill 的主模型在对话里给出

### `topic-paper-finder`

- 把模糊需求收敛成关键词、venue、年份窗口
- 搜索目标论文并可选下载 PDF
- 自动结合 `vault-note-finder` 做重复抑制
- 返回结构化 JSON，由主模型直接在对话里总结结果

### `vault-note-finder`

- 在 Obsidian vault 内搜索已有阅读笔记、审稿笔记和相关草稿
- 优先把正式 Reading / Review Notes 排到前面

### `reading-note-builder`

- 从 PaperQuay 阅读笔记出发，映射到对应论文和 MinerU 正文缓存
- 导出 `original.md`、`evidence_bundle.json`、`paper_summary.json`、`mapping_report.json`、`writer_prompt.md`
- 由当前执行 skill 的主模型完成正式 `enhanced.md`

### `review-note-builder`

- 从 PaperQuay 审稿笔记出发，先完成内部七问式增强理解，再转成正式 review 结构
- 所有关键批评都必须可回指到正文 Markdown 证据

## Output Contract

`weekly-paper-radar` 和 `topic-paper-finder` 都遵循同一个约定：

- 脚本只产出结构化 JSON
- 最终推荐或搜索结论由 Codex/Claude 在对话里直接告诉用户
- 回答时应显式总结：
  - 成功下载了哪些 PDF
  - 实际写入的本地论文目录是什么
  - 哪些论文仍需用户手动补链

## Validation

The redesign validation checklist for the expert-facing skills lives in:

- [shared/tests/expert_skill_validation.md](./shared/tests/expert_skill_validation.md)

## Quickstart

For commands and workflow examples, see [QUICKSTART.md](./QUICKSTART.md).
