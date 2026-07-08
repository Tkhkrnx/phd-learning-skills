---
name: targeted-knowledge-closure
description: Close one specific knowledge gap that is blocking current research or engineering work. Use when the user partly understands a concept, method, equation, or system idea but needs a fast, scoped workflow that starts from recall, repairs the mental model, checks transfer, and preserves independent restatement instead of passive dependence.
---

# Targeted Knowledge Closure

Use this skill to repair one blocking knowledge gap while preserving independent recall and transfer.

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

## Artifact Contract

Create or update:

- `knowledge-closure-note.md`
- `transfer-check.md`

The final note must include:

- one corrected formulation the user explicitly keeps
- one immediate application context chosen by the user

Follow the schema in `references/artifact-schemas.md`.

## Stop Rules

- Stop the round when the repair set is small and explicit.
- Stop the skill when the user passes one independent restatement and one near transfer check.
- If multiple unrelated knowledge gaps appear, split them and keep only one closure target in the current run.

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
