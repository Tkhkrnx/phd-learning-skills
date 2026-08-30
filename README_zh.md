# PhD Learning Skills

这个仓库现在包含三类 skill：

1. 面向博士研究/工程/学习协作的 expert skill
2. 面向论文发现、笔记增强与参考文献核验的论文工作流 skill
3. 面向系统与高性能计算顶会写作的论文写作 skill

## 显式调用总规则

仓库中的每一个任务 skill 都通过 `agents/openai.yaml` 关闭 Codex 隐式调用，使用的是官方文档中的 [`policy.allow_implicit_invocation`](https://developers.openai.com/codex/skills)。唯一允许被隐式发现的是窄路由 `explicit-skill-router`：它不做领域任务，只在用户明确说“要使用某类 skill/技能处理某件事”时，把自然语言称呼映射到受保护的目标 skill。

部署脚本还会在本机存在时保护 `cs-paper-submission-check`、`planning-with-files`、`scipilot-figure-skill` 以及规划命令别名。它们的原有能力正文不被替换，只补充显式调用策略；在不识别 Codex 元数据的镜像中，还会给描述加上“仅显式要求 skill 才能使用”的前缀。

用户不必记住英文全名。“用研究方法的 skill”“调用问题定义那个技能”“用需求分析 skill”“用教学技能”都可以，只要同时说明要处理的任务。相反，“帮我找方法”“判断这是不是学术问题”“分析这个需求”“带我学会这个概念”只是普通任务请求，绝不能触发 skill。“用一个合适的 skill”没有说明类型，模型也不能根据任务内容擅自选择。

一次显式授权可以覆盖同一协作任务里的后续交互，不必每轮重复。但协作完成、换任务，或切换到写作、编码、同步、调试、审阅、跑实验和交付等普通执行时，授权立即失效；它也不能自动传递给另一个 skill。

## 一、Expert Skill

这四个 skill 是按“不同任务对应不同专家角色”的原则设计的，不再是统一模板：

- `research-problem-formulation`
  - 扮演大模型推理系统领域专家
  - 第一个问题表述只是检索假设；必须先覆盖奠基工作、最新工作、最接近方案、失败案例和反证，再判断问题是否真实、重要且尚未解决
  - 最终必须逼近三件事：
    - 问题定义是什么
    - 为什么重要
    - 现有工作为什么还失败
- `research-method-design`
  - 扮演系统方法设计与实验设计专家
  - 只有在研究问题已经稳定、用户明确要求寻找、比较或论证解决方案时才触发
  - 先把根源挑战表示为结构特征，再跨本领域、相邻系统领域、远距离类比、代码/文档/issue/benchmark/工程文章和负面证据寻找机制
  - 重点收敛到：
    - 根源挑战和适用边界
    - 因果机制及可落地的系统载体
    - 相关工作或跨领域启发中的可迁移原理
    - 替代方案、trade-off、假设和系统成本
    - kill criterion
    - 第一个判别性实验
- `engineering-task-decomposition`
  - 扮演资深工程师 / 架构师
  - 通过持续交互，让模型对真实需求的理解以及用户对关键系统边界的理解都达到约 90% 的可执行把握
  - 重点收敛到：
    - 真实需求、非目标和验收证据
    - 真正理解代码、运行路径和系统边界
    - 当前最优实现路径及被拒绝的替代方案
    - 第一可逆执行切片
    - 验证、可观测性和回滚边界
- `targeted-knowledge-closure`
  - 扮演懂内容也懂教学法的导师
  - 可以先讲解，再通过重构、纠偏和迁移把用户的理解推进到约 90% 的可应用把握
  - 重点收敛到：
    - 准确心智模型和前置知识修复
    - 用自己的话独立重构
    - 与近似概念或常见误解进行辨析
    - 迁移到当前任务中的小案例
    - 在下一次相似问题中减少脚手架依赖

这四个 skill 是用户可见的协作协议，不是模型自己的任务拆解或执行清单。触发条件是用户明确要求“使用某类 skill/技能”处理当前任务；不要求念出英文全名，但仅仅提出“分析/澄清需求”“判断学术问题”“设计方法”或“弄懂概念”仍属于普通请求，不能触发。

专家可以先给出完整的候选问题陈述、若干可行方案、系统模型或示范讲解，用户不必先从空白开始构造。但这些答案只能是待检验候选：skill 必须邀请用户做一次聚焦的纠正、补证、选择、复述、质疑或应用，并根据反馈更新判断，直到关键不确定性被消除。退出前应达到约 90% 的共同把握，并明确剩余不确定性；这里的 90% 是可执行/可迁移门槛，不是统计概率。阶段名、状态和生命周期标记只在内部维护，正常对话不得显示机器协议行。直接写作、审阅、同步、编码、调试、跑实验、修 replay 或执行已冻结方案必须走普通执行流程。若用户从协作切换到直接执行，skill 只保留已确认结论并静默退出。

两个研究 skill 共享“证据先于结论”的硬门槛。模型负责扩展查询、检索、追踪引用和整理证据，不把可查事实反问给用户；但只能向用户压缩呈现真正改变边界或方案排序的证据，并通过用户对边界、因果、假设和 trade-off 的质疑或修正共同收敛。搜索失败、原文打不开或关键查询族未覆盖时，不得把空结果说成创新性，也不得冻结“尚未解决”或“方案最优”的判断。

“必须明确要求使用 skill”限制的是顶层主 skill，不是每一个内部依赖。同一项已授权目标内，主 skill 可以按需受限调用辅助 skill，例如研究方法设计调用 `topic-paper-finder` 建立论文候选池。主 skill 始终负责对话、判断和结果整合；辅助 skill 不另起目标、不接管交互、不保留独立生命周期。若要切换主专家角色或开始另一项任务，仍须用户重新明确要求使用对应类型的 skill。

典型边界：

| 用户意图 | 应有行为 |
|---|---|
| “请用需求分析的 skill 把这个需求弄清楚，先别写代码” | 调用 `engineering-task-decomposition` |
| “用问题定义那个技能判断这个研究想法是否构成学术问题” | 调用 `research-problem-formulation` |
| “问题已经明确，请用研究方法的 skill 带我找一个可辩护的解决方法” | 调用 `research-method-design` |
| “用教学 skill 带我真正弄懂这个概率” | 调用 `targeted-knowledge-closure` |
| “帮我分析一下这个需求，先别写代码” | 不调用 skill，普通分析 |
| “这个问题已经明确，带我找一个解决方法” | 不调用 skill，普通协助 |
| “说明一下 PR9 做了什么，我先了解后再审阅” | 不调用教学 skill，直接解释具体工作产物 |
| “继续修复 replay，并按冻结方案收集结果” | 不调用方法设计 skill，直接执行既定方法 |
| “按已经确认的方案同步实验计划、论文和代码” | 不调用这四个 skill，直接执行 |

这套 expert skill 的总蓝图见：

- [AGENT_COLLABORATION_SKILL_BLUEPRINT.md](./AGENT_COLLABORATION_SKILL_BLUEPRINT.md)

研究问题和方法设计会用到的大模型推理系统三层框架见：

- [shared/expert-skill-references/llm_inference_three_layer_framework.md](./shared/expert-skill-references/llm_inference_three_layer_framework.md)

两者共同遵循的证据获取协议见：

- [shared/expert-skill-references/research_evidence_acquisition.md](./shared/expert-skill-references/research_evidence_acquisition.md)

其中三层是：

- 请求组织与调度
- 状态管理与复用
- 执行路径优化与验证

注意第二层和第三层可以天然交叉，不应强行切开。

## 二、系统与 HPC 顶会论文写作 Skill

- `systems-paper-writing`：面向 OSDI、SOSP、EuroSys、ATC、NSDI 等系统顶会，覆盖论文结构、写作、修改和投稿前审计；强制检查“问题 → 机制 → 证据”的论证链。
- `hpc-paper-writing`：面向 SC、PPoPP、ICS、HPDC 等 HPC 顶会，覆盖论文结构、写作、修改和投稿前审计；强制检查“profiling → 优化 → 硬件极限证据”的性能论证链。

两个 skill 都内置用户提供的完整写作指南作为本地 reference，离线也可查阅细节与投稿前 checklist。

## 三、论文工作流 Skill

仓库中原有的论文工作流 skill 仍然保留：

- `weekly-paper-radar`
- `topic-paper-finder`
- `vault-note-finder`
- `reading-note-builder`
- `review-note-builder`
- `reference-validation-report`

其中 `topic-paper-finder` 有三种检索模式：`study` 保留近三年与固定 taxonomy；`problem-boundary` 和 `mechanism-inspiration` 默认不受年份、venue 或 taxonomy 限制，并支持多个 `--query` 组成证据组合。它只产生学术候选池，关键判断仍需检查原文；代码仓库、官方文档、issue、benchmark、工程文章和博客由方法设计流程使用相应工具另行检索。

它们服务于这条链路：

1. 搜索论文
2. 下载 PDF 到本地论文目录
3. 在 PaperQuay 阅读、标注、写原始笔记
4. 基于 PaperQuay 笔记和 MinerU 缓存生成正式 Obsidian 阅读/审稿笔记
5. 核验 LaTeX 参考文献，并生成中文参考文献验证报告 PDF

### `reference-validation-report`

- 基于 DOI/Crossref、arXiv 及官方出版或会议页面核验参考文献
- 生成带证据的中文 PDF 报告；未解决条目不会被标记为已确认
- 支持标准 `.bib + .bbl + .tex`、Elsevier 风格 `.bbl` 和内联 `thebibliography`

## 验证

这次新增的 expert skill 验证记录见：

- [shared/tests/expert_skill_validation.md](./shared/tests/expert_skill_validation.md)

静态协议与回归用例验证：

```powershell
python shared\tests\validate_expert_skills.py
python shared\tests\validate_explicit_skill_policy.py
```

将四个 expert skill、证据检索后端及其共享依赖闭包同步到本机两套 Codex skill 根目录、全局 Claude Code 和 Obsidian Claudian 的两套镜像：

```powershell
.\shared\scripts\sync_expert_skills.ps1
.\shared\scripts\sync_explicit_skill_policy.ps1
```

Codex 对所有受保护任务 skill 设置 `allow_implicit_invocation: false`；Codex 与 Claude 同步使用“仅显式要求 skill 才允许”的描述和窄别名路由。若客户端或会话在部署前已经加载 skill 目录，请重启客户端或新建会话使目录重新发现。

如需命令示例和工作流说明，统一以 [README.md](./README.md) 和 [QUICKSTART.md](./QUICKSTART.md) 为准。
