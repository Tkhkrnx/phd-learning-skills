# Shared Stop Rules

## Round stop rule

Stop the current round when:

- the next action is singular and concrete
- required artifact fields are filled
- no new top-level uncertainty was introduced

## Skill stop rule

Stop the skill when:

- required artifacts exist
- the user has written the decision record when applicable
- the next workflow step belongs to another skill or execution phase
- the user passes the required agent-off check

## Escalation rule

- use `targeted-knowledge-closure` when a specific knowledge gap blocks progress
- return to `research-problem-formulation` if a design assumption invalidates the problem framing
- pause engineering planning and gather evidence if key system claims still lack anchors
