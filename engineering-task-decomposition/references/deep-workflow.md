# Deep engineering-decomposition workflow

Use this reference for ambiguous requirements, cross-module changes, migrations, concurrency/state changes, or a formal execution handoff.

## Requirement contract

Recover the stakeholder and operational outcome, acceptance authority, must/should/optional behavior, non-functional constraints, non-goals, failure policy, compatibility needs, and delivery budget. Treat requested artifacts as possible means rather than success itself.

## Architecture slice

Inspect only the path relevant to the requirement:

- entrypoint and public interface;
- data/control flow;
- state ownership and transitions;
- concurrency and error boundaries;
- configuration and feature gates;
- observability, tests, migration, and rollback.

Separate current facts from assumptions and proposed architecture. Do not require a full repository map when a narrow slice is enough.

## Options

Compare up to three credible paths when the choice is consequential. Include the smallest path and evaluate relevant trade-offs such as performance, coupling, maintainability, testability, operability, rollback, and delivery cost. Reject pattern-heavy redesign that does not improve the requirement.

## First slice

Define the smallest reversible implementation that proves a meaningful part of the requirement. State what it changes, what it deliberately leaves unchanged, how to observe success, and what result triggers rollback or redesign.

Choose validation by risk:

```text
smoke -> targeted tests -> regression -> full acceptance
```

State which layer was run and what stronger claim it cannot support. Reuse unchanged environment evidence instead of repeating full acceptance for every small item.

## Handoff and execution

Summarize the frozen requirement, attachment boundary, chosen path, rejected alternative, first slice, validation, rollback, and remaining risk. If implementation is authorized, proceed directly through edit, run, inspection, repair, and revalidation. Ask only when a missing user decision would materially change the result or when a side effect needs new authority.
