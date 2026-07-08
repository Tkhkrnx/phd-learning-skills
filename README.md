# PhD Learning Skills

[中文说明 / Chinese README](./README_zh.md)

Personal Codex skill repository for research, engineering, and learning workflows during PhD work.

This repository is designed for personal long-term use rather than public marketplace polish. The core goal is:

- improve task throughput with an agent
- preserve and grow independent problem formulation, design judgment, and transfer ability

## Skill Set

- `targeted-knowledge-closure`
  - close one blocking knowledge gap with recall, correction, transfer, and independent restatement
- `engineering-task-decomposition`
  - turn an unclear engineering request into evidence-grounded boundaries, options, decisions, and a first execution slice
- `research-problem-formulation`
  - turn a vague research intuition into a defendable problem definition with evidence and failure hypotheses
- `research-method-design`
  - turn a stable research problem into mechanism candidates, failure modes, and a minimal validation plan

## Shared Design Rules

All skills in this repository follow the same operating rules:

- user-first draft before agent expansion
- one agent role per round
- explicit user decision records
- fixed artifact schemas
- explicit stop rules
- agent-off completion checks
- evidence-grounded engineering claims
- `light mode` for high-pressure use
- anti-theater checks for unsupported claims, weak alternatives, and fake understanding

See [AGENT_COLLABORATION_SKILL_BLUEPRINT.md](./AGENT_COLLABORATION_SKILL_BLUEPRINT.md) for the full design specification.

## How To Use The Skill Family

Run every task through the same high-level loop:

1. Choose the primary skill.
2. Write the minimum viable first draft yourself.
3. Freeze the agent to one role for the current round.
4. Produce or update the required artifact.
5. Write the user decision or commitment at branch points.
6. Insert `targeted-knowledge-closure` if a specific knowledge gap blocks progress.
7. End with an agent-off check.

## Invocation Style

You do not need to remember each input template before calling a skill.

Short invocations are enough, for example:

- "Use `research-problem-formulation` and help me define the problem."
- "Use `research-method-design` for this direction."
- "Use `engineering-task-decomposition` for this requirement."
- "Use `targeted-knowledge-closure` for this concept."

After invocation, the skill should guide you by asking only for the minimum 3-bullet input needed to start.

## Execution Modes

### `light mode`

Use when:

- time pressure is high
- the main goal is to preserve the minimum safeguards
- a full artifact set would reduce adoption

Still required:

- user-first draft
- explicit user decision or commitment
- one challenge or falsification point
- one agent-off check

Expected output:

- one compact working note
- no full artifact set unless the user wants durable records

### `standard mode`

Use when:

- the result will be reused, implemented, published, or taught
- the user wants durable records instead of fast triage

Required:

- full artifact set
- explicit evidence or contrast handling
- complete finish criteria

Expected output:

- the full artifact set for the chosen skill
- full decision, evidence, and completion records

## Skill Flows

## 1. `targeted-knowledge-closure`

### When to use it

- a specific concept blocks current research or engineering work
- you need a fast repair, not a broad tutorial

### What the user provides first

- what I think this concept means
- where it blocks me
- what confuses me most

If the user does not know how to begin, the skill should ask for one rough sentence per bullet.

`light mode` output:

- one compact note with corrected model, one retained formulation, one immediate use, and one fresh example

`standard mode` output:

- `knowledge-closure-note.md`
- `transfer-check.md`

If the concept is too broad, reduce it to exactly one of:

- one mechanism
- one theorem or formula
- one system component
- one contrast pair between two concepts

### Agent roles

1. `corrector`
2. `explainer`
3. `evaluator`

### User responsibilities

- explain from memory first
- choose one corrected formulation to keep
- choose one immediate application context
- restate the concept independently
- generate one fresh example or application

### Completion

Complete only if the user can:

- restate the concept without looking
- explain why it matters in the current task
- pass one near transfer check
- generate one fresh example not copied from the agent

## 2. `engineering-task-decomposition`

### When to use it

- a requirement arrives but the current system state is unclear
- you do not know whether to inspect code, APIs, config, logs, or runtime first

### What the user provides first

- what I think the requirement asks for
- what part of the system might be affected
- what I do not understand yet

If the user does not know how to begin, the skill should ask for one rough sentence per bullet.

`light mode` output:

- one compact working note with boundary guess, unknowns, evidence anchors, `null or reuse-first` option, first slice, and user path choice

