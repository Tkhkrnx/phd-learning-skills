# Self-Test: Research Problem Formulation

## Task

Simulated user request:

"I suspect long-context serving systems look good on average but fail under bursty enterprise workloads. I think this matters because deployments care about tail behavior and stability. I think current work gets one thing wrong: it benchmarks with smooth synthetic distributions."

## Step 1: Minimum input

```md
- suspected problem: long-context serving systems fail under bursty enterprise workloads
- why I think it matters: deployments care about tail behavior and stability
- one thing I think current work gets wrong: they benchmark with smooth synthetic distributions
```

## Step 2: Workflow artifacts

### `problem-card.md`

```md
# Problem Card

## Current problem statement
Current long-context serving evaluations may overstate robustness because they do not model bursty workload behavior that stresses latency and stability.

## Target setting
Enterprise or production-like long-context serving with bursty arrivals and tail-sensitive service objectives.

## Why it matters
Average throughput or mean latency can hide deployment failure modes driven by queue buildup and tail instability.

## Known evidence
- Many papers emphasize average metrics.
- Synthetic benchmarks often use smooth workload assumptions.

## Failure hypotheses
- Existing schedulers are tuned for average-case behavior.
- Evaluation traces underrepresent burstiness.
- State pressure compounds tail failures under bursts.

## Open uncertainties
- How often published evaluations use realistic burst traces
- Whether some recent work already addresses this setting

## Next evidence to collect
- Survey recent serving papers for workload assumptions
- Compare benchmark trace shapes
- Check whether any studies report burst-driven tail regressions

## Current owner decision
Keep the problem framing focused on workload realism plus tail instability, not on all long-context failures.
```

### `failure-taxonomy.md`

```md
# Failure Taxonomy

1. Evaluation mismatch
2. Scheduler average-case bias
3. State-pressure amplification
```

### `evidence-gap-list.md`

```md
# Evidence Gap List

- direct paper evidence still needed for benchmark assumptions
- direct paper evidence still needed for reported burst behavior
- current state-pressure hypothesis remains partly inferential
```

### `decision-record-problem-scope.md`

```md
# Decision Record

## Decision
Focus on burst-sensitive long-context serving evaluation gaps.

## Context
The initial framing was too broad.

## Alternatives considered
- all long-context performance failures
- scheduler design in general
- burst-sensitive evaluation mismatch

## Why chosen
It is narrower, testable, and better aligned with the claimed importance.

## Why others were rejected
- too broad
- too solution-oriented too early

## Consequences
The next step is evidence collection, not method invention.

## Reversal triggers
If recent work already covers burst-sensitive evaluation rigorously, this framing should be revised.
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

- The workflow can still tolerate weak evidence too long.
- It needs a stronger requirement that every related-work bucket should contain at least one named paper anchor before the framing is considered stable.

## Callback conclusion

Add a hard rule: stable related-work buckets require at least one concrete paper anchor per bucket.
