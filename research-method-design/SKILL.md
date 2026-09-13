---
name: research-method-design
description: Design and compare methods for an established systems research problem when the user explicitly invokes this Skill.
---

# Research Method Design

Derive a testable method from an established systems, architecture, or LLM inference/serving problem. The method may combine mechanisms, representations, measurement, analysis, models, or experiments; do not force every problem into a new-system template.

## Core workflow

1. Verify the declarative problem, relevant boundary, and nearest-method failure.
2. Derive the root challenge from that failure, not from a preferred component.
3. Compare serious candidate principles and their feasible system carriers.
4. Map assumptions, control scope, costs, and failure conditions to the target system.
5. Compare the strongest simpler alternative and define evidence that would reject the proposed method.
6. Synthesize compatible elements and choose the first discriminating experiment.

Use the chain `problem condition -> prior-method failure -> root challenge -> transferable principle -> adapted elements -> integrated method -> discriminating evidence` as a reasoning aid, not a fill-in template.

## Collaboration contract

Lead with sourced candidate principles, causal mappings, and serious alternatives. Ask the user to compare the decisive assumption, trade-off, failure case, or engineering constraint when that judgment can change the design; yes/no approval or a bare option choice is not enough. Keep rankings provisional until the relevant evidence and the user's reasoning support convergence. Do not finish a consequential method choice as an agent-only monologue, but do not impose a fixed number of challenges, candidates, or turns.

## Load on demand

- Read [deep method workflow](references/deep-workflow.md) when several mechanism families, cross-domain transfers, or system-carrier trade-offs must be compared.
- Read `../shared/expert-skill-references/research_evidence_acquisition.md` before ranking literature-backed methods; use its mechanism-inspiration route only.
- Read `../shared/expert-skill-references/llm_inference_three_layer_framework.md` only for LLM inference/serving work that crosses model, workload, and runtime layers.
- Use `topic-paper-finder` only as a bounded academic-discovery backend; inspect code, official docs, issues, benchmarks, and engineering sources separately for implementation facts.

## Boundaries

- If the problem is not stable enough to design against, identify the missing boundary instead of inventing a challenge.
- Keep desired, applied, effective, and measured behavior distinct.
- A borrowed idea is defensible only when its assumptions, carrier, cost, and analogy-break condition map to the target system.
- Do not use this Skill for executing an already chosen method, repairing replay, collecting data, writing the paper, or implementing code.

## Completion

Finish when the method addresses the evidence-derived root challenges through a causal path, feasible carrier, mapped assumptions and costs, a serious simpler alternative, a kill criterion, and a discriminating experiment—and the user can explain or challenge the decisive design logic. When execution is requested, preserve these decisions and continue under the normal implementation-and-verification loop.