`standard mode` output:

- `system-snapshot.md`
- `unknowns-checklist.md`
- `solution-options.md`
- `execution-slice-plan.md`
- `decision-record-engineering-path.md`
- `evidence-acquisition-plan.md` if needed

### Agent roles

1. `clarifier`
2. `system-mapper`
3. `design-reviewer`

### User responsibilities

- inspect real evidence: code, interfaces, config, logs, runtime
- tag claims as `observed`, `inferred`, or `unknown`
- write the decision record
- choose the first execution slice

### Special rules

- include a `null or reuse-first` option in comparison
- do not write the final option comparison before at least 3 real evidence anchors exist
- if direct evidence is not yet reachable, create `evidence-acquisition-plan.md`

### Completion

Complete only if the user can:

- explain the system boundary independently
- justify the chosen path
- name the first minimal execution slice

## 3. `research-problem-formulation`

### When to use it

- there is a research intuition, but the problem is still fuzzy
- the importance claim is weak or too broad
- related work exists, but its insufficiency is not yet structured

### What the user provides first

- suspected problem
- why I think it matters
- one thing I think current work gets wrong

If the user does not know how to begin, the skill should ask for one rough sentence per bullet.

`light mode` output:

- one compact framing note with problem guess, top failure hypotheses, one paper anchor per stable bucket, next evidence step, and one scope decision

`standard mode` output:

- `problem-card.md`
- `failure-taxonomy.md`
- `evidence-gap-list.md`
- `decision-record-problem-scope.md`
- one explicit contrast statement

### Agent roles

1. `organizer`
2. `critic`
3. `evidence-planner`

### User responsibilities

- narrow the scope
- decide which failure hypotheses remain live
- write the problem-scope decision record
- state one explicit contrast against an existing line of work

### Special rules

- each related-work bucket needs at least one concrete paper anchor before it is stable
- the direction may be sharpened, parked, or abandoned
- if no differentiated failure claim survives review, stop and park the direction

### Completion

Complete only if the user can:

- write a concise problem statement independently
- name the top related-work buckets
- explain why they are insufficient in the target setting
- name the next evidence to collect

## 4. `research-method-design`

### When to use it

- the research problem is already mostly clear
- the bottleneck is mechanism design, option comparison, or validation planning

### What the user provides first

- problem I am trying to solve
- one candidate mechanism
- one reason I do not trust it yet

If the user does not know how to begin, the skill should ask for one rough sentence per bullet.

`light mode` output:

- one compact design note with chosen mechanism guess, simpler comparison mechanism, baseline/reference, kill criterion, first experiment, and one rejection reason

`standard mode` output:

- `design-card.md`
- `mechanism-comparison.md`
- `failure-mode-table.md`
- `minimal-validation-plan.md`
- `decision-record-method-choice.md`

### Agent roles

1. `mechanism-challenger`
2. `design-space-organizer`
3. `validation-planner`

### User responsibilities

- choose the mechanism
- write rejection reasons
- decide what the first experiment must actually validate
- define what result would kill the chosen mechanism

### Special rules

- keep at most 3 live mechanisms after critique
- include at least one simpler or more standard comparison mechanism
- the validation plan must include an explicit baseline or reference comparison
- the validation plan must include a kill criterion

### Completion

Complete only if the user can:

- explain the chosen mechanism independently
- explain why it may work
- name the main failure modes
- name the first minimal validation experiment

## Validation and Audit

This repository treats skill quality as an engineering problem.

Each skill is checked for:

- low-friction entry
- artifact completeness
- evidence grounding
- decision ownership
- transfer
- adoption cost
- anti-theater robustness

Shared tests live under `shared/tests/`, including smooth self-tests and stress-test audits.

## Repository Layout

```text
phd-learning-skills/
├── AGENT_COLLABORATION_SKILL_BLUEPRINT.md
├── README.md
├── README_zh.md
├── shared/
│   ├── references/
│   ├── scripts/
│   └── tests/
├── targeted-knowledge-closure/
├── engineering-task-decomposition/
├── research-problem-formulation/
└── research-method-design/
```

## Notes

- This repo is meant to stay private unless intentionally cleaned for public release.
- The defaults are optimized for repeated personal use in Codex rather than broad discoverability.
- The shared references and tests are intentionally explicit so future revisions can be checked instead of guessed.
