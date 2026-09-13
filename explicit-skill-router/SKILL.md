---
name: explicit-skill-router
description: Route an explicit request to use a personal Skill; ignore ordinary task requests that do not ask for a Skill.
---

# Explicit Skill Router

This is the only implicitly discoverable entrypoint for the personal Skills listed in `aliases.yaml`. It decides authorization and target only; it does not perform domain work.

## Route

Load `aliases.yaml` when the current user explicitly asks to use, call, invoke, apply, or run a Skill/技能 for a stated task.

- Match an exact Skill name or an unambiguous plain-language label.
- If one target matches, load that target's root `SKILL.md` and apply it to the stated task.
- If two targets remain plausible, explain the short distinction and ask one routing question.
- If the user asks only for “a suitable Skill” without identifying a kind, ask which kind; do not infer it from task semantics.
- If an optional target is not installed, report that boundary instead of substituting another Skill.

Ordinary requests such as “analyze the requirement”, “find papers”, “explain this”, “review the paper”, “write code”, or “run experiments” are normal assistance even when a Skill could help. Topic similarity, complexity, prior use, and convenience are not authorization.

## Scope

The authorization covers follow-ups within the same stated collaboration. It expires when that work completes, the task changes, or the user pivots to direct execution. A new primary Skill requires a new explicit request.

An active primary Skill may load a supporting Skill without another user request only for a concrete dependency of the same goal. The supporting work must add no independent deliverable, external side effect, or broader permission; it returns its result to the primary Skill and then stops.

Do not use supporting work to change the primary research or engineering objective. Writing, coding, synchronization, debugging, experiment execution, publishing, and other delivery work are normal execution unless the user explicitly invokes another Skill.

Keep router paths, identifiers, and lifecycle mechanics internal unless the user asks for diagnostics.
