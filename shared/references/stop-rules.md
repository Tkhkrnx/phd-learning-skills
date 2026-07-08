# Shared Stop Rules

## Round stop rule

Stop the current round when:

- the next action is singular and concrete
- required artifact fields are filled
- no new top-level uncertainty was introduced

In `light mode`, allow one compact working note instead of the full artifact set, but do not skip:

- one explicit next action
- one explicit user commitment
- one falsification or challenge point

## Skill stop rule

Stop the skill when:

- required artifacts exist
- the user has written the decision record when applicable
- the next workflow step belongs to another skill or execution phase
- the user passes the required agent-off check

Do not declare completion if the output only restates the agent wording without fresh user reasoning.

## Escalation rule

- use `targeted-knowledge-closure` when a specific knowledge gap blocks progress
- return to `research-problem-formulation` if a design assumption invalidates the problem framing
- pause engineering planning and gather evidence if key system claims still lack anchors

## Anti-theater rule

Pause the workflow and downgrade confidence if any of these occur:

- the user cannot name an alternative
- the user cannot state what would make the current choice wrong
- the user cannot generate a fresh example or rationale
- the artifacts contain polished claims with no support tags
