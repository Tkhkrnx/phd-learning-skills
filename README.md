# PhD Learning Skills

This repository now contains three skill families:

1. expert-facing PhD collaboration skills
2. paper discovery, note-building, and validation workflow skills
3. systems and HPC paper-writing skills

## Explicit Invocation Policy

Every task skill in this repository disables Codex implicit invocation through `agents/openai.yaml`. This uses the documented [`policy.allow_implicit_invocation`](https://developers.openai.com/codex/skills) control. The only implicitly discoverable component is `explicit-skill-router`, whose sole job is to recognize a meta-level request to use a skill and route a plain-language label to the protected target.

The policy deployment also protects the installed `cs-paper-submission-check`, `planning-with-files`, and `scipilot-figure-skill` copies when present, plus the planning command aliases. Those optional skills retain their own source bodies; the deployment guard adds explicit-only metadata and, on non-Codex mirrors, an explicit-use-only description prefix.

The user does not need to remember an exact identifier. “Use the research-method skill”, “调用问题定义那个技能”, “用需求分析 skill”, and “用教学技能” are valid when they also identify the task. By contrast, “find a method”, “judge whether this is an academic problem”, “analyze this requirement”, and “teach me this concept” are ordinary requests and must not activate a skill. A generic “use a suitable skill” is ambiguous and must not be resolved from task semantics.

Authorization covers follow-up interaction within the stated task, so the user need not repeat it every round. It expires on completion, a task change, or a pivot to normal writing, coding, synchronization, debugging, review, experiment execution, or delivery. It never transfers automatically to another skill.

## Expert-Facing Collaboration Skills

These four skills are designed to solve real work while improving the user's own research, engineering, and learning ability:

- `research-problem-formulation`
- `research-method-design`
- `engineering-task-decomposition`
- `targeted-knowledge-closure`

They are user-facing collaboration protocols, not agent-only planning or execution checklists. Activation requires an explicit request to use a recognizable kind of skill for the stated task; exact identifiers are optional, but the underlying collaboration request alone is not authorization. Direct writing, reviewing, coding, synchronization, debugging, experiment execution, or plan execution must bypass this family.

The expert may lead with a complete candidate problem statement, several feasible methods, a system model, or a worked explanation. The Skill asks for a focused reaction only when a user-owned decision or missing observation could materially change the result. Candidate conclusions remain provisional while such uncertainty is open; otherwise the agent proceeds. Stage names, statuses, and lifecycle markers stay internal. If the user pivots to direct execution, the Skill preserves confirmed decisions and exits silently.

The two research skills are evidence-first. `research-problem-formulation` treats the first framing as a search hypothesis and cannot freeze reality, importance, or unresolved status until a query portfolio, decisive primary sources, closest solution families, counterevidence, and material blind spots have been checked. `research-method-design` searches by the root challenge's structural signature across the same field, adjacent systems areas, distant analogies, implementation artifacts, and negative evidence before ranking methods. The agent performs retrieval and triage and presents only decision-changing evidence.

Explicit authorization applies to the primary skill, not to every internal dependency. During that same authorized goal, the primary skill may invoke a bounded supporting skill when needed—for example, method design may call `topic-paper-finder` for academic candidate discovery. The primary skill keeps ownership of the conversation and integrates the result; the supporting skill does not start an independent goal or lifecycle. Switching the primary expert role or starting a different task still requires a new explicit skill request.

Trigger examples:

Evidence-led collaboration starts with source investigation and accessible explanation, then uses focused user discussion to revise the actual account. Method design follows the problem through existing-method failures, core challenges, transferable principles, adapted elements, an integrated solution and discriminating evidence. The research target remains systems/architecture/LLM inference and serving; inspiration can cross disciplines and the resulting method need not be a new system mechanism. Three challenges are common, never a quota.

Preserve the user's requested headings, order, language and source wording during delivery. Abstract-level background and problem definitions should be concise paper-quality paragraphs. Formatting and handoffs must not silently change the agreed research claim or its evidence status.

| User intent | Behavior |
|---|---|
| "请用需求分析的 skill 把这个需求弄清楚，先别写代码" | `engineering-task-decomposition` |
| "用问题定义那个技能判断这个研究想法是否构成学术问题" | `research-problem-formulation` |
| "问题已经明确，请用研究方法的 skill 带我找一个可辩护的解决方法" | `research-method-design` |
| "用教学 skill 带我真正弄懂这个概率" | `targeted-knowledge-closure` |
| "帮我分析一下这个需求，先别写代码" | no skill; analyze normally |
| "这个问题已经明确，带我找一个解决方法" | no skill; assist normally |
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
  - resolves material requirement and system-boundary uncertainty before a consequential handoff
  - converges on:
    - real requirement, non-goals, and acceptance evidence
    - real codebase and runtime understanding
    - best current implementation path and rejected alternatives
    - first reversible execution slice
    - validation, observability, and rollback
- `targeted-knowledge-closure`
  - acts like a subject-matter teacher with scaffolding discipline
  - adapts through explanation, correction, and transfer only as far as the live learning goal requires
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

The discovery and analysis tools can be used separately:

1. search papers
2. download PDFs into the local paper directory when possible
3. read the paper directly; optionally add a Typora/Markdown note and presentation
4. build a seven-question speaking note, or use the review workflow in two stages: a presentation-ready analysis note first, then a formal reviewer report after the presentation and discussion
5. verify LaTeX references against authoritative sources and generate a Chinese PDF validation report

## Default PDF Directory

默认 PDF 下载目录：

- `~/Documents/PHR/Intellistream/papers/read`

可用环境变量覆盖：

- `PAPERQUAY_DATA_DIR`
- `PHD_PAPER_SUBMISSION_DIR`

## Dependency

`reading-note-builder` 与 `review-note-builder` 不依赖 PaperQuay、MinerU 或 Obsidian。论文 PDF/全文 Markdown 是事实依据；用户 Markdown 笔记和 PPT 都是可选材料。PaperQuay 仍可用于个人阅读与旧资料定位，不再是这两个 Skill 的入口。

本地资料清单脚本接受 `--paper`、可选 `--note` 和 `--pptx`；最终文稿由当前模型完成，并对照论文、PPT 和用户最新判断审读。阅读笔记的前五问形成“问题—重要性—现有工作缺口—核心想法—设计”的讲述链，实验设置与图表目的/结论另列证据地图，第六问整理写作和内容细节，第七问总结证据支持的结论。审稿分析采用不同的五问：“问题定义—重要性—现有工作—核心想法—实验是否支撑结论”；在每一问中都要写出评审判断，实验设置与图表证据地图放在第五问内，第六问检查写作、术语与展示细节，最后给整体判断。

`review-note-builder` 分两阶段运行。第一阶段只生成可直接用于准备 PPT 的分析笔记；第二阶段在用户汇报和讨论后，使用其 PPT、讨论结论及用户修改过的分析笔记生成正式审稿意见。阶段之间由用户自行推进，不强制插入讨论或确认回合。

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

- 从论文本身出发，以七问组织可支撑 PPT 讲述的增强笔记；Markdown 笔记和 PPT 可选
- 前五问遵循问题定义和方法设计的推理要求；实验设置适度展开，并将每个相关图表映射到实验目的和它支持的结论
- 第六问检查写作、术语、方程、表格、引用和交叉引用，区分影响论证/汇报的主要问题与次要润色；第七问收束证据支持的结论
- 只纠正用户实际表达过的误解，不强制生成“遗漏与纠偏”章节

### `review-note-builder`

- 阶段一按系统论文五问评审：问题定义、重要性、现有工作、核心想法、实验是否支撑结论；各问都须明确写出评审意见，而不只是复述论文
- 实验设置和图表证据地图放在第五问中；第六问检查写作、术语、表格、引用与交叉引用，并把影响接收判断的问题和次要修订分开
- 提供最终 PPT 时，笔记需达到足以重建其中问题、论证、方法和证据的表达深度；同时补上 PPT 漏掉但有证据支持的评审意见
- 阶段二在用户汇报和讨论后，读取 PPT、讨论/导师结论及用户修改过的分析笔记，生成正式审稿意见
- 最新讨论结论决定评审重点和立场，论文原文核验事实；保留原文术语、因果和证据限定，对已确认缺陷、说明不足、待验证解释和可选增强分别措辞
- 阶段由用户推进，Skill 不强制增加讨论回合，也不会默认在阶段一同时生成正式意见

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
python shared\tests\validate_explicit_skill_policy.py
```

Synchronize the four expert skills, the evidence-oriented paper finder, and their shared dependency closure to both local Codex skill roots, global Claude Code, and both Obsidian Claudian mirrors with:

```powershell
.\shared\scripts\sync_expert_skills.ps1
.\shared\scripts\sync_explicit_skill_policy.ps1
```

Codex uses `allow_implicit_invocation: false` for every protected task Skill. Short descriptions state only the discriminating capability; the narrow alias router handles explicit plain-language requests. Optional external Skills and migrated command adapters keep their upstream bodies, while deployed copies receive explicit-only metadata and a short description prefix for clients that do not honor Codex metadata. Restart an already-open client or start a new task after deployment if its Skill catalog was loaded before the update.

## Quickstart

For commands and workflow examples, see [QUICKSTART.md](./QUICKSTART.md).
