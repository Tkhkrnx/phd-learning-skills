---
name: engineering-task-decomposition
description: Turn an unclear engineering request into an evidence-grounded understanding of the system boundary, unknowns, solution options, and first execution slice. Use when a requirement arrives but the current system state is unclear, the user does not yet know what to do, and the workflow must avoid replacing direct repository or runtime inspection with plausible but detached planning.
---

# Engineering Task Decomposition

Use this skill to ground an unclear engineering request in evidence before choosing a path.

## Execution Mode

Use `light mode` for urgent triage.
Use `standard mode` when the decision will drive implementation, coordination, or architecture.

### `light mode` required user output

- the 3-bullet minimum seed
- one compact working note containing:
  - current boundary guess
  - prioritized unknowns
  - current evidence anchors
  - `null or reuse-first` option
  - first execution slice
  - one user path choice

### `standard mode` required user output

- `system-snapshot.md`
- `unknowns-checklist.md`
- `solution-options.md`
- `execution-slice-plan.md`
- `decision-record-engineering-path.md`
- `evidence-acquisition-plan.md` when direct evidence is not yet reachable

## Minimum Viable First Draft

Ask the user for this minimum seed if they have not already provided it:

- what I think the requirement asks for
- what part of the system might be affected
- what I do not understand yet

Expand that seed into `system-snapshot.md`.

## Invocation Handshake

If the user only says something like "Use `engineering-task-decomposition` for this task", do not expect them to know the template.

Reply by asking only for:

- what they think the requirement is asking for
- what system part may be affected
- what they do not understand yet

If they are still unsure, offer this fallback:

- "Give me one rough sentence for the requirement, one guess about the affected area, and one unknown."

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
   - null or reuse-first
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
- `evidence-acquisition-plan.md` when direct evidence is not yet reachable

Follow the schema in `references/artifact-schemas.md`.

Artifact language rule:

- in Chinese-first usage, write artifact titles, section headers, and analysis in Chinese by default
- keep repository paths, function names, config keys, APIs, and other precise technical identifiers in English when that is clearer

In `light mode`, the user may collapse:

- `system-snapshot.md`
- `unknowns-checklist.md`
- `execution-slice-plan.md`

into one compact working note, but must still preserve:

- current boundary guess
- unknowns
- evidence anchors
- first execution slice
- user decision

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
Require at least 3 concrete evidence anchors before writing the final option comparison.
If direct evidence is not yet reachable, stop solution discussion and produce `evidence-acquisition-plan.md`.

## Stop Rules

- Stop round 1 when the unknowns list is finite and prioritized.
- Stop round 2 when the task is partitioned into a stable boundary or lifecycle map.
- Stop the skill when one execution slice can be implemented or verified next without further planning.
- If two planning rounds occur without new evidence anchors, force evidence collection before more discussion.
- Pause and mark the run incomplete if the user cannot name a `null or reuse-first` alternative or cannot state what would falsify the current path.

## Completion Test

The skill is complete only if the user can independently explain:

- what the requirement means in system terms
- which boundaries and unknowns matter
- why the selected path is appropriate
- what the first execution or verification slice is

## Failure Patterns

- treating the requirement text as sufficient truth
- validating a favored architecture before checking whether reuse or no-change is enough
- substituting the agent for repository inspection
- producing one elegant plan with no explicit alternatives
- making unsupported system claims

## References

- Use `references/theory-map.md` for rationale.
- Use `references/artifact-schemas.md` for required artifacts.
- Use `references/stop-rules.md` for execution boundaries.
- Use `references/examples.md` for good and bad runs.
