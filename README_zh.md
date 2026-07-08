# 博士学习 Skills

[English README](./README.md)

这是一个面向博士阶段科研、工程和学习协作的个人 Codex skill 仓库。

这个仓库不是为了做一个好看的公开模板，而是为了长期个人使用。核心目标有两个：

- 用 agent 提升任务推进速度
- 把问题定义、设计判断、独立复述和迁移能力留在自己身上

## Skill 集合

- `targeted-knowledge-closure`
  - 用“先回忆、后纠错、再迁移”的方式补齐一个正在卡住任务的知识点
- `engineering-task-decomposition`
  - 把一个不清楚的工程需求拆成有证据支撑的边界、选项、决策和第一步执行切片
- `research-problem-formulation`
  - 把一个模糊研究直觉收缩成可辩护的问题定义、相关工作桶和失败假设
- `research-method-design`
  - 把一个基本清楚的研究问题推进到机制候选、失败模式和最小验证计划

## 共享设计原则

这套 skill 统一遵守这些规则：

- 先由用户写最小初稿，再让 agent 扩展
- 每一轮 agent 只扮演一个角色
- 关键分叉处必须由用户写 decision 或 commitment
- artifact 要有固定 schema
- artifact 默认使用用户当前的工作语言，中文为主的运行默认产生中文标题、小节标题和分析文本
- 要有明确 stop rule
- 要做脱离 agent 的完成检查
- 工程判断必须绑定真实证据
- 高压场景使用 `light mode`
- 为了防止“表演式走流程”，必须保留反证、替代方案和 fresh output

完整总蓝图见：[AGENT_COLLABORATION_SKILL_BLUEPRINT.md](./AGENT_COLLABORATION_SKILL_BLUEPRINT.md)

## 整套 skill 的通用用法

每次任务都走这条总流程：

1. 先判断主 skill 是哪一个。
2. 自己先写最小输入。
3. 明确本轮 agent 角色。
4. 产出或更新本轮 artifact。
5. 分叉处由自己写 decision 或 commitment。
6. 如果被具体知识点卡住，就嵌入 `targeted-knowledge-closure`。
7. 最后做一次脱离 agent 的检查。

## 调用方式

你不需要在调用 skill 之前先记住模板。

像下面这样一句话调用就够了：

- “现在调用 `research-problem-formulation`，帮我做问题定义。”
- “现在调用 `research-method-design`，帮我做方法设计。”
- “现在调用 `engineering-task-decomposition`，帮我拆这个需求。”
- “现在调用 `targeted-knowledge-closure`，帮我补这个知识点。”

调用之后，skill 应该先反过来引导你，只问启动所需的最小 3 条输入，而不是默认你已经知道要怎么写。

## 执行模式

### `light mode`

适合：

- 时间压力大
- 需要先保住最小护栏
- 如果要求完整 artifact 会让你直接不用这套流程

即使是 `light mode`，也不能省掉：

- 用户先写初稿
- 明确的用户决策或承诺
- 一个挑战/证伪点
- 一个 agent-off 检查

你应该交付的形式：

- 一份紧凑工作笔记
- 不要求完整 artifact 集，除非你明确要长期留档

### `standard mode`

适合：

- 这个结果会被复用、实现、发表或讲给别人
- 你需要一个可复盘的长期记录，而不是临时推进

要求：

- 完整 artifact 集
- 明确证据或对照
- 完整的 finish criteria

你应该交付的形式：

- 对应 skill 的完整 artifact 集
- 完整的 decision、evidence 和 completion 记录

## 四个 skill 的具体使用流程

## 1. `targeted-knowledge-closure`

### 什么时候用

- 某个具体概念、公式、机制、系统部件卡住了当前科研或工程任务
- 你需要快速补洞，而不是看一个大教程

### 你先写什么

- 我认为这个概念是：
- 它卡住我的地方是：
- 我最困惑的是：

如果你一开始也不知道怎么写，skill 应该继续引导你：

- 每一条先随便写一句猜测也可以

`light mode` 你要交付：

- 一份紧凑笔记，里面至少有：纠正后的理解、保留的版本、立即应用场景、一个新例子

`standard mode` 你要交付：

- `knowledge-closure-note.md`
- `transfer-check.md`

如果范围太大，必须收缩到下面四类之一：

- 一个机制
- 一个公式或定理
- 一个系统组件
- 两个概念之间的对比

### agent 怎么配合

1. `corrector`
2. `explainer`
3. `evaluator`

### 你必须自己做什么

- 先从记忆里解释，不允许先看答案
- 选定一个纠正后的版本保留下来
- 指定一个马上会用到它的场景
- 自己独立复述
- 自己给出一个 agent 没给过的新例子或新应用

### 什么叫完成

同时满足：

- 你能不看 agent 复述
- 你能解释它为什么和当前任务有关
- 你能通过一个 near transfer
- 你能给出一个新的例子，而不是重复 agent 的表述

## 2. `engineering-task-decomposition`

### 什么时候用

- 接到工程需求，但系统现状不清
- 不知道该先看代码、接口、配置、日志还是运行态

### 你先写什么

- 我理解这个需求是：
- 可能影响的系统部分是：
- 我现在不知道的是：

如果你一开始也不知道怎么写，skill 应该继续引导你：

- 每一条先随便写一句粗糙判断也可以

`light mode` 你要交付：

