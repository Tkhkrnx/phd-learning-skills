# Shared Artifact Schemas

Default language rule:

- adapt headings and body language to the user's working language
- in Chinese-first use, write headings and analysis in Chinese by default
- retain original English for paper names, system names, APIs, and other proper identifiers when helpful
- do not copy the English sample headings below verbatim when the user is working in Chinese; translate the artifact title and section headers into natural Chinese

## `problem-card.md`

```md
# 问题卡片

## 当前问题陈述
## 目标场景
## 为什么重要
## 已有证据
## 失败假设
## 当前未确定点
## 下一步要补的证据
## 当前用户决策
```

## `design-card.md`

```md
# 设计卡片

## 目标
## 约束
## 候选机制
## 各机制的关键假设
## 失败模式
## 验证计划
## 选定机制
## 淘汰理由
```

## `system-snapshot.md`

```md
# 系统快照

## 当前对需求的理解
## 推测的系统边界
## 当前工作流或运行路径
## 已知约束
## 未知项
## 已检查证据
## 当前风险
## 下一步验证动作
```

## `decision-record.md`

```md
# 决策记录

## 决策
## 背景
## 考虑过的备选项
## 为什么选它
## 为什么不选其他项
## 后果
## 触发反转的条件
```

## `knowledge-closure-note.md`

```md
# 知识补全笔记

## 我当前的理解模型
## 错误或缺失之处
## 纠正后的模型
## 在当前任务里的含义
## 近迁移案例
## 远迁移案例
## 独立复述
```
