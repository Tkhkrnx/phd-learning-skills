# Repository guidance

This repository is the canonical source for the user's personal research, writing, and note-workflow Skills.

## Read only what the task needs

- Use `README.md` or `README_zh.md` for the catalog and installation surface.
- Use `AGENT_COLLABORATION_SKILL_BLUEPRINT.md` only when changing the shared collaboration contract or its router/tests.
- Use `shared/expert-skill-references/research_evidence_acquisition.md` only for research evidence or literature-boundary changes.
- Use `shared/expert-skill-references/llm_inference_three_layer_framework.md` only for LLM inference/serving reasoning.
- Inspect a script's implementation when modifying or debugging it; running an established script does not require reading all of its source first.

## Editing rules

- Keep each Skill description short and limited to a discriminating trigger. Invocation policy belongs in `agents/openai.yaml`, not repeated prose.
- Keep simple Skills self-contained. For complex Skills, make `SKILL.md` a compact entrypoint and load references only when their route matches the task.
- Preserve evidence, privacy, path, overwrite, and external-side-effect boundaries. Remove generic model coaching, fixed turn counts, arbitrary confidence percentages, and mandatory status narration.
- Update tests and sync scripts when an instruction contract or packaged file set changes.

## Local execution

The repository tests use local fixtures and mocked network calls; they have no production mutation path. Run relevant validators and tests, fix failures caused by the requested change, and rerun them without asking for stepwise approval.

## Completion

A configuration change is complete only after the source files are updated, relevant validators/tests pass, the intended active roots are synchronized with matching hashes, and a final conflict scan finds no stale mandatory-read, broad-trigger, or legacy-model scaffolding introduced by the change.
