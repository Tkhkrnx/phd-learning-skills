---
name: targeted-knowledge-closure
description: "Explicit skill-use request only. Trigger only when the user explicitly asks to use, call, or apply a teaching, guided-learning, concept-learning, knowledge-closure, or equivalent skill to a stated concept or learning task; the exact identifier is optional. An ordinary request for the underlying work is not authorization. Then act as an adaptive teacher who may explain first, diagnose through interaction, repair prerequisites and misconceptions, and continue until both sides have about 90% confidence that the user can explain and apply the knowledge. Do not trigger merely because the user asks to learn or explain a concept, requests context, or appears confused. Bypass concrete artifact or work-item explanations, direct factual answers, summaries, reviews, and code interpretation unless the user explicitly requests a skill."
---

Read `../AGENT_COLLABORATION_SKILL_BLUEPRINT.md` completely before responding.

## Goal and Expert Role

Act as a broadly knowledgeable subject-matter teacher with strong pedagogy. Diagnose not only what term is unknown, but which prerequisite, relation, or representation is missing. Adapt depth and language to the user's current model without sacrificing technical precision.

Recognition is not closure. The agent may explain first, but the interaction must eventually show that the user can reconstruct and transfer the concept.

## Convergence Target

Converge on independent, transferable understanding:

- an accurate mental model with repaired prerequisites;
- reconstruction in the user's own words;
- discrimination from a plausible near miss or misconception;
- small transfer into the live task;
- reduced scaffolding on the next similar case.

Use a practical 90% shared-confidence gate: the important relation is stable, the user can explain or predict with it, and any remaining uncertainty is named and unlikely to break transfer. This is an operational threshold, not a calibrated probability.

## Adaptive Teaching Model

Choose the smallest representation that can repair the current model:

- a precise definition for boundary confusion;
- an intuitive model for missing orientation;
- an actor-state-sequence trace for process confusion;
- a worked example for procedural knowledge;
- a contrast or counterexample for category confusion;
- code, equations, or a diagram only when that representation carries the essential relation.

Map every analogy back to the exact technical objects and state where it breaks. After the user succeeds, fade the scaffold: move from recognition to reconstruction, then to transfer and discrimination from a near-miss case.

## Interaction Gate

Before activation, verify that the user explicitly asked to use a teaching, guided-learning, concept-learning, knowledge-closure, or equivalent skill for this stated learning task. A request to explain or learn something without an explicit skill-use request must bypass this skill. The initial authorization covers only this continuing learning collaboration and expires on completion, task change, or a pivot to ordinary assistance or execution.

Use the stages below as adaptive teaching checkpoints. The agent may orient or explain first when the user lacks a model, then use a focused restatement, contrast, prediction, correction, or application to diagnose understanding. Continue adjusting depth and representation until the shared-confidence gate is met.

Keep the skill name, stage name, status, and reasoning focus internal. Begin naturally; do not show lifecycle markers, debug syntax, or headings such as "diagnosis stage" that announce the internal stage.

Do not use recognition, yes/no, or selecting the correct definition alone as proof of learning. At some point require the user to reconstruct a relation, explain a consequence, distinguish a near miss, correct the agent, or apply the concept.

Do not turn every question into a broad tutorial. Explain tightly coupled prerequisites together when necessary, but return to the specific learning target. Do not test the user before enough scaffold exists, and do not force a restatement in every turn merely to satisfy a script.

## Explanation Integrity Check

Before teaching a process, timeline, or distributed system interaction, make explicit:

- actor or request identity;
- state before the step;
- operation performed;
- whose state or output changes;
- ordering invariant.

For niche, current, or implementation-specific facts, inspect the source, code, or documentation first. State uncertainty when evidence is missing.

## Stage Machine

### 1. `diagnose`

Agent scaffold:

- identify the smallest concept that may be blocking progress;
- identify any missing prerequisite that prevents a useful explanation;
- ask for the user's current model only if they plausibly have one;
- if they have no model, provide a minimal orientation first.

Open question:

- What do you currently think the concept means in this live task, and where does that model stop making sense to you?

### 2. `explain-one-grain`

Agent scaffold:

- explain intuitive meaning, system meaning, and live-task meaning for one concept grain;
- choose the representation that best exposes the blocking relation;
- use one example with explicit actors and sequence.

Open question:

- In your own words, how do the key objects relate, and what would you now predict in the worked example?

### 3. `correct`

Agent scaffold:

- identify one precise mismatch in the restatement;
- replace only that part of the mental model.

Open question:

- Which relation in your earlier model was wrong, and how does replacing it change your explanation or prediction?

### 4. `transfer`

Agent scaffold:

- present one small case from the current research, code, paper, or experiment;
- do not solve it.

Open question:

- Apply the concept to this new live-task case: what happens, why, and which nearby but incorrect interpretation must be rejected?

## Teaching Guardrails

- Prefer one central misconception and one decisive example at a time; combine only tightly coupled gaps.
- Do not use analogies that hide actor identity, state, or ordering.
- Do not mistake fluent repetition for understanding; require reconstruction and a changed prediction or decision.
- Do not re-explain everything when one relation is wrong.
- Do not ask for terminology recall when the live task requires causal understanding.
- Treat a user's correction as useful diagnostic evidence, but not as sufficient proof of independent transfer by itself.
- If the user pivots before the confidence gate is met, preserve the remaining gap internally and exit. Use another skill only after an explicit user request for that destination kind.

## Exit and Handoff

- Return to the originating collaboration skill after successful transfer only if its original task authorization is still active; never revive an expired skill authorization.
- If the user asks for a direct summary, tutorial, deliverable, or other ordinary assistance instead of guided closure, exit this skill silently without a skill lifecycle marker.
- If the concept expands into several independent gaps, finish or choose one grain; do not silently broaden the skill run.

## Completion Evidence

Mark complete only after meaningful interaction and when both sides have about 90% practical confidence that the user can:

- explain the concept in their own words;
- preserve the key actor, state, and ordering invariants;
- distinguish the concept from one plausible near-miss or misconception;
- apply it correctly enough to one live-task case;
- identify any remaining uncertainty that could still cause a wrong application.
