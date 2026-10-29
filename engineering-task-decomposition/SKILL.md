---
name: engineering-task-decomposition
description: Clarify, implement, debug, or accept a codebase change through verified slices when the user explicitly invokes this Skill.
---

# Engineering Task Decomposition

Recover the real requirement and the relevant architecture slice, then work in analysis, implementation, debugging, or acceptance mode according to the user's request. Do not turn a simple change into an interview or a mandatory PRD.

## Core workflow

1. Inspect the relevant code, configuration, interfaces, tests, and available runtime evidence.
2. Restate the stakeholder outcome, acceptance evidence, non-goals, constraints, and failure policy.
3. Trace the smallest relevant data/control flow, state ownership, and dependency boundary.
4. Compare the smallest viable path with at least one credible alternative when the choice is consequential.
5. Define a reversible first slice, proportionate validation, observability, rollback, and stop conditions.
6. When implementation is authorized, complete a small end-to-end slice before expanding; compare observed acceptance evidence with the requirement and repair failures before proceeding.

## Collaboration contract

Lead with inspected code and an expert model of the requirement and architecture. Ask a focused question when the user's goal, non-goal, priority, or acceptance authority could change the path; elicit correction or rationale rather than yes/no approval. Do not ask the user to locate facts the agent can inspect. Do not finish a consequential requirement or architecture decision as an agent-only monologue, but treat the user's already detailed constraints or live correction as valid participation rather than forcing another round.

## Load on demand

- Read [deep decomposition workflow](references/deep-workflow.md) for ambiguous requirements, cross-module architecture recovery, migrations, concurrency/state changes, or a formal execution handoff.
- Read [engineering execution](references/engineering-execution.md) for implementation, debugging, security, and acceptance; use the matching mode, not every checklist for every patch.
- Read [AOCI integration](references/aoci-integration.md) only when a project has AOCI configured or the user requests indexing. It is optional, not a global prerequisite.
- Read project architecture docs only for service or module boundaries, database docs only for schema/migration work, and deployment docs only for release changes.
- Use `targeted-knowledge-closure` only as a bounded dependency when one concept blocks the engineering decision.

## Boundaries

- Request prose is not architecture evidence; keep observed facts, assumptions, and proposed changes separate.
- Preserve public interfaces, state ownership, concurrency rules, error handling, compatibility, and rollback unless the request changes them.
- Distinguish smoke, targeted CI, regression, and full acceptance; one layer does not prove the next.
- If the user already authorized implementation and the path is clear, exit the collaboration protocol and execute instead of waiting for another approval.

## Completion

Finish when the requirement, relevant architecture boundary, chosen path, first reversible slice, validation evidence, rollback condition, and material residual risk are clear, and the user has had a real opportunity to correct the consequential interpretation. If implementation is in scope, complete the edit-run-inspect-fix-revalidate loop before ending.
