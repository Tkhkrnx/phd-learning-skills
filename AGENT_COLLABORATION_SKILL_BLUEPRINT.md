# Agent Collaboration Skill Blueprint

This repository-level blueprint defines the shared collaboration rules for all personal PhD learning skills.

## Shared Purpose

- accelerate research, engineering, and learning work with an agent
- keep first-pass modeling, decisions, and transfer with the user

## Two System-Level Risks

### Risk 1: artifact fatigue

In high-pressure work, the user may avoid the workflow if it always requires full artifact production.

### Risk 2: workflow theater

The user may appear to follow the workflow while skipping real evidence judgment, real tradeoff thinking, or real independent recall.

Both risks must be addressed structurally, not only by reminders.

## Shared Rules

1. Require a user-first draft.
2. Keep the agent in one role per round.
3. Require an explicit user decision record at branch points.
4. Use fixed artifact schemas.
5. Define stop rules for both round and skill completion.
6. Require an agent-off completion check.
7. Tie engineering claims to inspected evidence.

## Shared Invocation Guidance

A user should be allowed to invoke a skill with a short request such as:

- "Use `research-problem-formulation` and help me define the problem."
- "Use `engineering-task-decomposition` for this requirement."
- "Use `targeted-knowledge-closure` for this concept."

The skill must not assume the user remembers the required template.

Instead, every skill should begin with an invocation handshake:

1. identify the skill and its immediate goal in one sentence
2. ask for only the minimum viable first draft
3. if the user is overwhelmed, offer a 2 to 3 bullet fallback version
4. only after the user answers, expand into the first artifact

The handshake should reduce startup friction, not add a new ritual.

## Shared Artifact Language Policy

Artifacts should default to the user's working language.

For this repository and its intended usage:

- when the user works in Chinese, artifact titles, section headers, and analysis text should default to Chinese
- keep paper titles, system names, API names, and other proper technical identifiers in their original language when that is clearer
- do not force English artifact headers unless the user explicitly asks for English deliverables

## Shared Execution Contract

Every skill should use one execution mode only.

The workflow should stay simple for the user:

- one invocation
- one minimum 3-bullet first draft
- one role per round
- progressive artifact building across rounds

Do not require the user to choose between multiple modes before work can start.

Still required in every run:

- user-first draft
- explicit user decision or commitment
- at least one falsification or challenge point
- one agent-off check before declaring completion

Progressive artifact rule:

- do not jump from handshake directly to a full artifact set in the same response
- after the user provides the minimum seed, expand only into the next needed artifact step
- by skill completion, the full required artifact set should exist unless the user explicitly asks to stop early

## Continuation Boundary

In current Codex and similar chat-agent surfaces, a skill cannot be assumed to stay active across future turns unless it is invoked again.

Therefore each skill should make this boundary explicit:

- the agent should not pretend the skill remains locked across turns by itself
- if the user wants to continue in the same skill, the agent should accept a very short continuation phrase
- preferred continuation phrase:
  - "继续按 `skill-name` 执行下一轮"

The goal is not true persistent activation, but low-friction continuation.

## Round Lock

To reduce drift across turns, every skill should enforce a round lock at the start of each substantive response.

The response should begin by explicitly echoing:

- `active skill`
- `round role`
- `this round allows`
- `this round does not allow`

Round-lock rules:

- do this both after the initial handshake and on every later continuation round
- keep the round lock short and operational, not essay-like
- if the user continues with a skill phrase, restore the last valid skill context before doing new work
- if the user asks for something outside the current round lock, either finish the current round first or explicitly say the skill is switching

Preferred shape:

- `active skill: ...`
- `round role: ...`
- `this round allows: ...`
- `this round does not allow: ...`

## Shared Anti-Theater Checks

These checks exist to prevent the workflow from becoming ceremonial.

### Check 1: unsupported-claim marking

Any important statement must be marked as one of:

- observed
- inferred
- unknown
- hypothesis

### Check 2: forced alternative

At every major decision point, require at least one serious alternative, not a strawman.

### Check 3: falsification prompt

Require one answer to:

- what would make this current belief or choice wrong?

### Check 4: fresh output

The user must produce something that cannot be copied from the agent wording:

- a fresh example
- a fresh explanation
- a fresh decision rationale
- a fresh testable contrast

### Check 5: evidence anchor minimum

For engineering and evidence-heavy research work, do not accept a polished choice without minimum anchors.

## Shared Minimum Templates

### Minimal problem seed

- suspected problem
- why I think it matters
- one thing I think current work gets wrong

### Minimal design seed

- problem I am trying to solve
- one candidate mechanism
- one reason I do not trust it yet

### Minimal engineering seed

- what I think the requirement asks for
- what part of the system might be affected
- what I do not understand yet

### Minimal knowledge seed

- what I think this concept means
- where it blocks me
- what confuses me most

## Shared Artifacts

- `problem-card.md`
- `design-card.md`
- `system-snapshot.md`
- `decision-record.md`
- `knowledge-closure-note.md`
- `transfer-check.md`

## Shared Validation Rule

No skill should be treated as stable until:

- the required artifacts can be produced from a realistic task
- the user can finish the agent-off check
- no critical workflow dimension scores 0 in the forward-test rubric

See the shared references and tests for concrete schemas and scoring.
