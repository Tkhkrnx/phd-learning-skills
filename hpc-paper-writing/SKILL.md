---
name: hpc-paper-writing
description: Draft, restructure, revise, or pre-submit audit a top-tier high-performance-computing paper for SC, PPoPP, ICS, HPDC, or similar venues. Use for HPC performance narratives, profiling-driven motivation, hardware-aware optimization exposition, roofline or scaling analysis, benchmark and figure planning, abstract drafting, and reviewer-facing paper checks.
---

# HPC 论文写作

将论文组织为一条可验证的性能证据链：应用或算法的重要性 → 可量化的硬件/算法瓶颈 → 由该瓶颈导出的优化 → 公平、可复现的性能证据。不要把工程实现量或单一 speedup 当作贡献。

先阅读 [参考指南](references/hpc-paper-writing-guide.md)，再处理具体稿件。保留用户已有的术语、实测数据和结论；没有实测证据时，明确标为待验证，不要补造数字或性能归因。

## 工作流

1. 明确论文对象、目标 venue、硬件/编程模型、问题规模、对比对象和当前材料（提纲、稿件、结果或 profiler trace）。根据指南的四种 HPC 论文类型确定叙事重心。
2. 建立 claim–evidence 表：每个贡献或性能结论必须对应问题证据、优化机制、测量指标和图/表。删除或降级无法由证据支撑的 claim。
3. 构建 motivation：用 profiling breakdown、瓶颈归因、peak-efficiency gap 与 scaling bottleneck 量化优化空间。让每个优化点可追溯到一个已测瓶颈。
4. 按“问题 → insight → 方法 → 开销分析”展开每个优化，并说明其利用的算法或硬件性质；给出必要的伪代码、示意图或定量模型。
5. 按 HPC 评价链组织实验：公平 baseline、绝对性能、strong/weak scaling、fraction of peak/roofline、逐步 breakdown、SOTA/vendor comparison，以及适用时的性能模型验证。区分 kernel-level 与端到端结果。
6. 审核图、abstract 与语言：报告精确数字和实验条件，画 ideal/theoretical-peak 参考线，图注自包含；abstract 必须包含问题、性能挑战、核心方法、关键技术和结果数字。

## 交付形式

根据用户请求输出其需要的一个或多个工件：

- 论文叙事或 section outline；
- 逐段重写/审阅意见，保留原稿可取之处；
- claim–evidence、优化–瓶颈或实验–问题映射；
- 图表与实验计划；
- 按来源指南执行的投稿前缺口清单。

## 强制检查

- 不把不同硬件、精度或编译选项的结果当作公平比较。
- 不用“efficient”“near-linear”“significant”等空泛表述替代绝对数字、peak fraction 或 parallel efficiency。
- 不让 Design 与 Motivation 脱节；每个优化都要回答“消除了哪个瓶颈、为何预计有效”。
- 不把单节点结果宣称为可扩展性；在论文范围允许时，报告 strong/weak scaling 与大规模行为。
- 不把未执行的实验、未验证的瓶颈归因或预期 speedup 写成事实。

## 参考资料

- [高性能计算领域顶会论文写作指南](references/hpc-paper-writing-guide.md)：完整的结构、图表、术语与投稿前 checklist。
