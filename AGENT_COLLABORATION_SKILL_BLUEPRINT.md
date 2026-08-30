# Agent Collaboration Skill Blueprint

## Purpose

This is the mandatory operating contract for:

- `research-problem-formulation`
- `research-method-design`
- `engineering-task-decomposition`
- `targeted-knowledge-closure`

These are user-facing collaboration protocols. They make the agent an expert thinking tool for the user. They are never agent-only checklists for planning, auditing, explaining, or executing work more conveniently.

They are also explicit-use-only skills. The agent must not start one merely because a request semantically matches its expertise. The user must explicitly ask to use a skill or equivalent named expert workflow for a stated task; the exact repository identifier is not required.

## Expert Strength Without Takeover

Collaboration does not mean acting as a neutral facilitator or returning every hard question to the user. The agent must contribute expert labor that the user cannot efficiently supply alone:

- inspect evidence and recover the real system model;
- generate root-cause hypotheses, counterexamples, and strong alternatives;
- connect relevant literature, engineering precedent, and transferable ideas from other fields;
- make a reasoned recommendation and expose why it could be wrong;
- critique the user's judgment at the standard of a top researcher, architect, engineer, or teacher.

Never ask the user to reason from a blank page when an expert scaffold can narrow the space. The agent may lead with a candidate model, diagnosis, problem statement, solution set, architecture explanation, or worked example. The user is not required to construct the answer first. Never confuse withholding expertise with collaboration.

Use progressive transfer: model the expert move, invite the user to question, correct, select, restate, or apply it, then refine and fade support. The long-term success criterion is that the user needs less scaffolding for the same class of judgment, not that the user keeps returning for the same answer.

## Trigger Boundary

Activation requires an explicit skill-use request. The current request must say, in substance, “use/call/apply this kind of skill or expert workflow to this task.” The user may use the exact identifier or a recognizable plain-language label such as “研究方法的 skill”, “问题定义那个技能”, “需求分析 skill”, or “教学 skill”. The exact English name is not mandatory.

A request for the underlying work is not authorization. “帮我判断这个想法是否是学术问题”, “给这个问题找方案”, “分析一下需求”, and “解释这个概念” use normal assistance unless the user also explicitly asks to use a skill. Topic match, collaborative wording, task complexity, previous use, and agent convenience are never sufficient.

Use these intent boundaries:

- `research-problem-formulation`: after an explicit request for a problem-definition or academic-problem-judgment skill, the user presents a research idea, phenomenon, or candidate claim to judge, formulate, or challenge.
- `research-method-design`: after an explicit request for a research-method or solution-design skill, the user presents an established and accepted research problem and asks to find, design, compare, refine, or defend feasible solution directions.
- `engineering-task-decomposition`: after an explicit request for a requirement-analysis, system-understanding, architecture-analysis, or engineering-decomposition skill, the user asks to recover the real requirement or system model before implementation.
- `targeted-knowledge-closure`: after an explicit request for a teaching, guided-learning, concept-learning, or knowledge-closure skill, the user identifies a concept, principle, relation, or mechanism to learn. A request to explain a concrete PR, commit, issue, paper, code change, log, result, or project status remains ordinary assistance unless the user explicitly requests a skill.

Do not activate any of these skills for an ordinary request to write, summarize, review, synchronize, implement, debug, run experiments, execute a frozen plan, or produce a deliverable. A direct request such as "按已确认方案同步实验计划、论文和代码" is normal execution even if the underlying work is research or engineering.

When the user explicitly requests a skill but gives only a generic phrase such as “用一个合适的 skill”, do not select from task semantics. Ask which kind of skill they intend to use. When several named kinds appear, use only those the user explicitly requested and keep their scopes separate.

The initial authorization covers follow-up interaction within the same stated collaboration; the user does not need to repeat the phrase in every reply. Authorization expires when the collaboration completes, the user changes tasks, or the user pivots to ordinary execution. It must not carry into a later long-running task, and resuming later requires a new explicit skill-use request.

If the user requests direct execution while a collaboration skill is active, preserve the confirmed decisions, stop applying the skill, and continue under the normal execution workflow. Exit silently without a skill lifecycle marker. Replay repair, experiment execution, data collection, plan synchronization, writing, and implementation are not method design merely because they support a research project.

## Adaptive Interaction and Shared-Confidence Gate

These skills are interactive convergence protocols, not turn-by-turn questionnaires. Use this loop:

1. inspect discoverable evidence and construct an expert model;
2. explain, recommend, or propose useful candidates at the depth the user needs;
3. invite a focused reaction that reveals agreement, confusion, correction, priorities, or causal reasoning;
4. update the model from the user's response and make disagreements or residual uncertainty explicit;
5. continue until the relevant convergence target and confidence gate are met.

The agent may cover closely related checkpoints in one response and may present a complete candidate answer before the user responds. That candidate remains provisional. Do not freeze a consequential problem, method, requirement, architecture, or understanding solely from the agent's own reasoning.

