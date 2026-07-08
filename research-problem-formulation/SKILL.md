---
name: research-problem-formulation
description: Turn a vague or partly specified research intuition into a defendable problem definition with evidence, related-work buckets, and failure hypotheses. Use when the problem is still fuzzy, the importance claim is not sharp enough, or the user needs to determine whether a research direction is real before investing in method design.
---

# Research Problem Formulation

Use this skill to sharpen a fuzzy research problem before designing a method.

## Execution Contract

This skill uses one execution mode only.

The user should not need to choose a mode before starting.

Required progression:

- start from the 3-bullet minimum seed
- expand into only the next needed artifact step
- keep building evidence and decisions across rounds
- by skill completion, produce:
  - `problem-card.md`
  - `failure-taxonomy.md`
  - `evidence-gap-list.md`
  - `decision-record-problem-scope.md`
  - one explicit contrast statement against an existing line of work

## Minimum Viable First Draft

Ask the user for this minimum seed if they have not already provided it:

- suspected problem
- why I think it matters
- one thing I think current work gets wrong

Expand that seed into `problem-card.md`.

## Invocation Handshake

If the user only says something like "Use `research-problem-formulation` and help me define the problem", do not expect them to know the template.

Reply by asking only for:

- the problem they currently suspect
- why they think it matters
- one thing they think current work gets wrong

If they are still unsure, offer this fallback:

- "Give me one rough problem guess, one reason it may matter, and one dissatisfaction with existing work."

If they want to continue the same skill in a later turn, accept this short continuation phrase:

- "继续按 `research-problem-formulation` 执行下一轮"

At the start of every substantive response, echo a round lock:

- `active skill: research-problem-formulation`
- `round role: organizer` or `critic` or `evidence-planner`
- `this round allows: ...`
- `this round does not allow: ...`

## Agent Role Discipline

Keep one role per round:

1. `organizer`
2. `critic`
3. `evidence-planner`

Do not jump straight to inventing a method.

## Workflow

1. Expand the seed into a problem card.
2. Identify ambiguity, missing assumptions, and weak importance claims.
3. Group related work into a small number of strategy buckets.
4. Separate direct evidence, inference, and unvalidated hypotheses.
5. Build a failure taxonomy for the target setting.
6. Ask the user to rank or trim the live hypotheses.
7. Test whether the direction should be sharpened, parked, or abandoned.
8. End with the smallest next evidence plan that would narrow the framing.

Round-lock guidance:

- in the handshake round, `this round allows` should be limited to collecting the 3-bullet seed
- after the handshake, the first working round should allow only one compact framing note, not the full artifact set
- in `critic` rounds, allow hypothesis trimming and contrast testing, but do not allow unconstrained method invention
- in `evidence-planner` rounds, allow only the next evidence actions and gap closure priorities

## Artifact Contract

Create or update:

- `problem-card.md`
- `failure-taxonomy.md`
- `evidence-gap-list.md`
- `decision-record-problem-scope.md`

Follow the schema in `references/artifact-schemas.md`.

Artifact language rule:

- in Chinese-first usage, write artifact titles, section headers, and analysis in Chinese by default
- keep paper titles, system names, APIs, and other precise technical identifiers in English when that is clearer

Round-1 minimum output after the handshake:

- one compact framing note that records:
  - current framing
  - top failure hypotheses
  - one paper anchor per stable bucket if already available
  - next evidence step
  - user scope decision

## Evidence Contract

Every failure claim about current work must be tagged as one of:

- direct paper evidence
- inferred from reported behavior
- hypothesis needing validation

Do not promote unsupported claims into the final problem definition.
Do not treat a related-work bucket as stable until it contains at least one concrete paper anchor.
Require at least one explicit contrast statement:

- if existing line X already handles Y in setting Z, this framing should be weakened, narrowed, or abandoned

## Stop Rules

- Stop the round when the top 1 to 3 failure hypotheses are stable and the next evidence action is clear.
- Stop the skill when the user can state the problem, why prior buckets fail, and what evidence would overturn the framing.
- Stop the skill early and park the direction if no differentiated failure claim survives evidence review.
- If two full reframing loops occur without narrowing the hypothesis set, force a scope cut.
- Pause and mark the run incomplete if the user cannot give a concrete contrast statement against an existing line of work.

## Completion Test

The skill is complete only if the user can independently write:

- a concise problem statement
- the top related-work buckets
- why they are insufficient in the target setting
- what evidence would likely overturn the framing

## Failure Patterns

- vague importance language
- forcing a research problem when the direction should be parked
- literature listing without synthesis
- method invention before problem stabilization
- unsupported failure claims

## References

- Use `references/theory-map.md` for rationale.
- Use `references/artifact-schemas.md` for required artifacts.
- Use `references/stop-rules.md` for execution boundaries.
- Use `references/examples.md` for good and bad runs.
