# PhD Learning Skills

这个仓库现在包含三类 skill：

1. 面向博士研究/工程/学习协作的 expert skill
2. 面向论文发现、笔记增强与参考文献核验的论文工作流 skill
3. 面向系统与高性能计算顶会写作的论文写作 skill

## 一、Expert Skill

这四个 skill 是按“不同任务对应不同专家角色”的原则设计的，不再是统一模板：

- `research-problem-formulation`
  - 扮演大模型推理系统领域专家
  - 最终必须逼近三件事：
    - 问题定义是什么
    - 为什么重要
    - 现有工作为什么还失败
- `research-method-design`
  - 扮演系统方法设计与实验设计专家
  - 重点收敛到：
    - 机制
    - 替代方案
    - trade-off
    - kill criterion
- `engineering-task-decomposition`
  - 扮演资深工程师 / 架构师
  - 重点收敛到：
    - 真正理解相关代码和系统边界
    - 当前最优实现路径
    - 第一执行切片
- `targeted-knowledge-closure`
  - 扮演懂内容也懂教学法的导师
  - 重点收敛到：
    - 真正掌握一个知识点
    - 独立复述
    - 小迁移

这套 expert skill 的总蓝图见：

- [AGENT_COLLABORATION_SKILL_BLUEPRINT.md](./AGENT_COLLABORATION_SKILL_BLUEPRINT.md)

研究问题和方法设计会用到的大模型推理系统三层框架见：

- [shared/expert-skill-references/llm_inference_three_layer_framework.md](./shared/expert-skill-references/llm_inference_three_layer_framework.md)

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

如需命令示例和工作流说明，统一以 [README.md](./README.md) 和 [QUICKSTART.md](./QUICKSTART.md) 为准。
