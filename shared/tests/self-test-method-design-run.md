# Self-Test: Research Method Design

## Task

Simulated user request:

"I want to reduce burst-induced tail latency instability in long-context serving. One candidate mechanism is adaptive admission plus state-aware request shaping. I do not trust it because it may only shift latency and hurt throughput."

## Step 1: Minimum input

```md
- problem I am trying to solve: reduce burst-induced tail latency instability in long-context serving
- one candidate mechanism: adaptive admission plus state-aware request shaping
- one reason I do not trust it yet: it may only shift latency and hurt throughput
```

## Step 2: Workflow artifacts

### `design-card.md`

```md
# Design Card

## Objective
Reduce burst-induced tail instability without collapsing useful throughput.

## Constraints
- serving overhead must stay moderate
- throughput should not degrade excessively
- mechanism must react under burst conditions

## Candidate mechanisms
- adaptive admission plus state-aware shaping
- burst-triggered queue isolation
- predictive burst throttling

## Assumptions per mechanism
- shaping can observe useful state
- queue isolation does not starve normal traffic
- predictive throttling can anticipate bursts accurately enough

## Failure modes
- latency is only redistributed
- throughput drops too much
- control policy becomes unstable

## Validation plan
Compare tail latency, throughput, and stability across burst regimes.

## Chosen mechanism
Adaptive admission plus state-aware shaping

## Rejection reasons
- queue isolation may overcomplicate the first prototype
- predictive throttling depends on stronger forecasting assumptions
```

### `mechanism-comparison.md`

```md
# Mechanism Comparison

- candidate A: direct and testable
- candidate B: stronger isolation but higher complexity
- candidate C: potentially powerful but assumption-heavy
```

### `failure-mode-table.md`

```md
# Failure Mode Table

1. shifted latency rather than reduced instability
2. throughput collapse
3. policy oscillation
```

### `minimal-validation-plan.md`

```md
# Minimal Validation Plan

1. baseline under burst workload
2. candidate A under the same workload
3. compare tail latency, throughput, and queue stability
4. add one ablation removing state-aware shaping
```

### `decision-record-method-choice.md`

```md
# Decision Record

## Decision
Start with adaptive admission plus state-aware shaping.

## Context
Need the smallest mechanism with interpretable failure modes.

## Alternatives considered
- queue isolation
- predictive throttling

## Why chosen
It is easier to test with fewer speculative assumptions.

## Why others were rejected
- queue isolation is more complex
- predictive throttling relies on stronger forecasting assumptions

## Consequences
The first experiment should test whether the mechanism truly reduces instability rather than shifting it.

## Reversal triggers
If throughput degradation dominates or tail instability remains, revisit candidate B.
```

## Rubric

- Entry friction: 2
- Role discipline: 2
- Artifact completeness: 2
- Evidence grounding: 1
- Decision ownership: 2
- Transfer: 2

## Total

11/12

## Problems found

- The current workflow does not explicitly force a baseline comparison field inside the design artifact.
- That makes it easier to drift into mechanism discussion without enough experiment contrast.

## Callback conclusion

Add an explicit baseline or reference comparison requirement to the design skill.
