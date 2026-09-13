# Agent Collaboration Skill Blueprint

## Purpose

This document defines the shared contract for `research-problem-formulation`, `research-method-design`, `engineering-task-decomposition`, and `targeted-knowledge-closure`. It is a maintenance reference, not a document that every Skill run must load.

These Skills help the user make a consequential research, engineering, or learning judgment. They should add expert evidence and alternatives without taking ownership of decisions that depend on the user's intent.

## Activation

The four primary collaboration Skills are explicit-only through `agents/openai.yaml`. Route to one only when the user explicitly asks to use a Skill or recognizable expert-workflow label for a stated task. An ordinary request to analyze, explain, design, search, write, code, debug, review, or run experiments remains normal assistance.

`explicit-skill-router` is the only implicit entrypoint. It reads `aliases.yaml` when the user explicitly requests a Skill but names it in plain language. If the label is ambiguous, ask one short routing question; do not infer a target from the task topic alone.

Authorization covers the stated collaboration and expires when it completes, the task changes, or the user pivots to direct execution. A new primary expert role requires a new explicit request.

## Collaboration

Start with the useful expert work: inspect available evidence, explain the current model, surface serious alternatives or counterexamples, and identify the decision that remains. Do not make the user reconstruct facts that the agent can inspect.

Interaction is adaptive, not a staged questionnaire. The agent leads with evidence and expert candidates, while the user remains part of consequential framing, design, requirement, and learning judgments. Ask a focused question when the answer could materially change or validate the boundary, recommendation, implementation path, or learning diagnosis. Elicit reasoning, correction, application, or a concrete constraint rather than accepting yes/no approval as convergence. Do not close a consequential collaboration as an agent-only monologue; if the user's supplied reasoning or live application already provides the needed signal, proceed without manufacturing another turn.

Treat agent-generated problem statements, methods, architecture models, and explanations as provisional when a user-owned judgment is still unresolved. Incorporate corrections by updating the affected assumption and downstream conclusion. Do not require ritual restatements, fixed turn counts, arbitrary confidence percentages, or performative questions that add no evidence.

Keep internal routing, stage labels, status fields, and lifecycle mechanics out of normal conversation. Preserve the user's requested structure, language, terminology, and tentative or confirmed status.

## Evidence boundaries

- Separate observation, source-backed fact, inference, hypothesis, and missing evidence.
- Research-problem and method claims about novelty, unresolved status, or superiority require targeted evidence acquisition and decisive-source inspection; use `shared/expert-skill-references/research_evidence_acquisition.md` only for those claims.
- For LLM inference or serving questions that span workload, model, and runtime layers, use `shared/expert-skill-references/llm_inference_three_layer_framework.md`.
- Engineering judgments should inspect the relevant code, interfaces, configuration, tests, or runtime evidence rather than relying on request prose.
- Teaching explanations of processes should preserve actor identity, state, operation, and ordering; verify niche or current facts when they matter.
- Static checks, fixtures, historical data, and live runtime evidence are different proof levels and must not be substituted for one another.

## Frozen decisions

Treat user-confirmed problem statements, requirements, constraints, RQs, evaluation gates, and architecture choices as frozen within the current task. When new evidence conflicts:

1. name the exact conflict;
2. propose the smallest affected revision;
3. ask only if the choice is genuinely user-owned or would materially change scope;
4. update dependent artifacts only after the authority is clear.

Do not reorganize confirmed content merely for a cleaner narrative.

## Supporting Skills

An authorized primary Skill may use another Skill as a bounded dependency without a second request when the subtask is necessary to the same goal, introduces no independent deliverable or external side effect, and returns control to the primary Skill. Use the minimum supporting set.

Examples include academic candidate discovery for a research judgment or a short concept repair that unblocks an engineering decision. Supporting use must not become a new primary workflow, broaden permissions, or outlive the parent task.

Direct implementation, writing, synchronization, experiment execution, data collection, publishing, and other delivery work are normal execution, not supporting collaboration Skills. When the user requests them, preserve confirmed decisions, exit the collaboration protocol silently, and execute within the current authorization and safety boundaries.

## Completion

A collaboration Skill is complete when its requested outcome is usable and no unresolved issue is likely to reverse the next action. State any material residual uncertainty and its consequence.

Outcome examples:

- problem formulation: an abstract-level account of what the problem is, why it matters, why existing work still fails, and what evidence could invalidate it;
- method design: a causal method, feasible carrier, strongest simpler alternative, key assumption, and discriminating evidence;
- engineering decomposition: requirement, relevant architecture slice, chosen path, first reversible implementation slice, validation, and rollback boundary;
- knowledge closure: an accurate working model that the user can apply to the current task, with any remaining misconception identified.

When the user also requested execution, completion requires the normal implementation loop: implement, run, inspect, repair failures caused by the change, and revalidate. Do not stop after a first draft while a safe, in-scope verification or fix remains.

## Failure patterns

- activating a primary Skill from topic similarity or task complexity;
- loading every shared reference before knowing it is needed;
- turning checkpoints into a fixed one-stage-per-turn itinerary;
- asking the user to find evidence or code the agent can inspect;
- manufacturing a failure, novelty claim, challenge, or mechanism to fit a template;
- changing frozen decisions without exposing the conflict;
- treating an artifact, static validator, or polished answer as stronger evidence than it is;
- carrying a Skill into a new task or direct-execution phase without authorization.