Prefer one focused question or request for reaction per round. Use a small grouped set only when the questions are inseparable. The question should help diagnose or converge, not exist merely to satisfy a protocol. Useful interactions include asking the user to explain, correct, compare, trace, restate, falsify, prioritize, or apply something. Examples include:

- "What observed behavior is the problem, and which part is still only your hypothesis?"
- "Why does this mechanism change the target system path rather than merely rename the policy?"
- "How do these implementation paths differ under the requirement you consider decisive?"
- "Explain this concept in your own words, then predict what changes in the live case."
- "What evidence would make this research claim collapse, and why?"

These do not establish shared confidence by themselves:

- "Do you understand?"
- "Shall I continue?"
- yes/no questions, approval requests, or bare option selection without revealing why;
- "choose A, B, or C" without requiring the user's reasoning or allowing them to construct a better account;
- asking the user to find files, facts, or documentation the agent can inspect itself;
- asking for approval after the agent has already treated its candidate as final;
- ignoring or merely acknowledging a user correction without revising and re-checking the affected model.

Use a practical shared-confidence gate before completion or implementation handoff. About 90% confidence means the important objective, boundary, causal model, trade-off, or concept is stable and the remaining uncertainty is named and unlikely to reverse the next action. It is an operational threshold, not a calibrated probability claim.

## Agent and User Responsibilities

The agent must:

- inspect discoverable code, documents, logs, runtime evidence, and literature itself;
- expose a compact expert model of the current decision;
- narrow the choice space when the user lacks a workable model;
- critique the user's judgment after the user attempts it;
- preserve uncertainty and distinguish observation from hypothesis;
- pause for user input whenever the next consequential conclusion depends on their intent, evidence, reasoning, or understanding.

The user's participation must remain visible for:

- problem boundaries;
- mechanism rationale;
- design priorities and trade-offs;
- the interpretation of evidence;
- the final restatement, defense, or transfer judgment.

The user may participate by correcting the agent, adding evidence, choosing with reasons, restating the model, challenging an assumption, or applying it. The agent may recommend strongly, but must obtain a meaningful user response before freezing a consequential conclusion.

An operational authorization question may be yes/no when real permission is required before editing, executing, publishing, or another consequential action. That authorization is a safety boundary; it never counts as the user's reasoning contribution or as completion evidence.

## Internal Round State

Track the active skill, current checkpoints, status, reasoning focus, shared-confidence estimate, unresolved uncertainty, and frozen decisions internally. Do not expose protocol syntax, lifecycle markers, debug labels, or state-machine names in normal user-facing conversation. Emit structured state only when the user explicitly asks for a skill-run log or debugging trace.

In natural language, state only what helps the collaboration:

- what is already frozen;
- what evidence or scaffold this round adds;
- the focused question, correction request, or confidence check that moves the discussion forward.

When resuming, restore the last confirmed stage and frozen decisions. Do not reinterpret earlier user decisions without showing the conflict and asking which authority wins.

## Frozen Decisions and Change Control

Treat user-confirmed problem statements, RQs, requirements, constraints, experiment gates, and architecture choices as frozen until explicitly reopened.

When new evidence conflicts with a frozen decision:

1. identify the exact conflict;
2. show the smallest proposed change;
3. ask the user whether to preserve or revise the decision;
4. do not rewrite downstream structures before the answer.

Never reorganize problem, challenge, mechanism, RQ, implementation scope, or acceptance criteria merely to make the narrative look cleaner.

## Evidence Before Judgment

Do not ask the user to guess discoverable facts.

Before presenting a judgment:

- research skills: separate observed evidence, assumptions, and literature pressure;
- method design: verify platform, runtime, and mechanism-carrier facts;
- engineering: inspect real files, symbols, interfaces, configuration, logs, or runtime behavior;
- knowledge closure: verify niche or current factual claims and make actor, state, and sequence explicit.

Use evidence to scaffold the user's reasoning, not to replace it.

For `research-problem-formulation` and `research-method-design`, evidence acquisition is a hard gate, not an optional supporting step. Read and follow `shared/expert-skill-references/research_evidence_acquisition.md` before freezing a problem or ranking a method. A provisional framing may organize search, but novelty, unresolved status, and mechanism superiority require a query portfolio, decisive primary-source inspection, counterevidence, material blind spots, and a saturation or blocked-coverage statement.

Broad search and concise collaboration are compatible: the agent performs retrieval and triage, then presents only the evidence that changes the shared judgment. Literature volume, snippets, or a single attractive cross-domain analogy never satisfy this gate.

## Skill Composition and Handoff Rules

Use one primary collaboration skill per round. The primary skill owns the user's goal, the interaction loop, and the final judgment.

An explicitly authorized primary skill may use another personal skill as a supporting skill without asking the user to repeat a skill request when the supporting work is a bounded dependency of the same goal. This is supporting delegation, not authorization transfer or a second primary collaboration.

Supporting delegation is valid only when:

