---
name: explicit-skill-router
description: "Route a user-authored primary skill only when the current user explicitly asks to use, call, invoke, or apply a skill/技能 for a stated task and identifies its kind by an exact name or recognizable plain-language label. This narrow router may match phrases such as '用研究方法的 skill' or '调用需求分析那个技能'. Never activate a top-level skill from ordinary task semantics such as asking to analyze a requirement, find a method, explain a concept, search papers, write, review, code, debug, or run experiments. Once authorized, the primary skill may invoke bounded supporting skills for the same goal, but a new primary role still requires an explicit request."
---

# Explicit Skill Router

This is the only implicitly discoverable entry point for the user-authored skills in this repository. Its job is authorization and routing, not domain work.

Read `aliases.yaml` completely before routing.

## Authorization Gate

Route a target skill only when all of these are true:

1. the user explicitly asks to use, call, invoke, apply, or run a skill/技能 in the current request;
2. the user identifies the kind of skill through its exact identifier or an unambiguous plain-language label;
3. the task to which the skill should apply is stated or unambiguously referenced.

The exact English identifier is never required. For example, “用研究方法的 skill 处理这个已定义的问题”, “调用问题定义那个技能判断这个想法”, and “用教学 skill 帮我学会条件概率” are authorized requests.

Ordinary intent is not authorization. “帮我找研究方法”, “分析一下需求”, “解释条件概率”, “查几篇论文”, “审一下文章”, or “继续跑实验” must use normal assistance even when a repository skill could help.

If the user says only “用个合适的 skill” without identifying its kind, do not infer the target from task semantics. Ask one concise question about which kind they intend to use.

## Scope and Expiry

Record the authorized target and task scope internally.

- The user does not need to repeat the skill request in every reply within the same interactive collaboration.
- Authorization expires immediately when that collaboration completes, the user changes tasks, or the user pivots to ordinary execution such as writing, coding, synchronization, debugging, experiment running, review, or delivery.
- A later task or resumption requires a new explicit skill-use request.
- Authorization for one primary skill does not authorize an unrelated task or a transition to a new primary expert role. That transition still requires the user to explicitly request the destination kind of skill.
- The authorized primary skill may invoke a necessary supporting skill for a bounded subtask inside the same authorized goal. This is supporting delegation, not a new top-level activation.
- If scope is uncertain, keep the narrower interpretation and ask one focused question rather than carrying the skill into unrelated work.

## Supporting Delegation

A primary skill may delegate without a second user request only when all of these conditions hold:

1. the supporting work is necessary or materially useful to the current authorized goal, not merely convenient;
2. the subtask is concrete and bounded, and does not introduce a new deliverable, objective, externally visible mutation, or permission requirement beyond the parent task;
3. the primary skill remains accountable for the user-facing collaboration and final judgment;
4. the supporting skill returns its evidence, explanation, or artifact to the primary skill instead of opening an independent lifecycle;
5. the delegation ends when the subtask finishes and inherits the primary authorization's expiry.

For example, an authorized `research-method-design` run may use `topic-paper-finder` to build its academic candidate pool, and an authorized engineering collaboration may use `targeted-knowledge-closure` to repair one blocking concept before returning to the engineering decision. The supporting skill may use its own internal checkpoints when the bounded subtask genuinely requires them, but the conversation must remain one coherent collaboration.

Do not use supporting delegation to smuggle in a new primary task. Moving from problem formulation to method design, from method design to implementation preparation, or from any collaboration to paper writing is a primary-role transition when it changes the user's objective; require an explicit request for that destination kind. Ordinary execution is not a supporting skill and still exits the collaboration protocol.

## Routing

1. Match the user's label against the repository and optional installed-skill sections in `aliases.yaml`. Prefer meaning over exact wording, but never infer a skill solely from the underlying task.
2. If exactly one target is clear, read `../<target>/SKILL.md` completely and follow it for the authorized task.
3. If two targets remain plausible, name the short distinction and ask which kind the user wants. Do not start either target.
4. If an optional installed target is absent from the current skill root, say it is unavailable here instead of substituting another skill.
5. Keep router mechanics, paths, lifecycle state, and target identifiers internal unless the user asks for diagnostics.

When an authorized primary skill identifies a supporting skill under the conditions above, read that supporting skill's `SKILL.md` completely and apply only the relevant bounded subworkflow. A supporting skill's top-level explicit-use boundary remains intact: delegated use is valid only because an already authorized primary skill owns the same task.

Files, scripts, references, search utilities, and supporting skills that an authorized skill uses under this rule are internal backends. They do not become a second primary skill or broaden the authorization scope.

## Failure Conditions

The route is invalid if it was inferred from topic similarity, task complexity, a prior task's authorization, the model's convenience, or a generic request to produce an artifact. A delegation is also invalid if it creates an independent goal, changes the primary expert role without a new explicit request, persists beyond the parent scope, or lets the supporting skill take over the user interaction. On detecting an invalid or expired route, stop applying the target skill silently and continue with normal assistance.
