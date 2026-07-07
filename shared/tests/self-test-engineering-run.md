# 自测：Engineering Task Decomposition

## 任务

模拟需求：

“给评测系统加一个导出报告功能。”

## 第 1 步：最小输入

```md
- 我理解这个需求是：给评测系统增加报告导出功能
- 可能影响的系统部分是：API、报告 UI、报告数据拼装流程
- 我现在不知道的是：报告数据在哪里生成、是否已有导出接口、导出格式要求是什么
```

## 第 2 步：按流程扩展

### `system-snapshot.md`

```md
# System Snapshot

## Requirement as currently understood
给评测系统增加导出报告功能，至少涉及一个用户触发入口和一个可下载产物。

## Suspected subsystem boundary
- 报告展示前端
- 报告生成或聚合后端
- 文件导出接口或任务逻辑

## Current workflow or runtime path
目前未知，需要先定位报告页面入口、后端报告 API、数据聚合路径。

## Known constraints
- 需求还未说明导出格式
- 需求还未说明同步下载还是异步任务

## Unknowns
- 报告数据在哪里组装
- 是否已经有导出逻辑
- 导出格式是 PDF、CSV 还是 Markdown

## Evidence inspected
- observed: 当前样例未绑定真实仓库证据
- inferred: 导出功能通常跨 UI 与后端边界
- unknown: 真实代码入口和数据路径

## Immediate risks
- 在没有证据前就假设系统边界
- 把“导出”误当成单纯前端按钮问题

## Next verification action
先查报告页面入口文件、报告 API、以及仓库中是否已有 export/download 相关实现。
```

### `unknowns-checklist.md`

```md
# Unknowns Checklist

1. 报告页面入口文件在哪里
2. 报告数据由哪个服务或接口组装
3. 是否已有 export/download 相关路由
4. 导出格式和交付方式是什么
5. 是否需要权限控制或异步任务
```

### `solution-options.md`

```md
# Solution Options

## Option A: 前端触发 + 后端现有数据接口直接导出
- 前提：已有可复用数据接口
- 优点：实现最快
- 风险：接口并不适合导出格式

## Option B: 增加独立导出 API
- 前提：后端能稳定聚合导出数据
- 优点：职责清晰
- 风险：实现成本更高

## Option C: 异步导出任务
- 前提：数据量大或生成慢
- 优点：适合重型报告
- 风险：过早复杂化
```

### `decision-record-engineering-path.md`

```md
# Decision Record

## Decision
先验证 Option A 是否可行，再决定是否升级到 Option B。

## Context
当前没有真实仓库证据，不适合直接选高复杂路径。

## Alternatives considered
Option A / Option B / Option C

## Why chosen
Option A 对证据依赖最小，能最快验证真实系统边界。

## Why others were rejected
- B：当前缺少足够证据支撑新增独立 API
- C：在未确认导出是否重型之前复杂度过高

## Consequences
第一步必须先做证据搜集，而不是直接实现。

## Reversal triggers
如果发现现有接口无法稳定提供导出所需数据，则切换到 Option B。
```

### `execution-slice-plan.md`

```md
# Execution Slice Plan

## First slice
定位报告页入口、报告 API、导出相关现有实现。

## Validation target
确认：
- 报告数据在哪里组装
- 是否存在可复用接口
- 导出是否只是表现层问题

## Exit condition
拿到至少 3 个证据锚点后，再做最终路径选择。
```

## 第 3 步：按 rubric 自评

### 结果

- Entry friction: 2
- Role discipline: 2
- Artifact completeness: 2
- Evidence grounding: 1
- Decision ownership: 2
- Transfer: 2

### 总分

11/12

## 发现的问题

这个样例最大的不足是：

- 虽然流程对了，但它还没有绑定真实仓库证据

这说明：

- skill 结构已经可执行
- 但真实工程任务里必须真的去读代码、接口、日志，不能只在文档里模拟

## 改进结论

在实际运行 `engineering-task-decomposition` 时，应额外强制：

- `system-snapshot.md` 的 `Evidence inspected` 至少包含 3 个真实锚点后，才允许写最终 option comparison
