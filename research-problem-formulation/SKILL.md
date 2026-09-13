---
name: research-problem-formulation
description: Formulate and pressure-test a systems research problem when the user explicitly invokes this Skill.
---

# Research Problem Formulation

Turn a phenomenon or research idea into a defensible declarative problem, or conclude that the proposed problem is not established.

## Core workflow

1. Separate the observed condition from the objective, proposed solution, and causal hypotheses.
2. Identify the affected system object, operating condition, consequence, and evidence boundary.
3. Build a targeted query portfolio and inspect decisive primary sources before judging reality, importance, prior resolution, non-triviality, or researchability.
4. State the problem without a how-to question or preferred mechanism, then pressure-test the strongest collapse condition.
5. Preserve provisional status whenever decisive evidence or user-owned scope is unresolved.

## Collaboration contract

Lead with evidence, an expert candidate formulation, and the strongest counterexample rather than a questionnaire. When a user-owned boundary or interpretation can change the problem, ask one focused question that elicits their reasoning, correction, or evidence; yes/no approval alone is not convergence. Do not finish a consequential formulation as an agent-only monologue, but do not manufacture an extra turn when the user's supplied reasoning already resolves the boundary.

## Load on demand

- Read [deep formulation workflow](references/deep-workflow.md) for a broad new problem, a contested prior-work boundary, or revision of a frozen problem/RQ package.
- Read `../shared/expert-skill-references/research_evidence_acquisition.md` for every new-problem judgment and before revising any claim about importance, novelty, or unresolved status; use its problem-boundary route only.
- Read `../shared/expert-skill-references/llm_inference_three_layer_framework.md` only when an LLM inference/serving problem spans model, workload, and runtime layers.
- Use `topic-paper-finder` only as a bounded academic-discovery backend when the current evidence search needs it.

## Boundaries

- A problem remains meaningful after removing the proposed solution. “How to optimize X”, “build X”, and “we lack our X” are objectives or solution requests, not problem statements.
- Do not invent a failure, cause, metric, or literature gap to make a candidate look academic.
- Keep problem, challenge, mechanism, and experimental RQ distinct.
- Treat snippets and broad literature volume as discovery signals, not proof.
- Preserve confirmed wording and evidence roles during revision unless the user reopens them.

## Completion

Finish only when the user can defend an abstract-level, paper-ready account of: **what the problem is**, **why it matters**, and **why existing work still fails**. The problem itself must be a declarative condition or limitation, not a how-to question or solution objective. Include the evidence boundary and a condition that would narrow or invalidate the framing. If the user asks to move into method design, writing, experiments, or implementation, hand off the confirmed state and continue as normal execution or another explicitly requested Skill.
