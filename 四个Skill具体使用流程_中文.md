# 四个 Skill 具体使用流程

本文档分别说明四个 skill 在日常使用中的具体步骤。每个流程都按“输入什么、agent 做什么、你做什么、最后如何判断完成”来写。

## 1. `targeted-knowledge-closure`

### 什么时候用

- 你被一个具体知识点卡住了
- 这个知识点正在阻塞科研或工程任务推进
- 你想快速补齐，但不想只被动看解释

### 你先输入什么

最小输入：

- 我认为这个概念是：
- 它卡住我的地方是：
- 我最困惑的是：

### agent 怎么配合

第一轮只当 `corrector`：

- 只指出你哪里错了、漏了、混淆了

第二轮只当 `explainer`：

- 给直觉版解释
- 给形式化版解释
- 给任务内版解释

第三轮只当 `evaluator`：

- 给一个 near transfer
- 给一个 far transfer
- 检查你的独立复述

### 你必须做什么

- 自己先写理解，不允许先看解释
- 选定一个纠正后的说法，写明“我保留这个版本”
- 写明“我接下来会在哪个场景立刻用它”
- 独立复述一次

### 什么时候算完成

同时满足：

- 你能不用看 agent 的话复述概念
- 你能说清楚它在当前任务里为什么重要
- 你能完成一个 near transfer

## 2. `engineering-task-decomposition`

### 什么时候用

- 接到需求，但不懂系统现状
- 不知道该先看代码、接口、配置还是日志
- 不想让 agent 直接替你出方案然后你只转述

### 你先输入什么

最小输入：

- 我理解这个需求是：
- 可能影响的系统部分是：
- 我现在不知道的是：

### agent 怎么配合

第一轮只当 `clarifier`：

- 生成 unknowns checklist
- 生成验证顺序

第二轮只当 `system-mapper`：

- 帮你整理边界
- 帮你拆成系统层或生命周期阶段

第三轮只当 `design-reviewer`：

- 基于你已查到的证据比较 2 到 3 个方案
- 指出风险和验证优先级

### 你必须做什么

- 去读真实证据：代码、接口、配置、日志、运行结果
- 在 `system-snapshot.md` 里标注：
  - observed
  - inferred
  - unknown
- 自己写 decision record
- 自己决定第一步 execution slice

### 特别规则

- 写最终 option comparison 之前，至少要有 3 个真实证据锚点
- 如果连续两轮讨论没有新增证据锚点，必须停下来先补证据

### 什么时候算完成

同时满足：

- 你能自己讲清系统边界
- 你能解释为什么选这个方案
- 你知道下一步最小切片是什么

## 3. `research-problem-formulation`

### 什么时候用

- 有研究直觉，但问题还不清
- 重要性说不够硬
- 现有工作很多，但为什么不够好还没结构化

### 你先输入什么

最小输入：

- 我怀疑的问题是：
- 我觉得它重要是因为：
- 我觉得现有工作有一个关键问题是：

### agent 怎么配合

第一轮只当 `organizer`：

- 帮你把最小输入扩成 `problem-card.md`

第二轮只当 `critic`：

- 找模糊点
- 找隐含假设
- 找重要性论证的弱点

第三轮只当 `evidence-planner`：

- 给出最小证据搜集计划

### 你必须做什么

- 自己收缩问题范围
- 自己决定保留哪些 failure hypotheses
- 自己写 problem-scope decision record

### 特别规则

- 每个 related-work bucket 至少要有一个具体 paper anchor，才能算稳定
- 不允许在问题还不稳定时跳去设计方法
- 如果两轮重构后假设集合还是没收敛，必须砍范围

### 什么时候算完成

同时满足：

- 你能独立写出简洁问题定义
- 你能说出 top related-work buckets
- 你能说明为什么它们在目标场景下不够
- 你知道下一步该补什么证据

## 4. `research-method-design`

### 什么时候用

- 问题已经大体清楚
- 现在卡在怎么设计机制、怎么比较方案、怎么验证

### 你先输入什么

最小输入：

- 我要解决的问题是：
- 一个候选机制是：
- 我不放心它的原因是：

### agent 怎么配合

第一轮只当 `mechanism-challenger`：

- 拆出隐含假设
- 找失败模式

第二轮只当 `design-space-organizer`：

- 整理机制候选
- 帮你保留少量 live candidates

第三轮只当 `validation-planner`：

- 设计最小验证实验
- 指出 baseline/reference comparison

### 你必须做什么

- 自己决定保留哪个机制
- 自己写 rejection reasons
- 自己确认第一个实验到底要验证什么

### 特别规则

- critique 后最多保留 3 个 live mechanisms
- 验证计划里必须明确一个 baseline 或 reference comparison
- 如果核心假设塌了，就回到 `research-problem-formulation`

### 什么时候算完成

同时满足：

- 你能独立讲清 chosen mechanism
- 你能说清楚它为什么可能有效
- 你知道它最主要的 failure modes
- 你知道第一个最小验证实验是什么
