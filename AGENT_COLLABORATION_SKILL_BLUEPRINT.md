# Agent Collaboration Skill Blueprint

## Purpose

This document defines the design contract for four expert-facing collaboration skills:

1. `research-problem-formulation`
2. `research-method-design`
3. `engineering-task-decomposition`
4. `targeted-knowledge-closure`

They are not generic prompt templates. They are expert-role workflows whose goals are dual:

- solve the current research, engineering, or learning task
- grow the user's own judgment and transfer ability

## Design Position

These skills should not force the user to pre-structure a task they do not yet understand.

Instead:

- the user gives the most natural starting point
- the agent takes the corresponding expert role
- the agent builds the initial scaffold
- the user progressively takes back the key judgments

The four skills are intentionally not symmetric. They solve different task types and therefore use different expert roles, different round structures, and different completion tests.

## Shared Rules

Every skill in this family must satisfy all of the following:

1. The user can start with a natural entrypoint rather than a full template.
2. The agent must act as the relevant expert, not as a generic writing assistant.
3. The first working round must reduce uncertainty, not generate large artifact sets.
4. The skill must keep the main value in the conversation and keep artifacts lightweight.
5. The agent must progressively expose its reasoning structure so the user can learn the work itself.
6. The skill is incomplete until the user can independently restate or defend the current conclusion at the relevant level.

## Expert-Role Mapping

Each skill requires a different expert role:

- `research-problem-formulation`
  - domain expert in LLM inference systems and adjacent systems literature
- `research-method-design`
  - systems-method and experiment-design expert
- `engineering-task-decomposition`
  - staff-level engineer or architect with codebase diagnosis habits
- `targeted-knowledge-closure`
  - subject-matter teacher who also uses effective instructional scaffolding

Do not flatten these into one general workflow. The user explicitly wants the agent to behave like the right kind of expert in each skill.

## Theoretical Foundation

The design is grounded in theory, but the theories are not used identically across skills.

### Shared cognitive and instructional theories

#### T1. Cognitive apprenticeship

Experts should model, scaffold, coach, then gradually fade support instead of permanently taking over.

- Why it matters here:
  - the user wants to become able to do the work, not just receive outputs
- Use:
  - all four skills must expose expert moves and gradually hand back judgment
- Source:
  - Collins, Brown, and Newman, 1989

#### T2. Scaffolding

Support should be matched to what the learner can currently do, then withdrawn as competence increases.

- Why it matters here:
  - the user often starts from uncertainty and cannot reasonably pre-structure the task
- Use:
  - do not require three structured bullets when the user does not yet understand the task
- Source:
  - Wood, Bruner, and Ross, 1976

#### T3. Cognitive load theory

When a task is unfamiliar, forcing early structure generation can overload working memory and reduce learning quality.

- Why it matters here:
  - the user explicitly reported that the old workflow was hard to use because too much structure was demanded too early
- Use:
  - the agent should absorb more early structuring load in engineering and knowledge-closure runs
- Source:
  - Sweller, 1988 and later CLT literature

#### T4. Retrieval practice and generation effect

Independent recall and self-generation improve later retention and transfer, but only after a workable mental representation exists.

- Why it matters here:
  - the user does want growth, but not premature "perform without scaffolding"
- Use:
  - require independent restatement later in the run, not before the user has a usable model
- Sources:
  - Slamecka and Graf, 1978
  - Roediger and Karpicke, 2006

#### T5. Worked example effect

When the domain is unfamiliar, a good worked example often teaches more effectively than forcing immediate unguided production.

- Why it matters here:
  - the user reported that knowledge-closure worked better once terms were translated and explained concretely
- Use:
  - the learning skill should start from a small, concrete explanatory scaffold
- Source:
  - Sweller and Cooper, 1985

### Research and design theories

#### T6. Hypothetico-deductive reasoning

Research problem framing improves by iterating between candidate explanations, evidence, and attempts at refutation.

- Use:
  - `research-problem-formulation`
- Source:
  - standard philosophy-of-science and scientific-method literature

#### T7. Falsification and contrastive comparison

A strong research problem is clarified not only by what it explains, but by what nearby work already explains and what evidence would overturn the current framing.

- Use:
  - `research-problem-formulation`
  - `research-method-design`
- Source:
  - Popperian falsification logic and contrastive explanation traditions

#### T8. Mechanism-based explanation

A method claim is stronger when it states the mechanism, assumptions, and failure conditions, not just the surface design.

- Use:
  - `research-method-design`
- Source:
  - mechanism explanation traditions across systems and scientific modeling

#### T9. Design of experiments

Validation should target the key causal claim first, rather than dispersing effort across decorative experiments.

- Use:
  - `research-method-design`
- Source:
  - DOE and systems experimentation best practices

### Engineering theories

#### T10. Situated cognition

Real engineering understanding is inseparable from the actual code, logs, interfaces, and runtime behavior.

- Use:
  - `engineering-task-decomposition`
- Source:
  - situated cognition literature

#### T11. Evidence-based diagnosis

Good engineering diagnosis depends on anchoring claims to inspected evidence instead of detached planning.

- Use:
  - `engineering-task-decomposition`
- Source:
  - debugging, diagnosis, and software maintenance practice literature

#### T12. Trade-off analysis

An implementation plan is not "best" unless it considers performance, maintainability, coupling, observability, failure recovery, and delivery cost together.

- Use:
  - `engineering-task-decomposition`
  - `research-method-design`

## Conversation-First, Artifact-Light

The old failure mode was over-artifacting the interaction.

New rule:

- the main value must stay in the live conversation
- artifacts should be concise working notes, not the user's main coordination burden
- if an artifact exists, it must help either:
  - the next round
  - later recall
  - eventual paper or implementation handoff

## Round Lock

To reduce drift across turns, every substantive response should begin by echoing:

- `active skill`
- `expert role`
- `this round does`
- `this round does not`

If the user only says:

- `继续按 <skill-name> 执行下一轮。`

the skill should restore its current context and choose the next expert-role move automatically.

## Completion Standard

Every skill must satisfy both:

- task progress:
  - the current task is now more executable or more sharply understood
- user growth:
  - the user can now independently defend, explain, or apply the key conclusion at the right level

If only one of these is satisfied, the skill is not done.
