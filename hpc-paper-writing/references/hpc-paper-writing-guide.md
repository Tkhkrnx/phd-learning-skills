<div style="max-width: 780px; margin: 0 auto; padding: 20px 16px;">

<div style="text-align: center; margin-bottom: 40px; padding: 32px 20px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-lg);">
<h1 style="font-size: clamp(1.5rem, 4vw, 2rem); margin: 0 0 8px 0; color: var(--text-primary);">高性能计算领域顶会论文写作指南</h1>
<p style="color: var(--text-secondary); margin: 0; font-size: 0.95rem;">SC / PPoPP / ICS / HPDC</p>
<p style="color: var(--text-muted); margin: 8px 0 0 0; font-size: 0.85rem;">清华大学学生超算团队 金煜阳</p>
</div>

## 目录

- [HPC 论文 vs. 系统论文的区别](#hpc-论文-vs-系统论文的区别)
- [审稿人评判标准](#审稿人评判标准)
- [论文整体结构](#论文整体结构)
- [Introduction 写法](#introduction-写法)
- [Background Section](#background-section)
- [Performance Analysis / Motivation](#performance-analysis--motivation)
- [Design / Optimization Section](#design--optimization-section)
- [Evaluation Section](#evaluation-section)
- [画图指南](#画图指南)
- [Abstract 写法](#abstract-写法)
- [写作风格与关键术语](#写作风格与关键术语)
- [投稿前 Checklist](#投稿前-checklist)

---

## HPC 论文 vs. 系统论文的区别

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

HPC 论文的核心叙事围绕**「性能」**展开——不是构建新系统，而是让计算**尽可能接近硬件极限**。

| 维度 | OSDI/SOSP 系统论文 | SC/PPoPP/ICS HPC 论文 |
|------|-------------------|----------------------|
| 核心关注 | 新抽象/新机制/新架构 | 性能——接近硬件极限 |
| 创新来源 | 新的 system design idea | 新的优化技术/算法/并行策略 |
| 评判标准 | 设计是否 elegant、通用 | 性能提升是否显著、是否接近 peak |
| Evaluation 重心 | End-to-end + ablation | Scaling + roofline + breakdown |
| 硬件依赖 | 通常抽象掉硬件 | 深度绑定具体硬件特性 |

</div>

---

## 审稿人评判标准

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 8px;">

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">1. 性能提升显著性</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">Speedup 是否足够大？在有意义的规模上测试？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">2. 性能理解深度</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">分析了为什么快/慢？瓶颈在哪？离 peak 多远？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">3. Scalability</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">Strong/weak scaling 表现？Parallel efficiency？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">4. 方法通用性</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">优化技术可迁移？还是只对一个 kernel 有效？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">5. 实验严谨性</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">控制变量？报告 variance？多平台验证？</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-page); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">6. Reproducibility</strong><br/>
<span style="color: var(--text-secondary); font-size: 0.9rem;">代码开源？Artifact evaluation 通过？</span>
</div>

</div>
</div>

### 常见致命问题

- 性能提升来自不公平的 baseline 比较（不同硬件/编译选项/精度）
- 没有性能分析——只说 "fast" 但不解释为什么
- 只在单节点/单 GPU 测试，没有 scaling 实验
- 优化 trick 过于 case-specific，缺乏通用性
- 没有和 vendor-tuned library 比较（cuBLAS, FFTW, oneMKL）
- 实验不可复现

---

## 论文整体结构

SC/PPoPP 论文典型分配（10-12 页）：

| Section | 页数 | 核心任务 |
|---------|------|----------|
| Abstract | ~0.3 | 问题 + 方法 + speedup 数字 |
| Introduction | 1.5-2 | 领域重要性 + 性能瓶颈 + 方法 + 结果 |
| Background | 1-1.5 | 算法背景 + 硬件架构特性 + 性能模型 |
| Performance Analysis | 1-1.5 | Profiling + 瓶颈定位 + 优化空间量化 |
| Optimization Design | 2.5-3.5 | 核心优化技术（3-5 个优化点） |
| Implementation | 0.5-1 | 编程模型、编译器、代码细节 |
| Evaluation | 2.5-3.5 | Scaling + comparison + breakdown + roofline |
| Related Work | 0.5-1 | 同类优化工作对比 |
| Conclusion | ~0.3 | 总 speedup + future directions |

---

## Introduction 写法

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶1</span>
<strong>应用/问题的重要性 + 计算挑战</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">科学/工程重要性 + 计算量级。<br/><code>X is critical for… / requires Y PFLOPS / takes Z hours on W nodes</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶2</span>
<strong>现有实现的性能瓶颈</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">当前实现为什么慢：数据依赖、内存瓶颈、通信开销、负载不均。与硬件 peak 的差距。<br/><code>Current implementations achieve only N% of peak performance…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light); background: var(--accent-light); margin-left: -20px; margin-right: -20px; padding: 16px 20px;">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶3</span>
<strong>为什么现有优化方法不够 ⭐</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">已有优化工作的局限性。为什么不能简单套用——不同 access pattern / 算法特性 / 硬件特性。<br/><code>However, existing approaches fail to exploit… / are limited to…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶4</span>
<strong>Key Insight + 方法概要</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">来源于性能模型或硬件特性的深刻理解。列出 3-5 个核心优化点。<br/><code>We observe/exploit that… Our approach combines: (1)…, (2)…, (3)…</code></p>
</div>

<div style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border-light);">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶5</span>
<strong>结果预览（HPC 论文必须详细）</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">必须包含：Speedup 数字 + 绝对性能（FLOPS）+ 规模 + 峰值效率。<br/><code>X achieves Y PFLOPS on Z GPUs (W% of peak), a Nx speedup over SOTA</code></p>
</div>

<div style="margin-bottom: 0;">
<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">
<span style="background: var(--accent-primary); color: var(--text-inverse); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">¶6</span>
<strong>Contribution List</strong>
</div>
<p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">性能分析/瓶颈识别 + 核心优化技术 + 大规模实现验证 + 性能模型 + 开源代码</p>
</div>

</div>

---

## Background Section

HPC 论文的 Background 需覆盖两个方面：

### 算法/应用背景
- 目标问题的数学表述或算法伪代码
- 核心计算 kernel 的特征（compute/memory bound、数据依赖）
- 问题规模的参数空间

### 硬件架构特性
- 目标硬件关键参数（compute throughput, memory BW, interconnect BW）
- 内存层级（L1/L2/HBM/NVLink/network）
- 对优化有影响的微架构特性
- 性能模型基础（Roofline、Arithmetic Intensity）

---

## Performance Analysis / Motivation

<div style="background: var(--accent-light); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

**这是 HPC 论文区别于系统论文最关键的一节。**

任务：用 profiling 数据精确定位性能瓶颈，量化优化空间。

</div>

### 必做的分析

| 分析类型 | 回答什么问题 | 工具 |
|----------|-------------|------|
| Profiling breakdown | 时间花在哪些 kernel | Nsight, VTune, perf |
| 瓶颈归因 | Compute-bound vs. memory-bound? 哪层 memory? | Roofline, Nsight Compute |
| Peak efficiency gap | 达到 theoretical peak 多少？差距原因？ | LIKWID, manual analysis |
| Scaling bottleneck | 多节点时什么成为新瓶颈？ | Score-P, MPIP |

这一节的产出是 1-3 张 profiling/breakdown 图，为 Design section 的每个优化提供动机。

---

## Design / Optimization Section

### 结构：优化点逐一展开

```
3.1 Optimization 1: Memory access pattern optimization
3.2 Optimization 2: Communication-computation overlap
3.3 Optimization 3: Load balancing strategy
3.4 Optimization 4: Vectorization and kernel fusion
3.5 Putting it all together
```

### 每个优化点的写作结构

1. **问题**：对应 Motivation 中的哪个瓶颈
2. **Insight**：利用了什么硬件/算法性质
3. **方法**：具体怎么做（伪代码/示意图）
4. **分析**：为什么能减少多少开销（最好有量化公式）

### 常见优化类型

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin: 16px 0;">

<div style="padding: 12px 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">内存优化</strong><br/>
<span style="font-size: 0.85rem; color: var(--text-secondary);">数据布局变换 (AoS→SoA)<br/>Tiling / Blocking<br/>Kernel fusion 减少数据移动<br/>Register blocking<br/>Shared memory 利用</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">计算优化</strong><br/>
<span style="font-size: 0.85rem; color: var(--text-secondary);">SIMD/SIMT 向量化<br/>Operator fusion<br/>Mixed precision<br/>算法重构减少 FLOP<br/>Instruction-level parallelism</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">通信优化</strong><br/>
<span style="font-size: 0.85rem; color: var(--text-secondary);">通信-计算重叠<br/>通信量减少<br/>拓扑感知调度<br/>集合通信优化<br/>Async data transfer</span>
</div>

<div style="padding: 12px 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">并行策略</strong><br/>
<span style="font-size: 0.85rem; color: var(--text-secondary);">分区策略设计<br/>负载均衡<br/>任务调度<br/>Pipeline parallelism<br/>Hybrid parallelism</span>
</div>

</div>

---

## Evaluation Section

### HPC 论文 Evaluation 的六大必做维度

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

**1. Strong Scaling**
- 固定问题规模，增加资源
- 报告 parallel efficiency = actual speedup / ideal speedup
- 必须画 ideal linear scaling 虚线

**2. Weak Scaling**
- 问题规模随资源等比增加
- 理想应为常数 time / 100% efficiency
- 展示大规模下的可持续性

**3. 绝对性能（Peak Fraction）**
- 报告 FLOP/s 或 achieved bandwidth
- 与 theoretical peak 比较
- Roofline 可视化

**4. Performance Breakdown**
- Baseline → +Opt1 → +Opt2 → +Opt3 → Full
- 每步 incremental improvement
- 展示每个优化的独立贡献

**5. vs. State-of-the-art**
- 和最新 vendor library / 已发表工作比较
- 同硬件、同精度、同编译选项
- 区分 kernel-level 和 end-to-end

**6. 性能模型验证（如有）**
- 模型预测 vs. 实际测量
- 不同参数下的准确度

</div>

### 实验设置描述要求

HPC 论文的实验配置必须**极其精确**：

- **硬件**：具体型号（"A100 80GB SXM4"，不是 "NVIDIA GPU"）、节点数、互联拓扑
- **软件**：编译器版本、CUDA/ROCm 版本、MPI 实现、编译 flags
- **配置**：线程数、进程分布、affinity 设置
- **问题规模**：精确参数
- **统计**：运行次数、warmup 轮次、报告 median 还是 mean、误差条含义

---

## 画图指南

### HPC 论文特有的图类型

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0;">

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">1. Roofline Plot ⭐</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>坐标</strong>：X = Arithmetic Intensity (FLOP/Byte, log)；Y = Performance (GFLOP/s, log)<br/>
<strong>内容</strong>：Memory BW ceiling + Compute ceiling 两条线；kernel 位置标注<br/>
<strong>用途</strong>：展示 kernel 的瓶颈类型 + 优化使 kernel 向 roof 移动<br/>
<strong>要点</strong>：标注硬件峰值数字；用箭头标注优化方向；不同 kernel 不同 marker
</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">2. Scaling Plot（最核心）</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>Strong scaling</strong>：X = #GPUs (log)；Y = Speedup (log)；画 ideal linear 虚线<br/>
<strong>Weak scaling</strong>：X = #GPUs；Y = Efficiency (%)；理想是水平 100% 线<br/>
<strong>要点</strong>：双 log 坐标最清晰；ideal line 用灰色虚线；标注 efficiency 数字；大规模（>100 nodes）数据点最重要
</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">3. Performance Breakdown / Optimization Stack</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>形式</strong>：Stacked bar（时间分解）/ Waterfall（逐步优化）/ Grouped bar<br/>
<strong>内容</strong>：Baseline → 逐步应用优化 → Full<br/>
<strong>要点</strong>：用颜色区分 compute/memory/communication；标注绝对数字和百分比
</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">4. Communication vs. Computation 分解</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>形式</strong>：Stacked area chart，随节点数变化的各部分比例<br/>
<strong>用途</strong>：揭示大规模下通信成为瓶颈的拐点
</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">5. 硬件利用率时间线</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>形式</strong>：GPU kernel timeline（展示 overlap 前后）<br/>
<strong>用途</strong>：可视化 computation-communication overlap 的效果
</p>
</div>

<div style="margin-bottom: 24px;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">6. Parameter Heatmap</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>形式</strong>：X/Y = 参数（tile size, block size），颜色 = 性能<br/>
<strong>用途</strong>：参数空间探索和 sensitivity 分析
</p>
</div>

<div style="margin-bottom: 0;">
<h4 style="margin: 0 0 8px 0; color: var(--accent-primary);">7. 比较 Bar Chart</h4>
<p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
<strong>形式</strong>：和 baseline/SOTA 在不同 problem size 下的对比<br/>
<strong>要点</strong>：同硬件/精度/编译选项；标注 speedup 数字在 bar 上方
</p>
</div>

</div>

### HPC 画图通用原则

| 原则 | 要求 |
|------|------|
| Log-log scale 是默认 | Scaling 图、Roofline 图必须用 log scale |
| 标注绝对数字 | 不只有 speedup，还要有 FLOPS 或秒数 |
| 画 theoretical peak / ideal 参考线 | 让 reader 知道距离极限多远 |
| 多种 problem size | 证明方法的通用性 |
| Error bar 必须有 | 多次运行的 std/min/max |
| 图中标注硬件信息 | "4× A100 80GB, NVLink 600GB/s" |

---

## Abstract 写法

HPC 论文 abstract 的固定模式（150-250 词）：

1. 应用/问题重要性
2. 性能挑战（`achieve only N% of peak / take X hours`）
3. 核心方法概述（`We present optimized X that exploits Y and Z`）
4. 关键技术列表（`(1)…, (2)…, (3)…`）
5. **结果数字**（`achieve X PFLOPS on Y GPUs, Nx speedup, Z% of peak`）
6. 规模/Impact（`enables simulation of… in real-time`）

---

## 写作风格与关键术语

### HPC 社区文风

- **极度精确的数字**：不说 "significantly faster"，说 "3.7× speedup on 128 A100 GPUs"
- **硬件 aware 的语言**：cache line, warp divergence, memory coalescing
- **性能模型思维**：解释为什么能/不能更快
- **Reproducibility 意识**：写清每个实验细节

### 关键术语表

| 术语 | 含义 | 使用场景 |
|------|------|----------|
| Arithmetic Intensity | FLOP/Byte | 判断 compute/memory bound |
| Parallel Efficiency | actual_speedup / ideal_speedup | Scaling 评价 |
| Strong Scaling | 固定问题规模的并行扩展性 | 必做实验 |
| Weak Scaling | 增长问题规模的并行扩展性 | 必做实验 |
| Roofline | 性能上界可视化模型 | 性能分析 |
| Time-to-solution | 端到端执行时间 | 最终评价指标 |
| Fraction of peak | 达到理论峰值的百分比 | 性能评价 |
| Bandwidth utilization | 内存/网络带宽利用率 | 瓶颈分析 |
| Kernel fusion | 合并多个计算 kernel | 优化技术 |
| Comm-comp overlap | 通信计算重叠 | 多节点优化 |

### 避免的表述

- ❌ "Our implementation is efficient" → ✅ "achieves 72% of peak memory BW"
- ❌ "We parallelize X" → ✅ "We achieve 89% parallel efficiency on 256 GPUs"
- ❌ "Near-linear scaling" → ✅ "93% efficiency at 128 nodes, 78% at 512 nodes"
- ❌ "Significant speedup" → ✅ "4.2× over cuBLAS on A100"

---

## 投稿前 Checklist

<div style="background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 20px; margin: 16px 0; font-size: 0.9rem;">

- ☐ 性能对比基于公平 baseline（同硬件、同精度、同编译选项）？
- ☐ 有 strong scaling 和/或 weak scaling 实验？
- ☐ 有绝对性能数字（FLOPS / bandwidth / time）？
- ☐ 有 fraction of peak 或 roofline 分析？
- ☐ 有 performance breakdown 展示每个优化的贡献？
- ☐ 有与最新 vendor library / SOTA 的比较？
- ☐ 实验在大规模上验证（不只单节点）？
- ☐ 报告了 variance / error bars？
- ☐ 实验配置描述详细到可复现？
- ☐ 优化方法的 generality 有讨论？
- ☐ 代码开源 / artifact 准备好了？
- ☐ Scaling 图有 ideal line？
- ☐ 所有图有绝对性能数字？
- ☐ SC 双盲要求已满足（去除身份信息、自引用第三人称）？

</div>

---

## HPC 论文的四种类型

不同类型写法侧重不同：

<div style="display: grid; grid-template-columns: 1fr; gap: 12px; margin: 16px 0;">

<div style="padding: 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">1. 算法优化论文（最常见）</strong><br/>
<span style="font-size: 0.9rem; color: var(--text-secondary);">针对特定算法的深度优化。重点：多层次优化组合 + 性能分析。评判：方法能否迁移？</span>
</div>

<div style="padding: 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">2. 系统/框架论文</strong><br/>
<span style="font-size: 0.9rem; color: var(--text-secondary);">编程框架/运行时/编译器。重点：多应用上的广泛适用性。评判：比手动优化有竞争力吗？</span>
</div>

<div style="padding: 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">3. 性能建模/分析论文</strong><br/>
<span style="font-size: 0.9rem; color: var(--text-secondary);">新的性能模型或分析方法论。重点：准确性和预测力。评判：是否给出新 insight？</span>
</div>

<div style="padding: 16px; background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-sm);">
<strong style="color: var(--accent-primary);">4. 大规模实验 / Gordon Bell 类型</strong><br/>
<span style="font-size: 0.9rem; color: var(--text-secondary);">超大规模应用突破。重点：scalability + time-to-solution + 科学 impact。评判：规模 unprecedented？</span>
</div>

</div>

---

<div style="text-align: center; padding: 24px 0; color: var(--text-muted); font-size: 0.85rem;">
<p>内容来源：SC/PPoPP/ICS/HPDC 近年 accepted papers 模式分析、SC 审稿标准、Gordon Bell Prize 评选准则、HPC 社区通用方法论</p>
<p>THU Student Supercomputing Team</p>
</div>

</div>
