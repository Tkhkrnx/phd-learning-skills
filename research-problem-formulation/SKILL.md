---
name: research-problem-formulation
description: Formulate and pressure-test a systems research problem when the user explicitly invokes this Skill.
---

# Research Problem Formulation

Turn a phenomenon or research idea into a defensible declarative problem, or conclude that the proposed problem is not established.

## Core workflow

1. Recover what each consequential statement meant in the conversation. In the problem paragraph, state the difficulty that remains for the affected people or system given the information they already have. Place the user's requested report format with the intended output or agreed idea. For a paper offered as inspiration, recover the aspect the user wants to carry over.
2. Identify the affected system object, operating condition, consequence, and evidence boundary. Separate observations from objectives, proposed solutions and causal hypotheses.
3. Build a targeted query portfolio and inspect decisive primary sources before judging reality, importance, prior resolution, non-triviality, or researchability.
4. State the problem without a how-to question or preferred mechanism, then pressure-test the strongest collapse condition.
5. Preserve provisional status whenever decisive evidence or user-owned scope is unresolved.

For revisions, recover the user's current objects, intended outcomes and reopened scope before inheriting an old framing. Keep distinct outcomes visible; an illustrative case must not replace the full target. A prior-work gap needs its achieved capability, operative method/assumption, failing condition and consequence; “it lacks our complete system” is not an explanation of failure.

## Collaboration contract

When the user corrects the meaning of a phrase, follow that correction through the motivation, nearest-work comparison and any agreed idea that depends on it. Keep the other confirmed choices. Recover meaning from the surrounding passages in the discussion, project material and applicable references.

Lead with evidence, an expert candidate formulation, and the strongest counterexample rather than a questionnaire. When a user-owned boundary or interpretation can change the problem, ask one focused question that elicits their reasoning, correction, or evidence; yes/no approval alone is not convergence. Do not finish a consequential formulation as an agent-only monologue, but do not manufacture an extra turn when the user's supplied reasoning already resolves the boundary.

## Load on demand

- Read [deep formulation workflow](references/deep-workflow.md) for a broad new problem, a contested prior-work boundary, or revision of a frozen problem/RQ package.
- Read `../shared/expert-skill-references/research_evidence_acquisition.md` for every new-problem judgment and before revising any claim about importance, novelty, or unresolved status; use its problem-boundary route only.
- Read `../shared/expert-skill-references/llm_inference_three_layer_framework.md` only when an LLM inference/serving problem spans model, workload, and runtime layers.
- Use `topic-paper-finder` only as a bounded academic-discovery backend when the current evidence search needs it.
- If the user explicitly appoints an expert peer to answer or challenge this work, read [authorized expert-peer collaboration](../shared/expert-skill-references/expert_peer_collaboration.md); otherwise keep the ordinary human collaboration above.

## Boundaries

- A problem remains meaningful after removing the proposed solution. “How to optimize X”, “build X”, and “we lack our X” are objectives or solution requests, not problem statements.
- Do not invent a failure, cause, metric, or literature gap to make a candidate look academic.
- Keep problem, challenge, mechanism, and experimental RQ distinct.
- Treat snippets and broad literature volume as discovery signals, not proof.
- Preserve confirmed wording and evidence roles during revision unless the user reopens them.

## Completion

For a project synthesis, present the three answers below as a connected paper-ready account on the first turn. Open with the difficulty that survives given the records and tools already available. A question heading takes a declarative answer. Preserve the decisive source comparison even in a short version. If the request also covers an agreed core idea, explain how it follows from the gap. Keep examples subordinate to the argument and defer later assignments, including questions about their logistics, until the user moves on.

Finish only when the user can defend an abstract-level, paper-ready account of: **what the problem is**, **why it matters**, and **why existing work still fails**. The problem itself must be a declarative condition or limitation, not a how-to question or solution objective. Include the evidence boundary and a condition that would narrow or invalidate the framing. If the user asks to move into method design, writing, experiments, or implementation, hand off the confirmed state and continue as normal execution or another explicitly requested Skill.

For an abstract or PPT problem paragraph, give concise background plus the declarative difficulty and consequence. Keep source checks, untested explanations and collapse conditions separately inspectable rather than inserting process warnings into the prose. Retain qualifications that change its scientific meaning; a short answer must not become a stronger claim. In particular, do not turn a proposed counterexample into an observed failure when compressing: an unresolved guarantee or possible consequence is not a measured distortion.

For a converged project research task or an explicit file-output request, use [the seven-question output format](../shared/expert-skill-references/seven_question_research_outputs.md) after the first three answers stabilize. Create or update the project's single `写作指南` with Questions 1–3, the supported chapter and figure guidance, and clearly unresolved Questions 4–7. This file output does not replace the evidence search or user collaboration above; early exploratory and conversation-only turns remain live-first.
