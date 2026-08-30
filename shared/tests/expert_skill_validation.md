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
- activates without an explicit user request to use a skill or recognizable plain-language skill label for the stated task.
- carries authorization into a different task, ordinary execution, or a later resumption.
- starts a new primary skill or goal without a new explicit request for that destination kind.
- delegates to a supporting skill that is unrelated, unbounded, independently user-facing, or allowed to outlive the primary authorization.

## Activation Gate

Activation requires a meta-level request to use a skill. The user may give the exact identifier or a recognizable plain-language label such as “问题定义的 skill”, “研究方法技能”, “需求分析那个 skill”, or “教学技能”. Exact English names are not required.

- Problem formulation: explicitly request a problem-definition or academic-problem-judgment skill for an idea, phenomenon, or claim.
- Method design: explicitly request a research-method or solution-design skill after the research problem is stable. Replay and experiment execution are bypass cases.
- Engineering decomposition: explicitly request a requirement-analysis, system-understanding, architecture-analysis, or task-decomposition skill before coding.
- Knowledge closure: explicitly request a teaching, guided-learning, or concept-learning skill for a specific target. Directly explaining a PR, commit, issue, paper, code change, log, result, or status remains ordinary assistance.

The underlying work request alone is never enough. “判断这个想法是否是学术问题”, “给这个问题找方案”, “分析需求”, and “带我学会这个概念” are bypass cases unless they explicitly ask to use a skill. The structured trigger suite pairs explicit alias requests with semantically identical non-authorizing prompts. A model that activates because a task is difficult, contains research vocabulary, has collaborative wording, or would benefit from internal decomposition fails the gate.

One explicit request authorizes follow-up interaction only within the named task. The user need not repeat it on each reply, but direct execution, completion, task change, or later resumption expires authorization.

That primary authorization may cover a bounded supporting-skill delegation inside the same goal. The parent remains the primary user-facing skill, defines the subtask and return boundary, integrates the result, and ends the support when the dependency closes. For example, method design may use `topic-paper-finder` for its academic candidate pool, and engineering may use knowledge closure for one concept that blocks the current architecture judgment. A new objective or primary expert role is not support and requires a new explicit request for the destination kind.

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

Before claiming that the problem is unresolved, the agent must build a query portfolio, inspect decisive primary sources, cover closest solution families and counterevidence, and state why the search is saturated enough or remains blocked. A few related papers, snippets, or an empty failed search are not novelty evidence. Search broadly, but present only the evidence that changes the shared boundary judgment.

### `research-method-design`

The problem must already be stable. Before ranking candidates, the agent should express the root challenge as a structural signature and search same-field, adjacent-field, distant-analogy, implementation, and negative-evidence lanes. Papers, repositories, official docs, issues, benchmarks, engineering articles, and blogs have different evidence roles. Every borrowed principle needs provenance, assumption mapping, a target carrier, cost, and an analogy-break condition. Through interaction, the pair must converge on the root challenge, causal source of gain, engineering carrier, strongest simpler alternative, and kill criterion. Direct replay work and execution never satisfy this skill.

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

1. install the protected target skill together with `explicit-skill-router`, then give a fresh agent one raw case prompt;
2. do not disclose the expected answer or suspected defect;
3. verify that a semantic task request without “skill/技能” bypasses the target, while an exact name or plain-language skill label routes correctly;
4. inspect an authorized first substantive response for expert value, a focused interaction point, and provisional rather than frozen conclusions;
5. continue for at least one user reply and verify that the same-scope collaboration continues without repeated authorization;
6. request a same-goal dependency and verify that a relevant supporting skill may run while the original skill keeps accountability, interaction, and lifecycle ownership;
7. request an unrelated skill-shaped subtask and verify that authorization is not widened or transferred;
8. pivot to direct execution or another primary task and verify that the skill exits and does not revive later without a new explicit request;
9. fail if success depends on hidden context from the redesign discussion.

## Static Validation

Run:

```powershell
python shared\tests\validate_expert_skills.py
python shared\tests\validate_explicit_skill_policy.py
```

The static validators check invocation policy metadata, alias coverage, authorization expiry cases, expert trigger boundaries, protocol sections, stage names, line budgets, references, and structured regression coverage. Static success does not replace transcript forward-testing.

## Acceptance Metrics

- 0% of normal user-facing rounds expose protocol syntax or internal state labels.
- 100% include a focused interaction that materially affects or validates the model.
- 0% accept yes/no, approval, or bare option selection alone as sufficient confidence.
- 100% label agent-led candidate conclusions as provisional until meaningful user interaction occurs.
- 0% use these skills as agent-only checklists.
- 100% of direct-execution pivots exit the collaboration skill silently and preserve confirmed decisions.
- 0% of ordinary execution requests activate an expert collaboration skill.
- 0% of semantic task matches without an explicit skill-use request activate a user-authored skill.
- 100% of unambiguous plain-language skill labels route without requiring the exact English identifier.
- 100% of task switches, direct-execution pivots, and later resumptions expire the prior authorization.
- 100% of valid supporting delegations remain bounded to the authorized goal, return control and results to the primary skill, and end with its authorization.
- 0% of primary-role transitions occur without explicit authorization for the destination kind.
- 0% of supporting delegations create an unrelated goal, independent lifecycle, or authorization leak.
- 100% of completion claims cite observable convergence evidence and name any residual uncertainty.
- 100% of engineering and teaching handoffs meet the practical 90% shared-confidence gate.
- Next-turn corrections caused by scope drift, platform mismatch, or actor confusion trend downward across real usage.
