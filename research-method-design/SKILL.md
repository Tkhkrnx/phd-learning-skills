---
name: research-method-design
description: Design and compare methods for an established systems research problem when the user explicitly invokes this Skill.
---

# Research Method Design

Derive a testable method from an established systems, architecture, or LLM inference/serving problem. Recover what principle the user wants to borrow and which outcome comes first. Distinguish the research opportunity, the best known baseline and the project setting where the idea will be tested. The method may combine mechanisms, representations, measurement, analysis, models or experiments.

## Core workflow

1. Verify the declarative problem, relevant boundary, and nearest-method failure.
2. Derive the root challenge from that failure, not from a preferred component.
3. Compare serious candidate principles and their feasible system carriers.
4. Map assumptions, control scope, costs, and failure conditions to the target system.
5. Compare the strongest simpler alternative and define evidence that would reject the proposed method.
6. Synthesize compatible elements and choose the first discriminating experiment.

When the user asks for research options, trace the current execution or analysis on one concrete case. Show the cost it incurs, which assumption each candidate relaxes, the exact step that changes, and how that could improve the user's target. Compare with the closest work and strongest measured configuration. Credit an existing configuration as a baseline unless the investigation establishes what the proposed method adds. Rank by the user's stated outcome and flag any available measurement that is only a proxy. Invite discussion of the trade-off that could change the choice. If only one candidate survives, explain how the strongest alternative was ruled out.

For a measurement or data-analysis design, work one representative observation through the method in the first overview. Use the project's schema or sample when available. Show which records connect, the operation performed on them, and the decision the result supports. Identify any missing key or endpoint that changes the conclusion. Label illustrative inputs.

Use the chain `problem condition -> prior-method failure -> root challenge -> transferable principle -> adapted elements -> integrated method -> discriminating evidence` as a reasoning aid, not a fill-in template.

For open-ended inspiration, also work from a source-domain principle toward a natural target setting, then test whether its problem is real and survives prior work. Keep that candidate provisional; do not require a frozen problem merely to explore an idea. A transfer must change a design decision, not just rename an existing proposal with an analogy.

## Collaboration contract

Lead with sourced candidate principles, causal mappings, and serious alternatives. Ask the user to compare the decisive assumption, trade-off, failure case, or engineering constraint when that judgment can change the design; yes/no approval or a bare option choice is not enough. Keep rankings provisional until the relevant evidence and the user's reasoning support convergence. Do not finish a consequential method choice as an agent-only monologue, but do not impose a fixed number of challenges, candidates, or turns.

## Load on demand

- Read [deep method workflow](references/deep-workflow.md) when several mechanism families, cross-domain transfers, or system-carrier trade-offs must be compared.
- Read `../shared/expert-skill-references/research_evidence_acquisition.md` before ranking literature-backed methods; use its mechanism-inspiration route only.
- Read `../shared/expert-skill-references/llm_inference_three_layer_framework.md` only for LLM inference/serving work that crosses model, workload, and runtime layers.
- Use `topic-paper-finder` only as a bounded academic-discovery backend; inspect code, official docs, issues, benchmarks, and engineering sources separately for implementation facts.
- If the user explicitly appoints an expert peer, read [authorized expert-peer collaboration](../shared/expert-skill-references/expert_peer_collaboration.md). Peer agreement is neither user approval nor empirical validation.

## Boundaries

Apply a persistent goal's stage-specific assignment when the current decision belongs to that stage. After method selection, its agreed fields, baselines and checks become inputs to implementation.

- If the problem is not stable enough for a method decision, identify the missing boundary instead of inventing a challenge; authorized inspiration may continue without declaring a settled method.
- Keep desired, applied, effective, and measured behavior distinct.
- A borrowed idea is defensible only when its assumptions, carrier, cost, and analogy-break condition map to the target system.
- Do not use this Skill for executing an already chosen method, repairing replay, collecting data, writing the paper, or implementing code.

## Completion

Finish when the method addresses the evidence-derived root challenges through a causal path, feasible carrier, mapped assumptions and costs, a serious simpler alternative, a kill criterion, and a discriminating experiment—and the user can explain or challenge the decisive design logic. When execution is requested, preserve these decisions and continue under the normal implementation-and-verification loop.

For a converged project research task or an explicit file-output request, use [the seven-question output format](../shared/expert-skill-references/seven_question_research_outputs.md). Complete Questions 4–7 in the same `写作指南` that holds the confirmed problem, then finish its chapter and figure-to-conclusion guidance. Also write a separate `实验计划` that expands Question 6 into verifiable experiments and AI-executable work slices. Preserve the existing research and collaboration workflow; file creation is an output of a settled method, not an additional method-selection step.