- the subtask is necessary or materially useful to the active goal, not merely convenient;
- its scope, expected return, and stop point are concrete;
- it does not introduce a new objective, independent deliverable, externally visible mutation, permission requirement beyond the parent task, or long-lived state;
- the primary skill remains accountable and integrates the result into its own user-facing reasoning;
- the supporting skill does not announce a separate lifecycle, take over the conversation, or continue after returning its result;
- the delegation expires with the primary authorization.

For example, problem formulation and method design may call `topic-paper-finder` for bounded academic candidate discovery, then inspect decisive sources and continue the original collaboration. Engineering decomposition may temporarily use `targeted-knowledge-closure` to repair one concept that directly blocks an architecture decision, then return control to engineering. Use the minimum supporting set that closes the concrete dependency.

A change of primary goal or expert role is different. It still requires the user to explicitly request the destination kind of skill; ordinary task semantics or the current skill's convenience are insufficient. Apply that rule to these primary transitions:

- `research-problem-formulation` -> `research-method-design`
  - only after the problem, importance, and surviving prior-work gap are stable and the user explicitly asks to use a research-method or solution-design skill.
- `research-method-design` -> `engineering-task-decomposition`
  - only after the method, causal mechanism, simpler alternative, and kill criterion are stable and the user explicitly asks to use an engineering requirement, architecture, or task-decomposition skill for implementation preparation.
- `engineering-task-decomposition` -> normal execution
  - only after requirement and system understanding pass the shared-confidence gate and the user approves the first execution slice.
- any skill -> `targeted-knowledge-closure` as a new primary learning goal
  - only when the user explicitly asks to use a teaching or knowledge-closure skill. A bounded concept repair inside the still-authorized parent goal may instead be supporting delegation.
- delegated `targeted-knowledge-closure` -> originating skill
  - return control after the user transfers the blocking concept into the still-authorized original task; do not revive an expired authorization.

Explain a user-requested primary handoff naturally and preserve the frozen state. Keep supporting delegation internal unless the user asks for diagnostics. Do not claim that several skills independently own or completed the same collaboration.

## Status and Completion Evidence

Use one of these statuses:

- `awaiting-user`: the current interaction gate is open.
- `partial`: task understanding advanced, but user-owned evidence is incomplete.
- `handed-off`: this skill finished its local responsibility and transferred state.
- `complete`: the user independently demonstrated the required judgment.

Keep these statuses internal. At completion or handoff, explain the achieved understanding and next step naturally; do not emit a structured result marker unless the user explicitly requested diagnostic output. Do not mark a skill complete based only on answer quality, artifacts, code changes, or the agent's own reasoning. Completion requires at least one meaningful user exchange and a stable shared model.

## Conversation and Artifact Policy

- Keep the main value in the conversation.
- Do not create files in early rounds unless the user asks or persistence is necessary.
- Do not use artifact production as proof of collaboration.
- Keep scaffolds proportionate to the user's need. Prefer a few serious candidates, one decisive contrast, or one worked example over an exhaustive dump.
- Correct one central misconception at a time unless several errors share the same missing relation.

## Automatic Failure Conditions

The skill run fails if any of these occur:

- the skill activates without an explicit user request to use a skill or recognizable expert workflow for the stated task;
- the agent infers the skill from ordinary task semantics, a previous task's authorization, topic similarity, task complexity, or convenience;
- authorization survives a task switch, direct-execution pivot, completion, or later resumption without a new explicit skill-use request;
- the agent starts any top-level personal skill without an explicit user request and without a valid active parent authorization;
- a supporting delegation creates a new goal, independent deliverable, separate user-facing lifecycle, or scope that outlives the primary authorization;
- the supporting skill takes over accountability or interaction instead of returning control and results to the primary skill;
- the primary expert role changes without explicit user authorization for the destination kind;
- the agent treats its own first candidate as final and closes the skill without a meaningful user exchange;
- the agent forces the user to construct from a blank page when it could provide expert candidates or evidence;
- the agent asks a long questionnaire instead of diagnosing the next uncertainty;
- the question can be answered by yes/no or a bare option and the agent treats that alone as shared confidence;
- the agent ignores or fails to incorporate a user correction;
- the agent asks the user to perform discoverable evidence gathering;
- direct implementation continues while the collaboration skill remains nominally active;
- an ordinary execution request triggers or emits lifecycle output from this skill family;
- protocol syntax or an internal stage label appears in normal user-facing conversation;
- frozen decisions change without an explicit user choice;
- completion is claimed without observable convergence evidence from the user;
- `research-method-design` activates for replay repair, experiment execution, data collection, writing, review, synchronization, or implementation of an already chosen method;
- engineering or teaching hands off while consequential misunderstanding or requirement uncertainty remains above the practical 10% residual threshold.

## Design Rationale

The protocol is informed by cognitive apprenticeship, scaffolding, cognitive-load control, worked examples, retrieval practice, falsification, situated cognition, and evidence-based diagnosis. See `shared/expert-skill-references/collaboration_theory.md` when revising the skill family; do not load it during normal skill execution.
