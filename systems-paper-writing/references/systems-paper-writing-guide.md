<div style="max-width: 780px; margin: 0 auto; padding: 20px 16px;">

<div style="text-align: center; margin-bottom: 40px; padding: 32px 20px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-lg);">
<h1 style="font-size: clamp(1.5rem, 4vw, 2rem); margin: 0 0 8px 0; color: var(--text-primary);">系统领域顶会论文写作指南</h1>
<p style="color: var(--text-secondary); margin: 0; font-size: 0.95rem;">OSDI / SOSP / EuroSys / ATC / NSDI</p>
<p style="color: var(--text-muted); margin: 8px 0 0 0; font-size: 0.85rem;">清华大学学生超算团队 金煜阳</p>
</div>

## 目录

- [审稿人评判标准](#审稿人评判标准)
- [论文整体结构](#论文整体结构)
- [Introduction 写法](#introduction-写法)
- [Background / Motivation](#background--motivation)
- [Design Section](#design-section)
- [Evaluation Section](#evaluation-section)
- [Related Work](#related-work)
- [画图指南](#画图指南)
- [Abstract 写法](#abstract-写法)
- [写作风格](#写作风格)
- [投稿前 Checklist](#投稿前-checklist)

---

## 审稿人评判标准

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

审稿人判断一篇系统论文是否值得发表，核心看五个维度（源自 Levin & Redell 1983, SOSP PC chairs）：

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 16px;">

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">1. 原创性</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">有没有新 idea？能不能一段话讲清？与已有工作的区别是否 explicit？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">2. 现实性</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">系统实现了吗？有人用了吗？纯设计论文 idea 质量够高吗？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">3. 经验教训</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">学到了什么？Lessons 的 generality 如何？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">4. 设计选择</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">关键分岔路口有哪些替代方案？为什么选了当前方案？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">5. 聚焦</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">是否聚焦在新的部分？还是已知内容也事无巨细地写了？</span>
</div>

</div>
</div>

### 常见致命问题

- 系统实现了但没有新 idea（isomorphic to existing systems）
- idea 太小撑不起一篇论文（应该写 workshop paper）
- 设计论文没有任何实现经验
- 对 related work 的区分不 explicit
- 把工程量大等同于值得发表（"我们团队做了两年"≠"有新东西"）

---

## 论文整体结构

12-14 页论文的典型分配：

| Section | 页数 | 核心任务 |
|---------|------|----------|
| Abstract | ~0.3 | 问题 → 方法 → 结果数字 |
| Introduction | 1.5-2.5 | 叙事弧线（见下节） |
| Background / Motivation | 1-2 | 量化证明问题存在且严重 |
| Design | 3-4 | 系统架构 + 关键设计决策 + 为什么 |
| Implementation | 0.5-1 | 工程细节、代码量、依赖 |
| Evaluation | 3-4 | 用实验证明 claims |
| Related Work | 1-1.5 | 与最相关工作的 explicit 对比 |
| Conclusion | ~0.3 | Lessons + future work |

---

## Introduction 写法

Introduction 是论文最重要的 2 页。审稿人在这里决定要不要认真读下去。

### 5-7 段叙事弧线

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶1</span>
<strong>领域 + 重要性</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">用 1-2 句建立领域背景 + 有冲击力的数据/趋势。<br/><code>X has emerged as… / has revolutionized… / driving over 60% of…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶2</span>
<strong>现有方法 + 合理性</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">简述 state-of-the-art 的核心机制，承认其贡献。<br/><code>Frameworks like X have significantly improved…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light); background: var(--accent-light); margin-left: -20px; margin-right: -20px; padding: 16px 20px;">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶3</span>
<strong>Problem / Gap ⭐ 最关键</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">以 <strong>However / Unfortunately / Despite</strong> 开头（铁律）。指出<strong>结构性缺陷</strong>，不是小毛病。最好有量化证据。把根因归到一个 <em>fundamental misalignment / mismatch / inherent limitation</em>。<br/>这段决定了整篇论文存在的理由。</p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶4</span>
<strong>洞察 / 观察</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">展示你独特的 insight，暗示解决方案方向。通常配 Figure 1。<br/><code>We observe that… / Our key insight is…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶5</span>
<strong>方案概述</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">正式介绍系统名 + high-level 核心机制 + 列 2-3 个设计 challenges。<br/><code>We present X, a system that… Designing such a system is challenging because…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶6</span>
<strong>结果预览</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">一句话带核心数字，对比对象明确。<br/><code>Compared with vLLM, X improves QoE by 4.7× / saves 61% GPU resources.</code></p>
</div>

<div style="margin-bottom: 0;">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶7</span>
<strong>Contribution List</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">3-5 个 bullet，每条动词开头（We identify / We design / We implement / We evaluate）。每条对应论文一个 section。</p>
</div>

</div>

### Introduction 常见错误

- 第一段太空泛，没有数据支撑
- 没有 "however" 段 — 从背景直接跳到方案
- Problem 不够 fundamental — 听起来只是工程调优
- Contribution list 每条都太 vague，不可验证

---

## Background / Motivation

任务：**用数据说服 reader 问题确实存在且严重**。

三种核心手法：

| 手法 | 做什么 | 产出 |
|------|--------|------|
| Workload characterization | 分析真实 trace/workload | CDF / histogram 展示问题分布 |
| Profiling / breakdown | 对现有系统 profiling | Breakdown chart 暴露瓶颈 |
| Case study | 一个具体 example 走完执行流程 | 时间线图/步骤图暴露低效 |

这一节通常产出 1-3 张 motivation figure，它们的任务是让 reviewer 在读 design 之前就已经被说服"确实需要新方案"。

---

## Design Section

### 结构原则

**先整体后局部**：
1. 一张 system overview 图 + 一段话给全貌
2. 逐个讲核心组件

**Challenge-driven 叙事**（推荐）：
1. 列出 2-3 个 core challenges
2. 每个 challenge 依次展示解法
3. 比按组件平铺更有说服力

**每个设计决策都要有 justification**：
- 不是"我们怎么做了"，而是"为什么这么做"
- 提到被 reject 的替代方案
- 引用 motivation section 的数据作为选择依据

### 常见错误

- 全系统从头描述而没突出新的部分 — reviewer 看不出创新
- Design 和 motivation 对不上 — motivation 说问题 A，design 解决问题 B
- 过于 implementation-heavy — design 讲 idea，implementation 讲工程

---

## Evaluation Section

### 问题驱动结构

好的 evaluation 开头明确列出要回答的问题：

> We answer the following questions:
> - Q1: Does X outperform state-of-the-art in end-to-end performance?
> - Q2: How does each component contribute? (ablation)
> - Q3: How sensitive is X to parameter Y?
> - Q4: What is the overhead?

### 实验层次（由外到内）

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 16px 20px; margin: 16px 0;">

1. **End-to-end comparison** — 和最强 baseline 在真实 workload 上整体对比（最重要，放最前）
2. **Breakdown / ablation** — 关掉各组件看各自贡献
3. **Micro-benchmark** — 针对特定机制的深度分析
4. **Sensitivity analysis** — 关键参数变化的影响
5. **Scalability** — 随规模增长的表现
6. **Overhead analysis** — 新增机制的额外开销

</div>

### Reviewer 必问的致命三问

| 问题 | 如果你没回答 |
|------|-------------|
| "为什么不和 XX 比？" | Baseline 必须包含最新最强的 |
| "性能提升来自哪个组件？" | 必须有 ablation study |
| "开销多少？有 degenerate case 吗？" | 必须展示 limitation |

### 实验设置写作要求

- Baseline 选择说明理由
- Hardware/software 配置详细到可复现
- Workload 说明来源（real trace vs. synthetic）和特征
- 每张图的 caption 必须 self-contained

---

## Related Work

- **按技术方向分组**（不按时间）
- 每组：先概述共同做法，再说你和它们的区别
- 区别要 explicit：`"Unlike X which does A, our approach does B because C"`
- 不要贬低他人：用 "address different problems" 而非 "fail to"
- 通常放在 Evaluation 之后（reader 看完你的方案和结果后，更容易理解区别）

---

## 画图指南

### 系统论文的 7 类图

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">1. Motivation Figure</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Introduction 或 Background<br/><strong>目的</strong>：让 reader 一眼看到问题存在<br/><strong>形式</strong>：时间线对比（existing vs. ours）/ profiling breakdown / workload CDF<br/><strong>关键</strong>：有 annotation 标注问题；红色=bad，蓝色=improved；简洁——一张图一个 message</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">2. System Architecture / Overview</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Design 开头<br/><strong>目的</strong>：给 reader 系统全貌的 mental model<br/><strong>形式</strong>：Block diagram — 灰色=已有组件，彩色=本文新增<br/><strong>关键</strong>：组件 5-8 个，太多需分层；数据流方向一致；虚线框标子系统边界</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">3. Mechanism 示意图</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Design 各节，每个关键机制一张<br/><strong>目的</strong>：解释核心机制怎么工作<br/><strong>形式</strong>：状态转换图 / 时序图 / 内存布局 / Before-After 对比<br/><strong>关键</strong>：数字编号标步骤；符号与正文一致；配合 example 使用</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">4. End-to-End Performance</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Evaluation（最核心的 1-2 张）<br/><strong>目的</strong>：证明整体优于 baseline<br/><strong>形式</strong>：Bar chart / Line chart / CDF（tail latency 场景）<br/><strong>关键</strong>：Baseline 用灰色，Our system 用亮色；虚线标 SLA target</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">5. Breakdown / Ablation</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Evaluation<br/><strong>目的</strong>：证明每个组件都有贡献<br/><strong>形式</strong>：Stacked bar chart / Grouped bar chart（full vs. -component A vs. -component B）</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">6. Sensitivity / Scalability</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Evaluation<br/><strong>目的</strong>：展示在不同条件下的鲁棒性<br/><strong>形式</strong>：Line chart（X=参数, Y=性能）/ Heatmap（双参数）</p>
</div>

<div style="margin-bottom: 0;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">7. Overhead / Cost</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);"><strong>位置</strong>：Evaluation<br/><strong>目的</strong>：诚实展示新机制的额外开销<br/><strong>形式</strong>：小表格 / 简单 bar chart（with/without mechanism）</p>
</div>

</div>

### 画图通用原则

| 原则 | 要求 |
|------|------|
| 一图一义 | 如果 reviewer 需要 30 秒才看懂，你失败了 |
| Figure 1 在 Introduction | 可视化 key insight 或 existing vs. ours 对比 |
| Caption self-contained | 包含结论，不是 "Figure X shows results" |
| 黑白可读 | 除颜色还用 linestyle / marker / pattern 区分 |
| 字体 ≥ 8pt | 缩到论文页面后仍可读 |
| 配色一致 | 同一个 baseline 在所有图里颜色相同 |
| Our = 亮色，Baseline = 灰色 | 视觉引导 reader 关注你的结果 |

### Figure 数量参考

12 页论文通常有 8-14 个 figure/table：
- Introduction: 1-2
- Background/Motivation: 1-3
- Design: 2-4
- Evaluation: 4-8

---

## Abstract 写法

150-250 词，固定模式：

1. 一句话问题背景
2. 一句话现有方法的不足
3. 一句话核心 idea（`We present X, which leverages Y to…`）
4. 一句话关键技术
5. **结果数字**（没有数字的 abstract 没有信息量）

不要在 abstract 中写 prose table of contents（"Section 2 describes…"）或省略数字。

---

## 写作风格

### 系统社区文风偏好

- 直接、精确、不啰嗦
- 用主动语态：`"We design X"` 而非 `"X is designed"`
- 数字说话：每个 claim 要有 evidence 支撑
- 先说结论再展开（inverted pyramid）

### 用词精确度

| 词 | 要求 |
|----|------|
| significant | 有统计学意义或量级差异，不能随便用 |
| novel | 确实 first-of-its-kind |
| efficient | 必须说清相比什么更 efficient |
| scalable | 必须定义 scale along what dimension |

### 避免的表述

- `"To the best of our knowledge, this is the first…"` — reviewer 知道反例则论文完蛋
- `"Obviously" / "Clearly"` — 如果 obvious 不用说，如果不 obvious 你在 skip 论证
- `"We leave X for future work"` — 在 evaluation 里说 = 承认论文不完整

---

## 投稿前 Checklist

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0; font-size: 0.9rem;">

- ☐ Introduction 的 problem statement 能用一句话说清吗？
- ☐ Contribution list 的每条都在论文里有对应 evidence 吗？
- ☐ Design 中的每个决策都有 justification 吗？
- ☐ Evaluation 回答了 introduction 提出的所有 claim 吗？
- ☐ 最强的 baseline 都比了吗？
- ☐ 有 ablation study 吗？
- ☐ 有 overhead / limitation 讨论吗？
- ☐ 所有 figure caption 都 self-contained 吗？
- ☐ 所有 figure 打印成黑白仍可读吗？
- ☐ Related work 中和最相关工作的区别是 explicit 的吗？
- ☐ Reference 覆盖了最新的（1-2 年内）和最经典的？
- ☐ 论文字体全篇一致、无格式错误？

</div>

---

<div style="text-align: center; padding: 24px 0; color: var(--text-muted); font-size: 0.85rem;">
<p>内容来源：Levin & Redell 1983 "How (and How Not) to Write a Good Systems Paper"、近年 OSDI/SOSP accepted papers 模式分析、系统社区通用审稿准则</p>
<p>THU Student Supercomputing Team</p>
</div>

</div>
