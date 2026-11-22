---
name: research-problem-formulation
description: Formulate and pressure-test a systems research problem when the user explicitly invokes this Skill.
---

# Research Problem Formulation

Turn a phenomenon or research idea into a defensible declarative problem, or conclude that the proposed problem is not established.

## First full answer

For a full formulation, deliver these three answers in order, starting with the first synthesis you share for discussion. An explicit request for one part narrows the response to that part.

1. **What the problem is.** Render two separately labeled paragraphs under Question 1, each with one abstract-opening sentence by default. In Chinese, put **背景：** before the sentence introducing the setting, actors and relevant operating conditions. After a blank line put **问题：** before the declarative sentence stating the unresolved difficulty and its consequence in that setting. Use equivalent labels for the requested language. For a detailed guide explicitly requested by the user, expand within those same two paragraphs. Place illustrations and evidence in the later answers.
2. **Why it matters.** Explain who bears the cost, how it arises and which decision or outcome changes. Ground importance in evidence, a concrete case or a credible causal argument. When proposing a motivating experiment, describe the comparison and target outcome in everyday language, including what would weaken the motivation. If the claim is that a factor changes which action works, compare the same viable actions across the relevant conditions and measure the cost of ignoring that factor. Label proposed tests as such. The best action in hindsight gives an upper bound. To claim that recognizing a feature actually helps, choose using only information available before the decision and evaluate on fresh cases.
3. **Why existing work still fails.** Search across the approaches that could answer the current question, following primary sources and strong counterexamples. Organize by method, nearest competitors first, then adjacent approaches and useful background. Use four columns in Chinese: 类别 | 相关工作文章 | 已解决的问题与优势 | 为什么仍不足以解决本文问题. Give each category a short technical name. Use relevance tiers internally to order the rows. Put named papers and source locations in column two. In the last column name the specific part of our question left open and explain why, preserving the distinction between a documented limit and an inferred consequence. Give background work its actual role and credit a route that already solves the problem.

## Core workflow

1. Recover what each consequential statement meant in the conversation. In the problem paragraph, state the difficulty that remains for the affected people or system given the information they already have. Place the user's requested report format with the intended output or agreed idea. For a paper offered as inspiration, recover the aspect the user wants to carry over. Preserve the scope of the current research question. Treat a deployment, dataset or motivating example as one instance unless the user makes it the research population.
2. Identify the affected system object, operating condition, consequence, and evidence boundary. Separate observations from objectives, proposed solutions and causal hypotheses.
3. Build a targeted query portfolio and inspect decisive primary sources before judging reality, importance, prior resolution, non-triviality, or researchability.
4. State the problem without a how-to question or preferred mechanism, then pressure-test the strongest collapse condition.
5. Preserve provisional status whenever decisive evidence or user-owned scope is unresolved.

Give a research judgment supported by the investigation. Explain whether the difficulty occurs, matters enough to study, survives the closest existing solution, and poses a substantive challenge. A well-supported conclusion can narrow the idea, identify a routine engineering fix, or retire the topic.

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

If the user also asks for an agreed core idea, connect it after these answers. Defer team assignments until the requested stage.

Before delivering a completed formulation, follow up on each missing line of work that could change the gap. Put unresolved access limits or genuinely untested comparisons beside the affected rows. A discussion draft can surface an open question while the investigation continues.

Finish only when the user can defend an abstract-level, paper-ready account of: **what the problem is**, **why it matters**, and **why existing work still fails**. The problem itself must be a declarative condition or limitation, not a how-to question or solution objective. Include the evidence boundary and a condition that would narrow or invalidate the framing. If the user asks to move into method design, writing, experiments, or implementation, hand off the confirmed state and continue as normal execution or another explicitly requested Skill.

Put supporting evidence and open tests alongside the relevant motivation or comparison. Preserve scientific qualifiers in the two-sentence opening so a proposed counterexample stays provisional.

For a converged project research task or an explicit file-output request, use [the seven-question output format](../shared/expert-skill-references/seven_question_research_outputs.md) after the first three answers stabilize. Create or update the project's single `写作指南` with Questions 1–3, the supported chapter and figure guidance, and clearly unresolved Questions 4–7. This file output does not replace the evidence search or user collaboration above; early exploratory and conversation-only turns remain live-first.
