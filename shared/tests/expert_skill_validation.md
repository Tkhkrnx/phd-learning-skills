# Expert Collaboration Skill Validation

## Validation Target

The four skills succeed only when both outcomes occur:

1. the task becomes sharper or more executable;
2. the user performs a meaningful expert judgment.

Task progress without visible user reasoning is a failure, even when the answer is technically strong.

Weak facilitation without expert contribution is also a failure. The agent must inspect, model, diagnose, recommend, and critique before asking the user to own the consequential judgment.

## Round-Level Hard Failures

Fail a transcript immediately if a substantive skill response does any of the following:

- completes a full problem, method, architecture, plan, or tutorial before the user judges the current stage;
- advances more than one declared stage;
- asks more than one substantive question;
- uses a confirmation question such as "懂了吗" as the interaction gate;
- asks the user to locate evidence the agent can inspect;
- treats a later user correction as successful collaboration;
- changes frozen decisions without a user choice;
- continues implementation while the collaboration skill remains active;
- claims completion without observable user explanation, construction, comparison, restatement, falsification, or transfer;
- accepts yes/no, approval, or bare option selection as the user's reasoning contribution.
- activates on ordinary writing, review, coding, synchronization, debugging, experiment execution, or execution of an already frozen plan.
- emits a suspension or lifecycle marker after the user requests normal execution.

## Activation Gate

Activation requires either the skill name or a clear matching collaboration intent. Natural-language intent is valid; topic match is not.

- Problem formulation: judge or formulate whether an idea, phenomenon, or claim is a defensible academic problem.
- Method design: find, compare, or defend a solution for an already established research problem.
- Engineering decomposition: analyze or clarify a requirement, inspect the system boundary, or choose a first slice before coding.
- Knowledge closure: learn what one specific concept means well enough to restate and apply it.

The structured trigger suite pairs these with non-triggering tasks from the same domains. A model that activates because a task is difficult, contains research vocabulary, or would benefit from internal decomposition fails the gate.

## Required Round Shape

Every substantive response must contain:

1. a parseable `[skill-run]` line;
2. one declared stage;
3. a compact expert scaffold;
4. one parseable `reasoning-focus` and one open-ended question;
5. a real stop before the next stage.

## Skill-Specific Success Evidence

### `research-problem-formulation`

The user must explain the boundary reasoning, not merely approve agent wording. A complete run includes a user-constructed problem statement and a reasoned response to one dangerous counterexample.

The problem statement must be declarative. A formulation beginning with "how to" is an objective or design question, not the research problem. Do not require every problem to be a contradiction or known capability gap: a supported phenomenon or unresolved condition may be the problem. The run must still test reality, boundary, importance, prior resolution, non-trivial challenge, and researchability.

### `research-method-design`

Through open questions, the user must explain the root challenge, causal source of gain, any transferred design principle, the strongest simpler alternative, and a kill criterion. A complete architecture produced by the agent does not satisfy this.

### `engineering-task-decomposition`

The agent must discover explicit and latent requirements and inspect the system. The user must explain requirement priorities, architecture boundary, trade-off, and first-slice proof. Asking the user to search the repo is not participation.

### `targeted-knowledge-closure`

The user must reconstruct and transfer one concept grain, then distinguish it from a near miss. Explanations must preserve actor, state, and ordering invariants and fade scaffolding after success.

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
3. inspect only the first substantive response;
4. require the declared stage, minimal scaffold, one open-ended reasoning question, and stop;
5. continue for at least one user reply when checking critique and transition behavior;
6. fail if success depends on hidden context from the redesign discussion.

## Static Validation

Run:

```powershell
python shared\tests\validate_expert_skills.py
```

The static validator checks trigger boundaries, required protocol sections, stage names, line budgets, references, and structured regression-case coverage. Static success does not replace transcript forward-testing.

## Acceptance Metrics

- 100% of substantive rounds expose a parseable run state.
- 100% ask exactly one open-ended question that elicits a reasoning chain.
- 0% accept yes/no, approval, or bare option selection as collaboration evidence.
- 0% produce a complete downstream deliverable before that judgment.
- 0% use these skills as agent-only checklists.
- 100% of direct-execution pivots exit the collaboration skill silently and preserve confirmed decisions.
- 0% of ordinary execution requests activate an expert collaboration skill.
- 100% of completion claims cite observable user evidence.
- Next-turn corrections caused by scope drift, platform mismatch, or actor confusion trend downward across real usage.
