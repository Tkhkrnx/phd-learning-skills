---
name: targeted-knowledge-closure
description: Close one specific knowledge gap that is blocking current research or engineering work. Use when the user partly understands a concept, method, equation, or system idea but needs a fast, scoped workflow that starts from recall, repairs the mental model, checks transfer, and preserves independent restatement instead of passive dependence.
---

# Targeted Knowledge Closure

Use this skill to repair one blocking knowledge gap while preserving independent recall and transfer.

## Execution Contract

This skill uses one execution mode only.

The user should not need to choose a mode before starting.

Required progression:

- start from the 3-bullet minimum seed
- expand into only the next needed artifact step
- keep the closure target narrow
- by skill completion, produce:
  - `knowledge-closure-note.md`
  - `transfer-check.md`
  - one retained corrected formulation
  - one near transfer result
  - one far transfer result or one explicit reason to defer it

## Minimum Viable First Draft

Ask the user for this minimum seed if they have not already provided it:

- what I think this concept means
- where it blocks me
- what confuses me most

Expand that seed into `knowledge-closure-note.md`.
If the requested concept is too broad, force scope reduction to exactly one of:

- one mechanism
- one theorem or formula
- one system component
- one contrast pair between two concepts

## Invocation Handshake

If the user only says something like "Use `targeted-knowledge-closure` for this concept", do not expect them to know the template.

Reply by asking only for:

- what they currently think the concept means
- where it is blocking them
- what is most confusing

If they are still unsure, offer this fallback:

- "Write one sentence for each of the three bullets, even if you are guessing."

If they want to continue the same skill in a later turn, accept this short continuation phrase:

- "继续按 `targeted-knowledge-closure` 执行下一轮"

At the start of every substantive response, echo a round lock:

- `active skill: targeted-knowledge-closure`
- `round role: corrector` or `explainer` or `evaluator`
- `this round allows: ...`
- `this round does not allow: ...`

## Agent Role Discipline

Keep one role per round:

1. `corrector`
2. `explainer`
3. `evaluator`

Do not mix correction, long tutorial writing, and evaluation into one undifferentiated response.

## Workflow

1. Start from the user's recalled explanation, not from your own explanation.
2. Identify the smallest set of conceptual repairs needed.
3. Explain the concept in three aligned forms:
   - intuitive
   - formal
   - task-local
4. Give one near transfer case and one far transfer case.
5. Ask the user to choose one corrected formulation to keep and one immediate context in which they will apply it.
6. Ask for an independent user restatement or application.
7. Evaluate only the remaining gaps.

Round-lock guidance:

- in the handshake round, `this round allows` should be limited to collecting the 3-bullet seed
- after the handshake, the first working round should allow only one compact closure note, not the full artifact set
- in `corrector` rounds, allow only correction of the user's current model, not broad tutorial expansion
- in `evaluator` rounds, allow only gap checking and transfer checking, not a fresh long explanation

## Artifact Contract

Create or update:

- `knowledge-closure-note.md`
- `transfer-check.md`

The final note must include:

- one corrected formulation the user explicitly keeps
- one immediate application context chosen by the user

Follow the schema in `references/artifact-schemas.md`.

Artifact language rule:

- in Chinese-first usage, write artifact titles, section headers, and analysis in Chinese by default
- keep paper titles, system names, formulas, APIs, and other precise technical identifiers in English when that is clearer

Round-1 minimum output after the handshake:

- one compact note that records:
  - current model
  - corrected model
  - one retained formulation
  - one immediate application context
  - one fresh user-generated example

## Stop Rules

- Stop the round when the repair set is small and explicit.
- Stop the skill when the user passes one independent restatement and one near transfer check.
- If multiple unrelated knowledge gaps appear, split them and keep only one closure target in the current run.
- Pause and mark the run incomplete if the user can only paraphrase the agent wording without a fresh example.

## Completion Test

The skill is complete only if the user can, without looking at your explanation:

- explain the concept in their own words
- connect it to the current task
- solve or analyze one transfer case
- generate one fresh example or application that was not supplied by the agent

## Failure Patterns

- explaining before recall
- trying to close an entire field-sized topic in one run
- giving a broad tutorial instead of a scoped repair
- accepting recognition without transfer

## References

- Use `references/theory-map.md` for the learning rationale.
- Use `references/artifact-schemas.md` for required artifacts.
- Use `references/stop-rules.md` for execution boundaries.
- Use `references/examples.md` for good and bad runs.
