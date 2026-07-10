# Agent Collaboration Skill Blueprint

## Purpose

This document defines an executable collaboration system for four reusable skills:

1. `research-problem-formulation`
2. `research-method-design`
3. `engineering-task-decomposition`
4. `targeted-knowledge-closure`

The goal is dual:

- improve task completion speed with an agent
- preserve and grow the user's own problem-formulation, decision, and transfer ability

This is not a prompt pack. It is a workflow specification with explicit theory-backed constraints, required artifacts, completion gates, and implementation guidance for future skills.

## Design Position

The system is built on one core claim:

- the agent should expand, stress-test, and structure reasoning
- the human should retain first-pass modeling, final decisions, and independent reconstruction

This blueprint therefore treats skill design as a cognitive workflow design problem, not a text-generation problem.

## Engineering Readiness Standard

This blueprint is only acceptable if it can be executed repeatedly under real time pressure.

That means each future skill must provide:

- a low-friction entrypoint
- a minimum required input template
- a fixed artifact schema
- explicit stop rules
- evidence requirements where applicable
- a validation rubric

If a workflow depends on "good intentions" or "following the spirit", it is not ready.

## Theoretical Foundation

The workflow constraints below are grounded in a small set of repeatedly supported mechanisms.

### T1. Generation effect

People remember and can later use material better when they generate it themselves instead of only reading it.

- Implication for skills: require a user-first draft before agent synthesis.
- Use in this blueprint: all four skills begin with a mandatory user-produced initial representation.
- Source: Slamecka and Graf, 1978. "The generation effect: Delineation of a phenomenon." Journal of Experimental Psychology: Human Learning and Memory. Summary and citation: [Andy Matuschak notes](https://notes.andymatuschak.org/zWvCEwYz4Uv1dMHXynq3H5w)

### T2. Self-explanation effect

Having learners explain material to themselves improves understanding because they infer links and build a stronger mental model.

- Implication for skills: force the user to explain their current understanding, not just request an answer.
- Use in this blueprint: each skill requires a human-written rationale, interpretation, or restatement.
- Source: Chi, de Leeuw, Chiu, and LaVancher, 1994. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/0364021394900167)

### T3. Retrieval practice / testing effect

Actively retrieving knowledge strengthens long-term retention and often outperforms additional study or purely elaborative review.

