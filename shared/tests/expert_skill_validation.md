# Expert Collaboration Skill Validation

## Validation Target

The four skills succeed only when both outcomes occur:

1. the task becomes sharper or more executable;
2. the agent and user converge through meaningful interaction rather than an agent-only monologue.

The agent may lead with a strong candidate answer, diagnosis, solution set, architecture explanation, or lesson. The user is not required to construct first. The candidate must remain revisable until the conversation supplies correction, rationale, restatement, application, or another meaningful confidence signal.

Weak facilitation without expert contribution is also a failure. The agent must inspect, model, diagnose, recommend, and critique before asking the user to own the consequential judgment.

## Round-Level Hard Failures

Fail a transcript immediately if a substantive skill response does any of the following:

- treats its first problem, method, architecture, plan, or tutorial as final without a meaningful user exchange;
- forces the user to construct from a blank page when expert candidates would help;
- asks a long questionnaire instead of targeting the next uncertainty;
- uses a confirmation question such as "懂了吗" as the interaction gate;
- asks the user to locate evidence the agent can inspect;
- ignores or fails to incorporate a later user correction;
- changes frozen decisions without a user choice;
- continues implementation while the collaboration skill remains active;
- claims completion without observable convergence evidence from the user;
- accepts yes/no, approval, or bare option selection as the user's reasoning contribution.
- activates on ordinary writing, review, coding, synchronization, debugging, experiment execution, or execution of an already frozen plan.
- emits a suspension or lifecycle marker after the user requests normal execution.
- exposes a skill name, stage, status, reasoning-focus label, or lifecycle marker in normal user-facing conversation.
- activates `research-method-design` for replay repair, experiment execution, data collection, result audit, writing, synchronization, or implementation of a chosen method.
- hands engineering or teaching work off while a consequential requirement or understanding gap remains above the practical ten-percent residual threshold.

## Activation Gate

Activation requires either the skill name or a clear matching collaboration intent. Natural-language intent is valid; topic match is not.

- Problem formulation: judge or formulate whether an idea, phenomenon, or claim is a defensible academic problem.
- Method design: after a research problem is stable, find, generate, compare, refine, or defend feasible solutions. Replay and experiment execution are explicit bypass cases.
- Engineering decomposition: analyze or clarify a requirement, understand the system deeply, compare implementation paths, or choose a first slice before coding.
- Knowledge closure: learn a specific concept, principle, relation, or mechanism well enough to restate and apply it. Directly explaining a PR, commit, issue, paper, code change, log, result, or status is ordinary assistance.

The structured trigger suite pairs these with non-triggering tasks from the same domains. A model that activates because a task is difficult, contains research vocabulary, or would benefit from internal decomposition fails the gate.

## Required Round Shape

Every substantive skill run must show this adaptive loop in natural language:

1. evidence-backed expert explanation, recommendation, or candidates;
2. a focused request for correction, reasoning, priority, restatement, prediction, or application;
3. an update based on the user's response;
4. continued interaction until the convergence target and practical 90% shared-confidence gate are met.

A response may connect several related checkpoints. Prefer one focused question per round, but do not manufacture a question or force a restatement merely to satisfy a script.

The active skill, internal stage, status, and reasoning focus must not be shown unless the user explicitly requests diagnostic output.

## Skill-Specific Success Evidence

### `research-problem-formulation`

The agent may propose the first problem statement. A complete run includes meaningful user correction, refinement, or reasoned acceptance and a response to one dangerous counterexample. The first candidate must not be frozen unilaterally.

The problem statement must be declarative. A formulation beginning with "how to" is an objective or design question, not the research problem. Do not require every problem to be a contradiction or known capability gap: a supported phenomenon or unresolved condition may be the problem. The run must still test reality, boundary, importance, prior resolution, non-trivial challenge, and researchability.

### `research-method-design`

The problem must already be stable. The agent should proactively offer several feasible solution directions and relevant or cross-domain principles. Through interaction, the pair must converge on the root challenge, causal source of gain, engineering carrier, strongest simpler alternative, and kill criterion. Direct replay work and execution never satisfy this skill.

### `engineering-task-decomposition`

The agent must discover explicit and latent requirements, inspect the system, and explain the relevant architecture. Interaction continues until the agent is about 90% confident in the real need and the user is about 90% confident in the requirement or system model. The percentage is a practical gate, evidenced by stable restatement, boundaries, trade-offs, first-slice proof, and named residual uncertainty.

### `targeted-knowledge-closure`

The agent may explain first, then diagnose through reaction, correction, prediction, or restatement. Continue until both sides have about 90% confidence that the user can reconstruct and transfer the concept and distinguish it from a near miss. Explanations must preserve actor, state, and ordering invariants and fade scaffolding after success.

## Real-Usage Regression Cases

The structured cases live in `expert_skill_transcript_cases.yaml`.

They cover these observed failures:

1. NPU no-restart method design proposed a platform-misaligned path before a fact gate.
2. One adapter failure over-invalidated an otherwise usable replay cohort.
3. A problem/challenge/RQ revision changed frozen roles before user approval.
4. A full acceptance matrix and a fast CI sentinel were initially conflated.
5. A chunked-prefill explanation hid that decode and prefill belonged to different requests.
6. Direct implementation and synchronization requests incorrectly activated or kept a collaboration skill active.
7. A pipeline explanation used engineering decomposition instead of pausing for concept closure.
8. A user correction occurred only after the agent had already completed the judgment.

## Forward-Test Procedure

For each skill:

1. give a fresh agent only the skill and one raw case prompt;
2. do not disclose the expected answer or suspected defect;
3. inspect the first substantive response for expert value, a focused interaction point, and provisional rather than frozen conclusions;
4. continue for at least one user reply and verify that the agent revises or confirms its model from that reply;
5. check that the run stops only after the relevant confidence gate or exits silently on a direct-execution pivot;
6. fail if success depends on hidden context from the redesign discussion.

## Static Validation

Run:

```powershell
python shared\tests\validate_expert_skills.py
```

The static validator checks trigger boundaries, required protocol sections, stage names, line budgets, references, and structured regression-case coverage. Static success does not replace transcript forward-testing.

## Acceptance Metrics

- 0% of normal user-facing rounds expose protocol syntax or internal state labels.
- 100% include a focused interaction that materially affects or validates the model.
- 0% accept yes/no, approval, or bare option selection alone as sufficient confidence.
- 100% label agent-led candidate conclusions as provisional until meaningful user interaction occurs.
- 0% use these skills as agent-only checklists.
- 100% of direct-execution pivots exit the collaboration skill silently and preserve confirmed decisions.
- 0% of ordinary execution requests activate an expert collaboration skill.
- 100% of completion claims cite observable convergence evidence and name any residual uncertainty.
- 100% of engineering and teaching handoffs meet the practical 90% shared-confidence gate.
- Next-turn corrections caused by scope drift, platform mismatch, or actor confusion trend downward across real usage.
