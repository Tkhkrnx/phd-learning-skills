---
name: engineering-task-decomposition
description: Turn an unclear engineering request into an evidence-grounded understanding of the system boundary, unknowns, solution options, and first execution slice. Use when a requirement arrives but the current system state is unclear, the user does not yet know what to do, and the workflow must avoid replacing direct repository or runtime inspection with plausible but detached planning.
---

# Engineering Task Decomposition

Use this skill to ground an unclear engineering request in evidence before choosing a path.

## Minimum Viable First Draft

Ask the user for this minimum seed if they have not already provided it:

- what I think the requirement asks for
- what part of the system might be affected
- what I do not understand yet

Expand that seed into `system-snapshot.md`.

## Agent Role Discipline

Keep one role per round:

1. `clarifier`
2. `system-mapper`
3. `design-reviewer`

Do not jump from an unclear request to a polished final plan.

## Workflow

1. Normalize the seed into a system snapshot.
2. Produce a finite unknowns and verification list.
3. Require repository, interface, config, log, or runtime evidence before comparing final options.
4. Partition the task by system boundary, data flow, or lifecycle.
5. Compare a small option set:
   - simplest
   - balanced
   - higher-complexity
6. Require the user to record the chosen path and rejected alternatives.
7. End with one concrete execution or verification slice.

## Artifact Contract

Create or update:

- `system-snapshot.md`
- `unknowns-checklist.md`
- `solution-options.md`
- `execution-slice-plan.md`
- `decision-record-engineering-path.md`

Follow the schema in `references/artifact-schemas.md`.

## Evidence Contract

Every important system claim must cite at least one anchor:

- file path
- function or class name
- config key
- API endpoint or schema
- log line
- runtime observation

Tag claims as:

- observed
- inferred
- unknown

Do not finalize option comparison while the current system boundary is still unsupported by evidence.

## Stop Rules

- Stop round 1 when the unknowns list is finite and prioritized.
- Stop round 2 when the task is partitioned into a stable boundary or lifecycle map.
- Stop the skill when one execution slice can be implemented or verified next without further planning.
- If two planning rounds occur without new evidence anchors, force evidence collection before more discussion.

## Completion Test

The skill is complete only if the user can independently explain:

- what the requirement means in system terms
- which boundaries and unknowns matter
- why the selected path is appropriate
- what the first execution or verification slice is

## Failure Patterns

- treating the requirement text as sufficient truth
- substituting the agent for repository inspection
- producing one elegant plan with no explicit alternatives
- making unsupported system claims

## References

- Use `references/theory-map.md` for rationale.
- Use `references/artifact-schemas.md` for required artifacts.
- Use `references/stop-rules.md` for execution boundaries.
- Use `references/examples.md` for good and bad runs.
