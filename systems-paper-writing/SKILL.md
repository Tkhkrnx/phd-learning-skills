---
name: systems-paper-writing
description: Write or revise a systems paper for venues such as OSDI, SOSP, EuroSys, ATC, or NSDI when the user explicitly invokes this Skill.
---

# 系统顶会论文写作

将论文组织为一条可审查的论证链：重要且已量化的问题 → 不能由已有方法充分解决的原因 → 与实际贡献形态匹配的 insight、方法、机制、系统或实证发现 → 覆盖所有 claim 的证据与限制。不要预设每篇论文都必须提出新机制，也不要把实现规模、组件罗列或泛泛的“novel/efficient”当作论文贡献。

保留用户已经验证的术语、设计边界和实测结果；没有实现或实验支撑的内容必须标为设计假设或待验证项。需要完整论文结构、venue 细则或投稿前检查时，再读取 [参考指南](references/systems-paper-writing-guide.md)。

## 工作流

1. 明确系统对象、目标 venue、核心问题、最接近工作、已有实现/数据与论文 claim。先识别论文的真实贡献形态，再把 problem statement、核心贡献和预期证据各压缩成一句可检查的话。
2. 建立 claim–evidence 表：每条 contribution 映射到 motivation 数据、关键设计决策、对应的实验问题和图/表。先暴露没有证据的 claim，再决定补实验、缩小范围或改写。
3. 构造 Introduction 的叙事弧线：重要性与量化事实 → existing approaches → 缺口/失败原因 → 核心 insight 或发现 → 工作概览 → 可验证贡献 → 结果预览。避免从背景直接跳到方案。
4. 让 Motivation 用 workload characterization、profiling/breakdown 或 case study 证明问题严重；方法、设计或分析部分按证据导出的挑战展开，每个关键选择都说明取舍、替代方案和依据。
5. 用问题驱动的 Evaluation 回答端到端效果、组件贡献、敏感性、可扩展性和开销/degenerate case。优先对比最强且公平的 baseline；将 end-to-end comparison 放在前面，再补 ablation、microbenchmark 与限制。
6. 显式写出与最近相关工作的区别；检查图注、abstract 与术语是否精确，每项结果是否支撑一个引言中的 claim。

## 交付形式

根据用户请求输出其需要的一个或多个工件：

- 论文叙事、section outline 或段落重写；
- claim–evidence、challenge–design 或实验问题映射；
- reviewer-style 缺口清单与最小补证据计划；
- 图表计划、abstract 或 related-work differentiation；
- 按来源指南执行的投稿前审计。

## 强制检查

- 不把大量工程工作、已有系统的同构重实现或过小的 idea 包装为顶会创新。
- 不让 Motivation 与 Design 解决不同的问题；每个关键设计必须有明确 justification。
- 不用最弱 baseline、只给 aggregate 结果或省略 ablation 来支撑系统 claim。
- 不回避 overhead、limitation 与 degenerate case；它们是论文边界的一部分。
- 不把未运行的实验、未实现的机制或预期结果写成已经证实的事实。

## 参考资料

- [系统领域顶会论文写作指南](references/systems-paper-writing-guide.md)：完整的结构、图表、语言与投稿前 checklist。
