---
name: research-method-design
description: Turn a reasonably stable research problem into explicit mechanism candidates, assumptions, failure modes, and a minimal validation plan. Use when the problem is already mostly defined but the missing step is a defensible method design rather than unconstrained brainstorming.
---

# Research Method Design

Use this skill to turn a stable research problem into a defensible design space and validation plan.

## Minimum Viable First Draft

Ask the user for this minimum seed if they have not already provided it:

- problem I am trying to solve
- one candidate mechanism
- one reason I do not trust it yet

Expand that seed into `design-card.md`.

## Agent Role Discipline

Keep one role per round:

1. `mechanism-challenger`
2. `design-space-organizer`
3. `validation-planner`

Do not let the agent declare the winner by itself.

## Workflow

1. Expand the seed into a design card.
2. Rewrite vague ideas as explicit mechanisms and assumptions.
3. List likely failure modes and confounders.
4. Keep only a small live mechanism set.
5. Require at least one simpler or more standard comparison mechanism.
6. Ask the user to select or rank the surviving candidates.
7. Define the baseline or reference comparison that the first validation must beat or explain against.
8. Define one kill criterion that would make the chosen mechanism non-viable.
9. Produce the smallest experiment set that can separate the top candidates.
10. End with one chosen mechanism, rejection reasons, and a minimal validation plan.

## Artifact Contract

Create or update:

- `design-card.md`
- `mechanism-comparison.md`
- `failure-mode-table.md`
- `minimal-validation-plan.md`
- `decision-record-method-choice.md`

The validation plan must include:

- one explicit baseline or reference comparison
- one explicit kill criterion for the chosen mechanism

Follow the schema in `references/artifact-schemas.md`.

## Stop Rules

- Keep at most 3 live mechanisms after the critique phase.
- If two rounds of critique do not reduce the mechanism set, force ranking by expected information gain.
- Stop the skill when one chosen mechanism, one rejected alternative set, and one minimal validation plan are recorded.
- If a core assumption collapses, return to `research-problem-formulation`.

## Completion Test

The skill is complete only if the user can independently explain:

- the selected mechanism
- why it should work in this setting
- the main failure modes
- the best validating experiment
- what evidence would make them revise or abandon it

## Failure Patterns

- naming a method without mechanism clarity
- using the skill to justify a favorite mechanism without a fair simpler comparison
- novelty theater
- weak or decorative ablations
- failure to record why alternatives were dropped

## References

- Use `references/theory-map.md` for rationale.
- Use `references/artifact-schemas.md` for required artifacts.
- Use `references/stop-rules.md` for execution boundaries.
- Use `references/examples.md` for good and bad runs.
