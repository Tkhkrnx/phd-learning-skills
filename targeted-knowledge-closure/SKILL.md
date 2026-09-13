---
name: targeted-knowledge-closure
description: Teach a specific concept to usable transfer when the user explicitly invokes this Skill.
---

# Targeted Knowledge Closure

Repair the smallest concept, prerequisite, or relation blocking the user's current work, then help them apply it accurately.

## Core workflow

1. Identify the target concept and the smallest missing prerequisite or misconception.
2. Choose the lightest useful representation: definition, intuitive model, actor-state-sequence trace, worked example, contrast, code, equation, or diagram.
3. Explain the decisive relation and map any analogy back to the real objects and its limits.
4. Observe the user's restatement, prediction, example, or live-task application; correct the specific mismatch without restarting the whole tutorial.
5. Fade scaffolding once the user can use the concept in the live task.

## Collaboration contract

Explain the minimum necessary background before testing. Use the user's reasoning or application—not “懂了吗” or yes/no confirmation—as evidence of the working model. Do not finish a consequential learning closure as an agent-only monologue: obtain one meaningful transfer signal unless the user's live-task use already demonstrates it. Adapt the next explanation to the observed mismatch instead of mechanically appending a quiz or restatement request.

## Load on demand

- Read [deep teaching workflow](references/deep-workflow.md) when confusion persists, several prerequisites interact, or the user requests guided practice and transfer checks.
- Verify source code or current documentation only for niche, implementation-specific, or change-prone facts.
- When delegated by another authorized Skill, repair only the blocking concept and return control to the parent goal.

## Boundaries

- Ordinary explanations, summaries, code walkthroughs, and factual answers do not activate this explicit-only Skill.
- Do not force quizzes, restatements, or a fixed number of rounds when the current application already demonstrates understanding.
- For processes, preserve actor identity, prior state, operation, changed state, and ordering.
- Do not broaden one concept gap into a general course unless the user asks.

## Completion

Finish when observable user reasoning or application shows a correct working model for the requested task, the user can distinguish the decisive near-miss when relevant, and no remaining misconception is likely to cause a wrong application. State any material unresolved gap without manufacturing extra exercises.
