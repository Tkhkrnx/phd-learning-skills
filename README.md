# PhD Learning Skills

This repository now contains three skill families:

1. expert-facing PhD collaboration skills
2. paper discovery, note-building, and validation workflow skills
3. systems and HPC paper-writing skills

## Expert-Facing Collaboration Skills

These four skills are designed to solve real work while improving the user's own research, engineering, and learning ability:

- `research-problem-formulation`
- `research-method-design`
- `engineering-task-decomposition`
- `targeted-knowledge-closure`

They are user-facing collaboration protocols, not agent-only planning or execution checklists. Activation requires a clear matching intent, but the user does not have to spell the skill name: asking to analyze a requirement, judge a research idea as an academic problem, design a method for an established problem, or learn one specific concept is sufficient. Topic similarity and task complexity are not sufficient. Direct writing, reviewing, coding, synchronization, debugging, experiment execution, or plan execution must bypass this family.

The expert may lead with a complete candidate problem statement, several feasible methods, a system model, or a worked explanation. That candidate remains provisional: the skill must invite a focused reaction, update its model from the user's correction, evidence, choice, restatement, challenge, or application, and continue until the important uncertainty is closed. The practical exit gate is about 90% shared confidence in the skill's target outcome, with residual uncertainty stated explicitly. This is an operational readiness threshold, not a calibrated probability. Stage names, statuses, and lifecycle markers stay internal so the conversation remains natural. If the user pivots to direct execution, the skill preserves confirmed decisions and exits silently.

The two research skills are evidence-first. `research-problem-formulation` treats the first framing as a search hypothesis and cannot freeze reality, importance, or unresolved status until a query portfolio, decisive primary sources, closest solution families, counterevidence, and material blind spots have been checked. `research-method-design` searches by the root challenge's structural signature across the same field, adjacent systems areas, distant analogies, implementation artifacts, and negative evidence before ranking methods. The agent performs retrieval and triage, presents only decision-changing evidence, and still requires the user's reasoned challenge or correction before convergence.

Trigger examples:

| User intent | Behavior |
|---|---|
| "帮我分析一下这个需求，先别写代码" | `engineering-task-decomposition` |
| "我有一个研究想法，帮我判断它是否构成学术问题" | `research-problem-formulation` |
| "这个问题已经明确了，带我一起找一个可辩护的解决方法" | `research-method-design` |
| "这个概率是什么意思？带我真正弄懂" | `targeted-knowledge-closure` |
| "说明一下 PR9 做了什么，我先了解后再审阅" | no expert collaboration skill; explain the concrete artifact directly |
| "继续修复 replay，并按冻结方案收集结果" | no research-method skill; execute the established method normally |
| "按已经确认的方案同步实验计划、论文和代码" | no expert collaboration skill; execute normally |

They are intentionally expert-role skills, not generic templates:

- `research-problem-formulation`
  - acts like an LLM inference systems domain expert
  - searches seminal/current literature, closest work, failure cases, and counterevidence before concluding
  - converges on:
    - what the problem is
    - why it matters
    - why existing work still fails
- `research-method-design`
  - acts like a systems-method and experiment-design expert
  - activates only after the research problem is stable and the user explicitly asks to discover, compare, or defend solution directions
  - searches papers, repositories, documentation, engineering evidence, and structurally analogous mechanisms beyond the target field
  - converges on:
    - root challenge and boundary conditions
    - causal mechanism and feasible system carrier
    - transferable principles from relevant or cross-domain work
    - alternatives, trade-offs, assumptions, and system costs
    - kill criterion
    - first discriminating experiment
- `engineering-task-decomposition`
  - acts like a senior engineer or architect
  - keeps interacting until the agent understands the real need and the user understands the consequential system boundaries at roughly the 90% readiness threshold
  - converges on:
    - real requirement, non-goals, and acceptance evidence
    - real codebase and runtime understanding
    - best current implementation path and rejected alternatives
    - first reversible execution slice
    - validation, observability, and rollback
- `targeted-knowledge-closure`
  - acts like a subject-matter teacher with scaffolding discipline
  - may explain first, then adapts through reconstruction, correction, and transfer until roughly 90% learning confidence
  - converges on:
    - accurate mental model and repaired prerequisites
    - user reconstruction in their own words
    - discrimination from near-miss concepts
    - small transfer into the live task
    - reduced scaffolding on the next similar case

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
- `reference-validation-report`

Its goal is to stabilize this chain:

1. search papers
2. download PDFs into the local paper directory when possible
3. read and annotate in PaperQuay
4. turn PaperQuay notes plus MinerU cache into formal Obsidian reading or review notes
5. verify LaTeX references against authoritative sources and generate a Chinese PDF validation report

## Default PDF Directory

默认 PDF 下载目录：

- `~/Documents/PHR/Intellistream/papers/read`

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

- 提供 `study`、`problem-boundary`、`mechanism-inspiration` 三种模式
- `study` 保留近三年、固定 taxonomy 和 venue 策略；两个证据模式默认不限制年份、venue 或现有 taxonomy
- 支持重复 `--query` 构造查询组合、跨查询去重并记录 `matched_queries`
- 证据模式在可用时合并 Semantic Scholar、OpenAlex、DBLP 和 arXiv，并记录来源覆盖与失败
- 搜索目标论文并可选下载 PDF
- 学习模式做 vault 重复抑制；证据模式保留已有笔记对应论文并标注，避免丢掉关键 prior work
- 返回结构化 JSON，由主模型直接在对话里总结结果
- 只负责学术候选发现；关键结论仍需打开原文，仓库、文档、issue、博客等由方法设计流程另行检索

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

### `reference-validation-report`

- verifies bibliography entries against DOI/Crossref, arXiv, and official publisher or venue sources
- produces an evidence-backed Chinese PDF report and never marks unresolved items as confirmed
- supports standard `.bib + .bbl + .tex`, Elsevier-style `.bbl`, and inline `thebibliography` inputs

## Output Contract

`weekly-paper-radar` 和 `topic-paper-finder` 都遵循同一个约定：

- 脚本只产出结构化 JSON
- 最终推荐或搜索结论由 Codex/Claude 在对话里直接告诉用户
- 回答时应显式总结：
  - 成功下载了哪些 PDF
  - 实际写入的本地论文目录是什么
  - 哪些论文仍需用户手动补链

## Validation

The redesign validation checklist and paired activation/bypass cases for the expert-facing skills live in:

- [shared/tests/expert_skill_validation.md](./shared/tests/expert_skill_validation.md)

Run the static contract and regression-case validator with:

```powershell
python shared\tests\validate_expert_skills.py
```

Synchronize the four expert skills, the evidence-oriented paper finder, and their shared dependency closure to both local Codex skill roots, global Claude Code, and both Obsidian Claudian mirrors with:

```powershell
.\shared\scripts\sync_expert_skills.ps1
```

Codex and Claude discover the same narrow descriptions. Implicit discovery remains enabled so a clear natural-language collaboration intent can activate the right expert; the paired bypass cases prevent ordinary execution from becoming a skill run. Restart an already-open client or task after deployment if its skill catalog was loaded before the update.

## Quickstart

For commands and workflow examples, see [QUICKSTART.md](./QUICKSTART.md).
