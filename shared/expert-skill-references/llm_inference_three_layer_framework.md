# LLM Inference Three-Layer Framework

This note supports `research-problem-formulation` and `research-method-design`.

The user's working model is:

1. `请求组织与调度`
2. `状态管理与复用`
3. `执行路径优化与验证`

These are best treated as a top-down optimization stack for LLM inference systems rather than three isolated buckets.

## Layer 1: 请求组织与调度

Core concern:

- how requests, subtasks, workflows, or agent programs are organized, prioritized, scheduled, paused, resumed, and resource-governed

Typical objects:

- request
- dependency graph
- workflow or program
- priority
- quota
- admission control

Typical questions:

- which unit should be scheduled
- what can run in parallel
- what should be parked
- how should latency and fairness be balanced

## Layer 2: 状态管理与复用

Core concern:

- which state objects should be preserved, where they should live, how they are updated, and when they are worth reusing

Typical objects:

- KV cache
- prefix cache
- RAG embeddings and retrieval state
- session context
- intermediate results
- agent memory or tool execution context

Typical questions:

- what counts as system state
- how should states be layered across storage and devices
- how is semantic consistency maintained
- when is reuse beneficial enough to justify management cost

## Layer 3: 执行路径优化与验证

Core concern:

- how the engine, runtime, kernels, memory movement, and device mapping actually execute the work efficiently and how the gain is validated

Typical objects:

- runtime scheduler internals
- kernel path
- operator path
- memory path
- communication path
- benchmark and validation harness

Typical questions:

- where is the actual bottleneck
- what path optimization changes latency, throughput, TTFT, or tail risk
- how do we validate that the optimization matters under realistic workloads

## Important boundary note

Layers 2 and 3 often overlap.

State reuse decisions are often constrained by:

- memory hierarchy
- communication path
- runtime execution cost

Therefore a research problem may be:

- primarily in layer 2 with layer-3 consequences
- primarily in layer 3 but justified by state-reuse behavior

Do not force a false separation when the mechanism is cross-layer.

## How to use this framework in problem formulation

When a new research intuition appears, first ask:

1. which layer is the primary layer
2. which layer is the secondary layer
3. what is the actual system object
4. what adjacent papers already cover that object

The goal is to avoid:

- treating a layer-1 symptom as a layer-3 problem
- treating a layer-2 state problem as a vague “new runtime” claim
- treating industry/product signals as direct system evidence
