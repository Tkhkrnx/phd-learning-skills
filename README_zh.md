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
    - 根源挑战和适用边界
    - 因果机制及可落地的系统载体
    - 相关工作或跨领域启发中的可迁移原理
    - 替代方案、trade-off、假设和系统成本
    - kill criterion
    - 第一个判别性实验
- `engineering-task-decomposition`
  - 扮演资深工程师 / 架构师
  - 重点收敛到：
    - 真实需求、非目标和验收证据
    - 真正理解代码、运行路径和系统边界
    - 当前最优实现路径及被拒绝的替代方案
    - 第一可逆执行切片
    - 验证、可观测性和回滚边界
- `targeted-knowledge-closure`
  - 扮演懂内容也懂教学法的导师
  - 重点收敛到：
    - 准确心智模型和前置知识修复
    - 用自己的话独立重构
    - 与近似概念或常见误解进行辨析
    - 迁移到当前任务中的小案例
    - 在下一次相似问题中减少脚手架依赖

这四个 skill 是用户可见的协作协议，不是模型自己的任务拆解或执行清单。触发条件是用户明确表达了与某个 skill 对应的协作意图，但不要求念出 skill 名称：“分析/澄清需求”“判断一个研究想法是否构成学术问题”“为已明确的问题共同设计方法”“弄懂并应用一个具体概念”都属于明确意图。仅仅因为任务涉及研究、工程、论文、代码或解释，不能触发。

每个实质轮次只能推进一个内部阶段：AI 先提供最小专家脚手架，再提出一个能暴露用户推理过程的开放式问题，并在此停止等待。阶段名、状态和生命周期标记只在内部维护，正常对话不得显示机器协议行。是/否、批准或裸选项不算协作证据。直接写作、审阅、同步、编码、调试、跑实验或执行已冻结方案必须走普通执行流程。若用户从协作切换到直接执行，skill 只保留已确认结论并静默退出。

典型边界：

| 用户意图 | 应有行为 |
|---|---|
| “帮我分析一下这个需求，先别写代码” | 调用 `engineering-task-decomposition` |
| “我有一个研究想法，帮我判断它是否构成学术问题” | 调用 `research-problem-formulation` |
| “这个问题已经明确了，带我一起找一个可辩护的解决方法” | 调用 `research-method-design` |
| “这个概率是什么意思？带我真正弄懂” | 调用 `targeted-knowledge-closure` |
| “说明一下 PR9 做了什么，我先了解后再审阅” | 不调用教学 skill，直接解释具体工作产物 |
| “按已经确认的方案同步实验计划、论文和代码” | 不调用这四个 skill，直接执行 |

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

静态协议与回归用例验证：

```powershell
python shared\tests\validate_expert_skills.py
```

将四个 skill 及其共享依赖闭包同步到全局 Codex、全局 Claude Code 和 Obsidian Claudian 的两套镜像：

```powershell
.\shared\scripts\sync_expert_skills.ps1
```

Codex 与 Claude 使用同一组窄触发描述。保留自然语言意图发现能力，同时用成对的“应触发 / 必须绕过”用例约束普通执行任务。若客户端或会话在部署前已经加载 skill 目录，请重启客户端或新建会话使目录重新发现。

如需命令示例和工作流说明，统一以 [README.md](./README.md) 和 [QUICKSTART.md](./QUICKSTART.md) 为准。
