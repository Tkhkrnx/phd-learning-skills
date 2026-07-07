# Agent Collaboration Skill Blueprint

This repository-level blueprint defines the shared collaboration rules for all personal PhD learning skills.

## Shared Purpose

- accelerate research, engineering, and learning work with an agent
- keep first-pass modeling, decisions, and transfer with the user

## Shared Rules

1. Require a user-first draft.
2. Keep the agent in one role per round.
3. Require an explicit user decision record at branch points.
4. Use fixed artifact schemas.
5. Define stop rules for both round and skill completion.
6. Require an agent-off completion check.
7. Tie engineering claims to inspected evidence.

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