- Implication for skills: do not start from agent explanation; start from recall, reconstruction, or attempted application.
- Use in this blueprint: the learning skill and all final completion checks require independent recall or reconstruction.
- Sources:
  - Roediger and Karpicke, 2006. [PubMed](https://pubmed.ncbi.nlm.nih.gov/16507066/)
  - Karpicke and Blunt, 2011. [Science](https://www.science.org/doi/10.1126/science.1199327)

### T4. Illusions of competence

Learners often feel they understand material when they are still relying on cues present during study.

- Implication for skills: a workflow is incomplete until the user performs a no-agent reconstruction or transfer check.
- Use in this blueprint: every skill has a mandatory "agent-off" completion test.
- Source: Koriat and Bjork, 2005. [PubMed](https://pubmed.ncbi.nlm.nih.gov/15755238/)

### T5. Problem-solution co-evolution

In open-ended design work, the problem and the solution evolve together rather than appearing fully formed in sequence.

- Implication for skills: research framing and engineering decomposition must support controlled backtracking instead of pretending the task is already well-specified.
- Use in this blueprint: `research-problem-formulation`, `research-method-design`, and `engineering-task-decomposition` are separate skills but explicitly linked by iteration gates.
- Source: Dorst and Cross, 2001. [Design Studies / ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0142694X01000096)

### T6. Cognitive apprenticeship

Complex cognitive work is learned through modeling, coaching, scaffolding, articulation, reflection, and fading rather than permanent delegation.

- Implication for skills: the agent should initially scaffold, then gradually retreat from authoring and deciding.
- Use in this blueprint: each skill defines an agent role, a user obligation, and a fading rule.
- Source: Collins, Brown, and Newman, 1989. Overview: [American Federation of Teachers](https://www.aft.org/ae/winter1991/collins_brown_holum)

### T7. Externalized decision rationale

Software and research work degrade when decisions are not recorded with their context, alternatives, and consequences.

- Implication for skills: every substantial branch point needs a short decision record.
- Use in this blueprint: research and engineering skills require explicit rejection reasons and next-step criteria.
- Source for engineering practice pattern: Martin Fowler on ADRs. [martinfowler.com](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)

### T8. Design discussion has real value, but needs to be made explicit

Empirical work on code review shows that design discussion occurs and matters, but it is uneven and easily underperformed if not structured.

- Implication for skills: the agent is better used as a constrained reviewer or challenger than as an unconstrained substitute designer.
- Use in this blueprint: engineering and method-design skills assign the agent a critique-first role.
- Source: El Zanaty et al., 2018. [ACM DOI page](https://dl.acm.org/doi/10.1145/3239235.3239525) and [PDF](https://rebels.cs.uwaterloo.ca/papers/esem2018_elzanaty.pdf)

### T9. Transfer is the real test of learning

Learning is valuable when it can be extended to new contexts, not only recalled in the original one.

- Implication for skills: the learning skill must end with a transfer or application check.
- Use in this blueprint: `targeted-knowledge-closure` always ends with a same-structure-different-surface task.
- Source: National Research Council, "How People Learn", Learning and Transfer chapter. [National Academies](https://www.nationalacademies.org/read/9853/chapter/6)

## Global Operating Rules

These rules apply to all four skills.

### Rule G1. User-first draft is mandatory

The skill must not start with "give me ideas" or "analyze this for me" unless the user genuinely has zero structure. Even then, the skill should first ask for a minimal seed:

- current guess
- current confusion
- current evidence

Why:

- supported by T1 and T3
- prevents passive consumption

Engineering constraint:

- each skill must define a `minimum viable first draft` with no more than 3 to 5 required fields
- if the user cannot provide more, the workflow still starts from that reduced template instead of failing

### Rule G2. Agent role must be single-purpose per round

In each round, the agent may be only one of the following:

- critic
- explainer
- organizer
- planner
- evaluator

The agent must not simultaneously author the core answer, decide the direction, and justify the decision.

Why:

- supported by T6 and T8
- reduces dependence and role leakage

### Rule G3. Decision rights stay with the user

The user must explicitly write:

- what is being chosen
- why it is chosen
- why alternatives are rejected
- what evidence would reverse the decision

Why:

- supported by T6 and T7
- preserves judgment rather than outsourcing it

### Rule G4. Every round leaves artifacts

Conversation alone is not enough. Each round must produce a named artifact such as:

- problem card
- design card
- system snapshot
- decision record
- knowledge check note

Why:

- supports reflection, transfer, and skill usability

Engineering constraint:

- artifact names and field order must be fixed
- each skill should be able to generate an empty artifact template automatically later

### Rule G5. Completion requires an agent-off check

A skill does not complete when the agent has produced a strong answer. It completes only when the user demonstrates one of:

- independent restatement
- independent design summary
- independent problem framing
- independent transfer/application

Why:

- supported by T4 and T9

Engineering constraint:

- distinguish `round stop` from `skill completion`
- a round may stop when the next action is clear
- the whole skill completes only after the agent-off check

### Rule G6. Fading is intentional

Each skill should support three modes:

- `guided`
- `review-driven`
- `spot-check`

The target is to move recurring workflows from `guided` to `review-driven`.

Why:

- supported by T6

Engineering constraint:

- default mode should be `guided`
- promotion to `review-driven` requires two successful runs with complete artifacts and a passed agent-off check

### Rule G7. Stop rules are mandatory

Each skill must define:

- when to stop the current round
- when to stop the current skill
- when to route to another skill

Why:

- open-ended workflows otherwise expand indefinitely
- time pressure will cause abandonment if the workflow does not converge

### Rule G8. Evidence beats elegance

Any engineering or code-facing claim must be tied to inspected evidence rather than a clean-sounding explanation.

Why:

- protects against plausible but detached system analysis
- aligns the workflow with actual repository and runtime truth

## Shared Artifact Types

Each skill will reuse a small set of artifact schemas.

### A1. Problem Card

- problem statement
- affected setting
- why important
- evidence already known
- current failure hypotheses
- open uncertainties
- next evidence to collect

### A2. Design Card

- objective
- constraints
- candidate mechanisms
- assumptions per mechanism
- failure modes
- validation plan
- chosen mechanism
- rejection reasons

### A3. System Snapshot

- user / stakeholder
- current workflow
- current system boundary
- known constraints
- unknowns blocking progress
- observed risks
- first verification actions

### A4. Decision Record

- decision
- context
- alternatives considered
- reasons
- consequences
- reversal triggers

### A5. Knowledge Closure Note

- my current understanding
- what I am unsure about
- corrected model
- one example
- one transfer case
- independent restatement

## Shared Minimum Templates

These are the maximum-friction-reduction entry templates. Every future skill should accept them.

### M1. Minimal Problem Seed

- suspected problem
- why I think it matters
- one thing I think current work gets wrong

### M2. Minimal Design Seed

- problem I am trying to solve
- one candidate mechanism
- one reason I do not trust it yet

### M3. Minimal Engineering Seed

- what I think the requirement asks for
- what part of the system might be affected
- what I do not understand yet

### M4. Minimal Knowledge Seed

- what I think this concept means
- where it blocks me
- what confuses me most

## Shared Artifact Schemas

These schemas should be copied into future `references/artifact-schemas.md` files and later turned into templates or scripts.

### S1. `problem-card.md`

```md
# Problem Card

## Current problem statement
## Target setting
## Why it matters
## Known evidence
## Failure hypotheses
## Open uncertainties
## Next evidence to collect
## Current owner decision
```

### S2. `design-card.md`

```md
# Design Card

## Objective
## Constraints
## Candidate mechanisms
## Assumptions per mechanism
## Failure modes
## Validation plan
## Chosen mechanism
## Rejection reasons
```

### S3. `system-snapshot.md`

```md
# System Snapshot

## Requirement as currently understood
## Suspected subsystem boundary
## Current workflow or runtime path
## Known constraints
## Unknowns
## Evidence inspected
## Immediate risks
## Next verification action
```

### S4. `decision-record.md`

```md
# Decision Record

## Decision
## Context
## Alternatives considered
## Why chosen
## Why others were rejected
## Consequences
## Reversal triggers
```

### S5. `knowledge-closure-note.md`

```md
# Knowledge Closure Note

## My current model
## What is wrong or missing
## Corrected model
## Task-local meaning
## Near transfer case
## Far transfer case
## Independent restatement
```

## Shared Stop Rules

These defaults apply unless a future skill overrides them with a stricter version.

### SR1. Round stop rule

Stop the current round when all three are true:

- the next action is singular and concrete
- the current artifact has no unresolved placeholder in required fields
- no new top-level uncertainty was introduced

### SR2. Skill stop rule

Stop the current skill when:

- the required artifacts exist
- the user has written the decision record
- the next workflow step belongs to a different skill or execution phase

### SR3. Escalation rule

Escalate or switch skills when:

- a specific knowledge gap blocks progress -> use `targeted-knowledge-closure`
- a method assumption invalidates the problem framing -> return to `research-problem-formulation`
- an engineering unknown cannot be resolved without repository/runtime evidence -> pause planning and gather evidence

## Shared Forward-Test Rubric

Every skill should be graded on a 0 to 2 scale for each dimension.

- `Entry friction`
  - 0: user needed substantial coaching before starting
  - 1: user could start with help
  - 2: user could start from the minimum template directly
- `Role discipline`
  - 0: agent mixed authoring, deciding, and reviewing
  - 1: one minor role leak
  - 2: role stayed clean
- `Artifact completeness`
  - 0: missing required artifacts
  - 1: artifacts exist but fields are partially empty
  - 2: all required fields completed
- `Evidence grounding`
  - 0: claims detached from evidence
  - 1: some evidence cited, some unsupported claims remain
  - 2: critical claims tied to concrete evidence
- `Decision ownership`
  - 0: the agent effectively made the decision
  - 1: shared decision but weak user rationale
  - 2: user rationale and rejection reasons are explicit
- `Transfer`
  - 0: user failed the agent-off check
  - 1: partial pass
  - 2: clear independent pass

Suggested acceptance rule:

- no dimension may score 0
- total score should be at least 9/12 for provisional acceptance
- total score should be at least 11/12 for promotion to `review-driven`

## Skill 1: `research-problem-formulation`

### Goal

Turn a vague or partly specified research intuition into a defendable problem definition with evidence, boundaries, and a failure taxonomy.

### When to use

Use when:

- there is a suspected research gap but the problem is still fuzzy
- the importance claim is not yet sharp
- related work exists but its limitations are not organized
- the user needs to decide whether a research direction is real before designing a method

### Non-goals

- inventing a final method
- drafting paper prose
- producing a literature dump with no synthesis

### Theory mapping

- T1: user writes the first problem card
- T2: user must explain why the problem matters and what likely fails
- T5: allow iterative reframing between problem statement and observed evidence
- T6: agent acts as structured challenger, not originator
- T7: explicit record of what counts as evidence and what would falsify the current framing

### Input contract

The user must provide a first-pass problem card, even if incomplete, with at least:

- suspected problem
- target setting
- why it might matter
- at least two hypotheses about why existing work fails or is incomplete

Low-friction entry:

- accept `M1. Minimal Problem Seed`
- if only the seed is available, the first round must expand it into `problem-card.md`

### Agent role by round

Round 1:

- role: organizer
- job: normalize the user draft into a problem card

Round 2:

- role: critic
- job: identify missing assumptions, counterexamples, and weak importance claims

Round 3:

- role: evidence planner
- job: propose the minimum evidence needed to disambiguate the top hypotheses

The agent must not directly jump to "here is the method."

### Required artifacts

- `problem-card.md`
- `failure-taxonomy.md`
- `evidence-gap-list.md`
- `decision-record-problem-scope.md`

Artifact contract:

- `problem-card.md` must follow `S1`
- `decision-record-problem-scope.md` must follow `S4`

### Execution protocol

1. User writes a rough problem card.
2. Agent restructures it and marks ambiguity.
3. User revises the problem statement and selects the top hypotheses.
4. Agent groups prior work into a small number of strategy buckets.
5. Agent explains why each bucket may fail under the stated setting.
6. User records confidence for each failure claim: low, medium, or high.
7. Agent proposes the minimum next evidence collection plan.
8. User decides whether to continue problem framing or hand off to method design.

Evidence contract:

- every claimed related-work failure must be tagged as one of:
  - direct paper evidence
  - inferred from paper behavior
  - hypothesis needing validation
- unsupported failure claims cannot be promoted to the final problem definition

Stop rules:

- stop the current round when the top 1 to 3 failure hypotheses are stable and the next evidence action is clear
- stop the skill when the user can state the problem, why prior buckets fail, and what evidence would overturn the framing
- if more than 2 full reframing loops occur with no narrowing of hypotheses, force a scope cut

### Completion test

The skill is complete only if the user can independently write, without agent help:

- a 5 to 10 sentence problem statement
- the top 3 related-work buckets
- why those buckets are insufficient in the target setting
- what evidence would most likely prove the problem framing wrong

### Failure modes to guard against

- generic "this is important" language with no setting
- listing papers without extracting failure structure
- skipping evidence quality labels
- moving to method design before the problem is stable enough

## Skill 2: `research-method-design`

### Goal

Convert a reasonably stable research problem into a mechanism-level design space, select a candidate design, and define minimal validating experiments.

### When to use

Use when:

- the problem is already reasonably defined
- the importance and setting are understood
- the missing piece is method or mechanism design
- the user wants to avoid letting the agent invent an ungrounded "fancy method"

### Non-goals

- final paper writing
- exhaustive experiment execution
- unconstrained novelty generation

### Theory mapping

- T1: user writes an initial design card with candidate mechanisms
- T2: user explains why the preferred mechanism might work
- T5: allow limited backtracking to problem framing if design assumptions reveal framing flaws
- T6: agent coaches by critique and experiment planning
- T7: design choice and rejections must be recorded
- Popper-style severe testing: a good method must expose itself to informative failure, not only cherry-picked confirmation

### Input contract

The user must provide:

- current problem statement
- target constraint set
- at least one candidate mechanism
- at least one reason it may fail

Low-friction entry:

- accept `M2. Minimal Design Seed`
- if only the seed is available, the first round must expand it into `design-card.md`

### Agent role by round

Round 1:

- role: mechanism challenger
- job: enumerate hidden assumptions and likely failure modes

Round 2:

- role: design-space organizer
- job: separate candidate designs by mechanism, not by naming or framing rhetoric

Round 3:

- role: validation planner
- job: design low-cost, high-signal experiments and ablations

The agent must not declare a winner by itself.

### Required artifacts

- `design-card.md`
- `mechanism-comparison.md`
- `failure-mode-table.md`
- `minimal-validation-plan.md`
- `decision-record-method-choice.md`

Artifact contract:

- `design-card.md` must follow `S2`
- `decision-record-method-choice.md` must follow `S4`

### Execution protocol

1. User writes the initial design card.
2. Agent converts vague method ideas into explicit mechanisms and assumptions.
3. Agent lists failure modes and confounders for each mechanism.
4. User chooses which mechanism candidates remain live.
5. Agent proposes the smallest experiment set that would separate the top candidates.
6. User writes why the chosen path is favored and what result would overturn it.
7. If a core assumption collapses, route back to `research-problem-formulation`.

Stop rules:

- keep at most 3 live mechanisms after round 2
- if two rounds of critique do not reduce the mechanism set, force ranking by expected information gain
- stop the skill when one chosen mechanism, one rejected alternative set, and one minimal validation plan are recorded

### Completion test

The skill is complete only if the user can independently explain:

- the selected mechanism
- why it should work in this setting
- what the main failure modes are
- which experiment best tests the design
- what evidence would make them abandon or revise it

### Failure modes to guard against

- method naming without mechanism clarity
- novelty theater with no falsifiable distinction
- ablations that confirm only superficial behavior
- unbounded design branching with no recorded rejection logic

## Skill 3: `engineering-task-decomposition`

### Goal

Turn an unclear engineering request into a grounded understanding of the current system, the unknowns, the realistic solution options, and an initial execution path that the user can defend.

### When to use

Use when:

- a requirement arrives but the user does not yet understand the system or demand
- the current state is unclear
- the agent would otherwise become the de facto engineer while the user becomes a relay

### Non-goals

- immediate implementation from a vague requirement
- replacing direct code or runtime inspection with speculation
- architecture theater without system evidence

### Theory mapping

- T1: user must first state their current understanding of the requirement and system
- T5: problem understanding and solution decomposition co-evolve
- T6: agent acts as reviewer, mapper, and risk scanner, not replacement owner
- T7: use short ADR-style records for choice points
- T8: structure design discussion explicitly because leaving it implicit leads to shallow review

### Input contract

The user must provide an initial system snapshot, even if partial:

- what the request appears to ask for
- which subsystem might be affected
- what they already know
- what they do not know

Low-friction entry:

- accept `M3. Minimal Engineering Seed`
- if only the seed is available, the first round must expand it into `system-snapshot.md`

### Agent role by round

Round 1:

- role: clarifier
- job: generate a targeted unknowns and verification list

Round 2:

- role: system mapper
- job: help partition the problem by boundary, data flow, or lifecycle

Round 3:

- role: design reviewer
- job: compare 2 to 3 implementation paths with tradeoffs and risks

The agent must not jump from vague demand to final plan without system inspection.

### Required artifacts

- `system-snapshot.md`
- `unknowns-checklist.md`
- `solution-options.md`
- `execution-slice-plan.md`
- `decision-record-engineering-path.md`

Artifact contract:

- `system-snapshot.md` must follow `S3`
- `decision-record-engineering-path.md` must follow `S4`

### Execution protocol

1. User writes the initial system snapshot.
2. Agent identifies missing facts and proposes a verification sequence.
3. User inspects the repo, logs, interfaces, or runtime and updates the snapshot.
4. Agent helps partition the task into system layers or workflow stages.
5. Agent proposes a small option set: simplest, balanced, and higher-complexity path.
6. User records the chosen path and rejection reasons.
7. Agent helps define the first implementation slice and validation checks.

Evidence contract:

- every important system claim must cite at least one concrete anchor:
  - file path
  - function or class name
  - config key
  - API endpoint or schema
  - log line or runtime observation
- the agent must distinguish:
  - observed
  - inferred
  - unknown
- no final option comparison is valid if the current system boundary is still unsupported by evidence

Stop rules:

- stop round 1 when the unknowns list is finite and prioritized
- stop round 2 when the task is partitioned into a stable boundary or lifecycle map
- stop the skill when one execution slice can be implemented or verified next without further planning
- if two planning rounds occur without new evidence anchors, force evidence collection before more solution discussion

### Completion test

The skill is complete only if the user can independently explain:

- what the requirement really means in system terms
- which boundaries and unknowns matter
- why the selected path is appropriate
- what the first verification or implementation slice is

### Failure modes to guard against

- treating requirements text as sufficient truth
- allowing the agent to substitute for system inspection
- producing one polished solution with no explicit alternatives
- choosing a path with no reversal criteria

## Skill 4: `targeted-knowledge-closure`

### Goal

Close a specific knowledge gap that blocks ongoing research or engineering work, while ensuring the user can later recall and transfer the knowledge independently.

### When to use

Use when:

- a concept, method, equation, system component, or paper idea blocks progress
- the user needs fast, scoped learning tied to a real task
- general explanations are less valuable than task-local understanding

### Non-goals

- open-ended tutorial generation
- encyclopedic survey when only one blocking gap matters
- passive reading without application

### Theory mapping

- T1: user first states their current model
- T2: user articulates confusion and later restates the corrected model
- T3: retrieval happens before explanation
- T4: finish with no-cue restatement
- T9: finish with transfer to a near and a far case

### Input contract

The user must provide:

- what they think the concept means
- where it appears in the current task
- what specifically is confusing

Low-friction entry:

- accept `M4. Minimal Knowledge Seed`
- if only the seed is available, the first round must expand it into `knowledge-closure-note.md`

### Agent role by round

Round 1:

- role: corrector
- job: identify errors, omissions, and misleading mental models

Round 2:

- role: explainer
- job: explain in three aligned forms:
  - intuitive
  - formal
  - task-local

Round 3:

- role: evaluator
- job: produce a transfer prompt and judge the user restatement

### Required artifacts

- `knowledge-closure-note.md`
- `transfer-check.md`

Artifact contract:

- `knowledge-closure-note.md` must follow `S5`

### Execution protocol

1. User writes their current understanding from memory.
2. Agent corrects it and highlights the smallest set of conceptual repairs.
3. Agent explains the concept in intuitive, formal, and task-local terms.
4. Agent gives one near transfer case and one far transfer case.
5. User independently restates the concept and solves one transfer case.
6. Agent evaluates only the gaps that remain.

Stop rules:

- stop the round when the conceptual repair set is small and explicit
- stop the skill when the user passes one near transfer and one independent restatement
- if the concept fans out into multiple unrelated gaps, split and keep only one closure target per run

### Completion test

The skill is complete only if the user can, without looking at the agent's explanation:

- explain the concept in their own words
- show where it matters in the current task
- solve or analyze one transfer case

### Failure modes to guard against

- reading explanations before recall
- asking the agent for a polished tutorial instead of a repair
- stopping at recognition rather than transfer

## Cross-Skill Routing Rules

The four skills are separate but tightly connected.

- Use `research-problem-formulation` before `research-method-design` when the problem is not yet stable.
- Route from `research-method-design` back to `research-problem-formulation` when a design assumption reveals a framing error.
- Invoke `targeted-knowledge-closure` inside any of the other three skills when the user cannot continue because of a specific gap.
- Invoke `targeted-knowledge-closure` as an embedded sub-loop, not as a full workflow reset, unless the knowledge gap changes the top-level task definition.
- Use `engineering-task-decomposition` whenever the user would otherwise ask the agent to "just analyze the requirement and tell me what to do."

Embedded sub-loop rule:

- the parent skill keeps ownership of the main artifact
- the learning sub-loop creates only `knowledge-closure-note.md` and `transfer-check.md`
- after closure, return immediately to the parent artifact and continue

## Completion Standard for the Whole System

This skill family is working only if it improves both throughput and retained capability.

Track these outcomes:

- `Speed`: time from task start to the first defensible plan
- `Artifact quality`: whether the required artifacts are actually produced
- `Decision ownership`: whether rejection reasons and reversal criteria are written by the user
- `Transfer`: whether the user can later restate the framing, design, or knowledge without the agent

Operational logging recommendation:

- add a short `run-summary.md` for each forward test with:
  - skill name
  - task
  - mode
  - rubric score
  - failure pattern
  - revision needed

If a workflow is fast but the user cannot later reconstruct it, the system failed the growth objective.

## Recommended Skill Package Layout

Each new skill should follow the existing repo style and stay lean:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── theory-map.md
│   ├── artifact-schemas.md
│   └── examples.md
└── scripts/
    └── optional artifact helper scripts
```

Recommended shared reference material:

- `references/theory-map.md`
- `references/artifact-schemas.md`
- `references/failure-patterns.md`
- `references/example-transcripts.md`

Keep `SKILL.md` short. Put deeper theory detail and templates into `references/`.

Recommended reference split:

- `references/theory-map.md`
- `references/artifact-schemas.md`
- `references/stop-rules.md`
- `references/forward-test-rubric.md`
- `references/examples.md`

## What Goes in Each Future `SKILL.md`

Each `SKILL.md` should contain only:

- frontmatter with name and description
- trigger conditions
- strict workflow steps
- allowed agent roles
- mandatory artifacts
- completion test
- routing rules to other skills

Each `SKILL.md` should also include:

- minimum viable first draft
- artifact contract
- stop rules

Do not put full theory summaries in the main body unless they are needed for execution. Put supporting theory in `references/theory-map.md`.

## Strict Execution Checklist

This is the operational checklist the user or agent should follow when running any future skill.

1. Identify which of the four skills is primary.
2. Create the first mandatory artifact from the user's memory or current understanding.
3. Freeze the agent to a single role for the round.
4. Produce the round artifact update.
5. Force a user decision record at branch points.
6. Trigger `targeted-knowledge-closure` if a specific knowledge gap blocks progress.
7. End with an agent-off completion test.
8. Save the artifacts for later review and skill iteration.

9. If the skill is engineering-facing, verify that all important claims are tagged as observed, inferred, or unknown.
10. Score the run with the forward-test rubric if this is a validation or pilot run.

## Implementation Plan

Build the skills in this order:

1. `targeted-knowledge-closure`
   - simplest and reusable inside all other skills
2. `engineering-task-decomposition`
   - directly useful and easier to validate on concrete tasks
3. `research-problem-formulation`
   - more open-ended, benefits from the shared artifact schemas
4. `research-method-design`
   - depends on problem-formulation artifacts and decision discipline

For each skill:

1. create the skill skeleton
2. write a lean `SKILL.md`
3. add `references/theory-map.md`
4. add `references/artifact-schemas.md`
5. add `references/stop-rules.md`
6. add `references/forward-test-rubric.md`
7. add 2 to 3 good and bad examples
8. validate the skill
9. forward-test it on a real task
10. revise based on failure cases

## Forward-Testing Plan

Test each skill on at least one real task with these questions:

- Did the user produce the first artifact before the agent expanded it?
- Did the agent stay inside one role per round?
- Was a real decision record produced?
- Did the workflow expose, rather than hide, uncertainty?
- Could the user pass the final agent-off check?
- Did the workflow stop at the right time instead of continuing to elaborate?
- For engineering runs, were critical claims tied to file, config, API, or runtime evidence?

Reject or revise any skill that succeeds only when the agent silently does the user's framing or decision work.

## Final Standard

The target behavior of this skill family is not:

- "the agent gives strong answers"

The target behavior is:

- the agent accelerates search, critique, and structure
- the user retains first-pass modeling, decisions, and transfer
- the workflow leaves reusable artifacts
- repeated use gradually reduces the amount of scaffolding needed

If those four properties are not true, the skill system should be treated as unfinished.
