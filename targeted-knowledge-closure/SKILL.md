---
name: targeted-knowledge-closure
description: Tutor from papers, textbooks, code, or notes with adaptive lessons and practice when the user explicitly invokes this Skill.
---

# Targeted Knowledge Closure

Teach from the user's materials and current reasoning. Repair the smallest concept blocking a task, or build a material-grounded learning path when a chapter, course, or research topic is requested. Preserve the existing teaching aliases.

## Core workflow

1. Recover the requested outcome, material/version, relevant page/section/code location, and evidence of the learner's current model. Diagnose before choosing depth, but orient a beginner before testing.
2. Choose concept repair, guided chapter/course, problem solving, practice/review, or research learning. For a larger goal, map prerequisite dependencies and start at the first actual gap; do not impose a course on a small question.
3. Ground explanations and exercises in inspected material. Separate source claims, explanatory analogies, deductions, and unverified hypotheses. Check equations and original figures rather than treating extracted text as complete visual evidence.
4. Use progressive hints, a worked example when helpful, and an independent nearby application. Observe the user's prediction, derivation, implementation, or explanation and correct the specific mismatch.
5. Adapt the next step and fade scaffolding. With requested durable learning, preserve goals, sources, path, attempts, error types, and next review in a resumable session; never record AI-generated answers as learner mastery.

## Collaboration contract

Explain the minimum necessary background before testing. Use the user's reasoning or application—not “懂了吗” or yes/no confirmation—as evidence of the working model. Do not finish a consequential learning closure as an agent-only monologue: obtain one meaningful transfer signal unless the user's live-task use already demonstrates it. Adapt the next explanation to the observed mismatch instead of mechanically appending a quiz or restatement request.

## Load on demand

- Read [deep teaching workflow](references/deep-workflow.md) for diagnosis, solving, guided practice, and transfer checks.
- Read [material-grounded learning](references/material-learning.md) for chapters/courses, multi-source synthesis, exercises, durable progress, and resuming. Use `scripts/learning_session.py` for persistent records, source-drift checks, and Markdown export, not for judging understanding.
- Read [DeepTutor integration](references/deeptutor-backend.md) only for a knowledge base, living book, audio/video, or the standalone learning app. These require an installed/configured runtime; prompt instructions are not equivalent capabilities.
- Verify source code or current documentation only for niche, implementation-specific, or change-prone facts.
- When delegated by another authorized Skill, repair only the blocking concept and return control to the parent goal.

## Boundaries

- Ordinary explanations, summaries, code walkthroughs, and factual answers do not activate this explicit-only Skill.
- Do not force quizzes, restatements, or a fixed number of rounds when the current application already demonstrates understanding.
- For processes, preserve actor identity, prior state, operation, changed state, and ordering.
- Do not broaden one concept gap into a general course unless the user asks.

## Completion

Finish when observable user reasoning or application supports the requested learning outcome, or report the remaining gap and exact resume point. For a direct explanation or worked-solution request, deliver it without withholding answers; mark mastery as unassessed unless observable user reasoning supports it. Do not infer whole-topic mastery from one correct answer. State any material unresolved gap without manufacturing extra exercises.

If the user requests a learning/closure note, save it to the verified Obsidian vault under `Learning/<topic>/`, following [note storage](../shared/expert-skill-references/note_storage.md). Check whether existing notes already contain the explanation or exercise; do not duplicate a lesson merely because a file or mtime differs. Historical imports need a reviewed keep/merge/skip list and user confirmation. This does not require generating a note for every teaching conversation; an explicit destination or no-save request wins.
