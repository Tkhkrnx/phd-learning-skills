# Four Skill Usage Flows

This document gives a concrete usage flow for each of the four skills. Each section explains what the user should provide first, what role the agent should play, what the user must still own, and what counts as completion.

## 1. `targeted-knowledge-closure`

### When to use it

- A specific concept is blocking current research or engineering work.
- You need a fast repair, not a broad tutorial.
- You want to learn without becoming dependent on passive explanation.

### What the user provides first

Minimum input:

- what I think this concept means
- where it blocks me
- what confuses me most

### How the agent should help

Round 1: `corrector`

- identify errors, omissions, and confusions

Round 2: `explainer`

- give an intuitive explanation
- give a formal explanation
- give a task-local explanation

Round 3: `evaluator`

- provide one near transfer case
- provide one far transfer case
- check the user's independent restatement

### What the user must still own

- produce the first explanation from memory
- choose one corrected formulation to keep
- choose one immediate context in which to apply it
- restate the concept independently

### What counts as complete

All must be true:

- the user can restate the concept without looking
- the user can explain why it matters in the current task
- the user can pass one near transfer check

## 2. `engineering-task-decomposition`

### When to use it

- A requirement arrives but the current system state is unclear.
- You do not know whether to inspect code, APIs, config, or logs first.
- You want to avoid letting the agent become the de facto engineer.

### What the user provides first

Minimum input:

- what I think the requirement asks for
- what part of the system might be affected
- what I do not understand yet

### How the agent should help

Round 1: `clarifier`

- build an unknowns checklist
- build a verification order

Round 2: `system-mapper`

- organize the boundary
- partition the task by layer or lifecycle

Round 3: `design-reviewer`

- compare 2 to 3 options using inspected evidence
- highlight risk and validation priority

### What the user must still own

- inspect real evidence: code, interfaces, config, logs, runtime
- tag claims as observed, inferred, or unknown
- write the decision record
- choose the first execution slice

### Special rules

- do not write the final option comparison before at least 3 real evidence anchors exist
- if two rounds add no new evidence anchors, stop and gather evidence

### What counts as complete

All must be true:

- the user can explain the system boundary independently
- the user can justify the chosen path
- the user knows the first minimal execution slice

## 3. `research-problem-formulation`

### When to use it

- There is a research intuition, but the problem is still fuzzy.
- The importance claim is weak or too broad.
- Related work exists, but its insufficiency is not yet structured.

### What the user provides first

Minimum input:

- suspected problem
- why I think it matters
- one thing I think current work gets wrong

### How the agent should help

Round 1: `organizer`

- expand the seed into `problem-card.md`

Round 2: `critic`

- find ambiguity
- find hidden assumptions
- find weak importance arguments

Round 3: `evidence-planner`

- propose the smallest evidence plan that sharpens the framing

### What the user must still own

- narrow the scope
- decide which failure hypotheses remain live
- write the problem-scope decision record

### Special rules

- each related-work bucket must contain at least one concrete paper anchor before it is treated as stable
- do not jump to method design while the framing is unstable
- if the hypothesis set does not narrow after two reframing loops, cut scope

### What counts as complete

All must be true:

- the user can independently write a concise problem statement
- the user can name the top related-work buckets
- the user can explain why they are insufficient in the target setting
- the user knows the next evidence to collect

## 4. `research-method-design`

### When to use it

- The research problem is already mostly clear.
- The current bottleneck is mechanism design, option comparison, or validation planning.

### What the user provides first

Minimum input:

- problem I am trying to solve
- one candidate mechanism
- one reason I do not trust it yet

### How the agent should help

Round 1: `mechanism-challenger`

- expose hidden assumptions
- identify likely failure modes

Round 2: `design-space-organizer`

- organize mechanism candidates
- reduce the live mechanism set

Round 3: `validation-planner`

- define the smallest validation plan
- define the baseline or reference comparison

### What the user must still own

- choose the mechanism
- write rejection reasons
- decide what the first experiment must actually validate

### Special rules

- keep at most 3 live mechanisms after critique
- the validation plan must include an explicit baseline or reference comparison
- if a core assumption collapses, route back to `research-problem-formulation`

### What counts as complete

All must be true:

- the user can explain the chosen mechanism independently
- the user can explain why it may work
- the user knows the main failure modes
- the user knows the first minimal validation experiment
