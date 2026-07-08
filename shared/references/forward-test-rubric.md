# Shared Forward-Test Rubric

Score each dimension from 0 to 2.

## Entry friction

- 0: user needed substantial coaching before starting
- 1: user could start with help
- 2: user could start from the minimum template directly

## Role discipline

- 0: agent mixed authoring, deciding, and reviewing
- 1: one minor role leak
- 2: role stayed clean

## Artifact completeness

- 0: missing required artifacts
- 1: artifacts exist but fields are partially empty
- 2: all required fields completed

## Evidence grounding

- 0: claims detached from evidence
- 1: some evidence cited, some unsupported claims remain
- 2: critical claims tied to concrete evidence

## Decision ownership

- 0: the agent effectively made the decision
- 1: shared decision but weak user rationale
- 2: user rationale and rejection reasons are explicit

## Transfer

- 0: user failed the agent-off check
- 1: partial pass
- 2: clear independent pass

## Adoption cost

- 0: the workflow is too heavy for realistic repeated use
- 1: usable, but with noticeable friction
- 2: sustainable under realistic task pressure

## Anti-theater robustness

- 0: the workflow can be completed with superficial artifact filling
- 1: some real thinking is required, but imitation can still slip through
- 2: the workflow forces fresh reasoning, alternatives, and falsification

## Acceptance rule

- no dimension may score 0
- total score should be at least 12/16 for provisional acceptance
- total score should be at least 14/16 for promotion to review-driven use