- 一份紧凑工作笔记，里面至少有：边界猜测、unknowns、证据锚点、`null or reuse-first` 选项、第一步切片、用户路径选择

`standard mode` 你要交付：

- `system-snapshot.md`
- `unknowns-checklist.md`
- `solution-options.md`
- `execution-slice-plan.md`
- `decision-record-engineering-path.md`
- 必要时加 `evidence-acquisition-plan.md`

### agent 怎么配合

1. `clarifier`
2. `system-mapper`
3. `design-reviewer`

### 你必须自己做什么

- 去读真实证据：代码、接口、配置、日志、运行结果
- 把判断标成 `observed / inferred / unknown`
- 自己写 decision record
- 自己决定第一步 execution slice

### 特别规则

- 选项比较里必须有 `null or reuse-first`
- 没有至少 3 个真实证据锚点前，不能写最终 option comparison
- 如果暂时拿不到直接证据，必须先产出 `evidence-acquisition-plan.md`

### 什么叫完成

同时满足：

- 你能自己讲清系统边界
- 你能解释为什么选这个路径
- 你知道第一步最小执行切片是什么

## 3. `research-problem-formulation`

### 什么时候用

- 有研究直觉，但问题还不清
- 重要性说法太宽或太虚
- 现有工作很多，但“不够好”的原因还没结构化

### 你先写什么

- 我怀疑的问题是：
- 我觉得它重要是因为：
- 我觉得现有工作有一个关键问题是：

如果你一开始也不知道怎么写，skill 应该继续引导你：

- 每一条先写一个不完整判断也可以

`light mode` 你要交付：

- 一份紧凑 framing 笔记，里面至少有：问题猜测、前 1 到 3 个失败假设、每个稳定 bucket 的 paper anchor、下一步证据、以及一个 scope decision

`standard mode` 你要交付：

- `problem-card.md`
- `failure-taxonomy.md`
- `evidence-gap-list.md`
- `decision-record-problem-scope.md`
- 一条显式对照句

### agent 怎么配合

1. `organizer`
2. `critic`
3. `evidence-planner`

### 你必须自己做什么

- 自己收缩问题范围
- 自己决定哪些 failure hypotheses 继续保留
- 自己写 problem-scope decision
- 自己写一个和现有工作对照的显式反例句

### 特别规则

- 每个 related-work bucket 至少要有一个具体 paper anchor 才算稳定
- 方向不一定要硬做成题，可以是 `sharpen / park / abandon`
- 如果差异化失败主张经不起检查，就应当停下并 park 方向

### 什么叫完成

同时满足：

- 你能独立写出简洁问题定义
- 你能说出主要 related-work buckets
- 你能说明它们为什么在目标场景下不够
- 你知道下一步该补什么证据

## 4. `research-method-design`

### 什么时候用

- 研究问题已经基本清楚
- 现在卡在机制设计、方法比较和验证计划

### 你先写什么

- 我要解决的问题是：
- 一个候选机制是：
- 我不放心它的原因是：

如果你一开始也不知道怎么写，skill 应该继续引导你：

- 每一条先写一个粗糙想法也可以

`light mode` 你要交付：

- 一份紧凑 design 笔记，里面至少有：候选机制、一个更简单对照机制、baseline/reference、kill criterion、第一步实验、一个 rejection reason

`standard mode` 你要交付：

- `design-card.md`
- `mechanism-comparison.md`
- `failure-mode-table.md`
- `minimal-validation-plan.md`
- `decision-record-method-choice.md`

### agent 怎么配合

1. `mechanism-challenger`
2. `design-space-organizer`
3. `validation-planner`

### 你必须自己做什么

- 自己决定保留哪个机制
- 自己写 rejection reasons
- 自己决定第一个实验到底验证什么
- 自己写 kill criterion，也就是哪种结果一出来就说明这个机制不成立

### 特别规则

- critique 后最多保留 3 个 live mechanisms
- 必须至少保留一个更简单或更标准的 comparison mechanism
- 验证计划里必须写 baseline/reference comparison
- 验证计划里必须写 kill criterion

### 什么叫完成

同时满足：

- 你能独立讲清 chosen mechanism
- 你能说清它为什么可能有效
- 你知道主要 failure modes
- 你知道第一个最小验证实验是什么

## 验证与审计

这个仓库把 skill 质量当作工程问题处理，而不是当作文案问题。

每个 skill 都会检查：

- 入口是否够轻
- artifact 是否完整
- 证据是否真实
- 决策是否真由用户承担
- 能否迁移
- 使用成本是否可接受
- 是否容易被“表演式走流程”骗过去

测试与审计都放在 `shared/tests/` 下，包括常规自测和压力测试。

## 仓库结构

```text
phd-learning-skills/
├── AGENT_COLLABORATION_SKILL_BLUEPRINT.md
├── README.md
├── README_zh.md
├── shared/
│   ├── references/
│   ├── scripts/
│   └── tests/
├── targeted-knowledge-closure/
├── engineering-task-decomposition/
├── research-problem-formulation/
└── research-method-design/
```

## 备注

- 这个仓库默认按个人私有长期使用设计，不按公开市场化展示设计。
- 默认行为优先考虑在 Codex 里反复使用，而不是一次性演示。
- references 和 tests 写得比较显式，是为了以后能审计和回调，而不是靠记忆猜。
