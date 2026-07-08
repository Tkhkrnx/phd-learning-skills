# Stress-Test Audit

This audit probes where the current skills are likely to become fragile in real PhD usage.

## Test dimensions

1. vague input
2. overscoped input
3. strong user bias
4. missing evidence
5. false-problem scenarios
6. transfer failure after apparently good interaction

## Skill: `targeted-knowledge-closure`

### Stress case A: the concept is too broad

Example:

- "I do not understand reinforcement learning."

Observed fragility:

- the skill can still start, but the closure target is too broad to finish well
- the agent may produce a mini-tutorial instead of a scoped repair

Fix applied:

- the skill now forces scope reduction to one mechanism, theorem/formula, system component, or contrast pair

### Stress case B: the user only imitates understanding

Example:

- the user can paraphrase the agent wording but cannot produce a fresh example

Observed fragility:

- the previous completion test could pass too easily with surface restatement

Fix applied:

- the completion test now requires one fresh user-generated example or application

## Skill: `engineering-task-decomposition`

### Stress case A: no direct evidence is available yet

Example:

- the user only has a product requirement and no local code or runtime access yet

Observed fragility:

- the skill could stall because evidence was required, but no formal evidence-acquisition branch existed

Fix applied:

- the skill now requires `evidence-acquisition-plan.md` when direct evidence is not yet reachable

### Stress case B: the user already prefers one architecture

Example:

- "I think we should build a new microservice for export."

Observed fragility:

- the workflow could drift into validating the preferred option instead of checking whether the system even needs it

Fix applied:

- the option comparison must now include a `null or reuse-first` path

## Skill: `research-problem-formulation`

### Stress case A: there may not actually be a research problem

Example:

- the user has a trend impression but little differentiated contrast with existing work

Observed fragility:

- the workflow used to assume the framing should always be sharpened

Fix applied:

- the skill now explicitly allows a direction to be sharpened, parked, or abandoned
- it can stop early if no differentiated failure claim survives review

### Stress case B: importance inflation

Example:

- the user can state why a topic sounds important, but not why existing methods fail in a differentiated way

Observed fragility:

- the workflow could produce elegant problem prose with weak novelty substance

Fix applied:

- the skill now requires an explicit contrast statement against an existing line

## Skill: `research-method-design`

### Stress case A: the user is attached to a favorite mechanism

Example:

- the user strongly wants one mechanism to be the answer

Observed fragility:

- the skill could become a justification engine if alternatives were weak

Fix applied:

- the skill now requires at least one simpler or more standard comparison mechanism
- the skill now requires one kill criterion for the chosen mechanism

### Stress case B: baseline drift

Example:

- a method sounds novel, but the baseline is underspecified

Observed fragility:

- the validation plan could sound scientific without testing meaningful superiority

Fix applied:

- the validation plan now requires an explicit baseline or reference comparison

## Cross-skill fragility

### Case A: user fatigue from too many artifacts

Current risk:

- heavy artifact production may reduce adoption under time pressure

Mitigation status:

- partially mitigated by minimum viable first drafts
- not fully solved

### Case B: false sense of rigor

Current risk:

- structured artifacts may be mistaken for actual evidence or understanding

Mitigation status:

- mitigated by evidence tags, paper anchors, kill criteria, and agent-off checks
- still a residual risk if the user treats the workflow as ceremony

## Audit conclusion

The skill family is much stronger after this audit, but two residual risks remain:

1. artifact fatigue in very high-pressure tasks
2. users may still try to "perform the workflow" without genuine evidence or reflection

Those are not fatal flaws, but they should be watched in future real-use iterations.
