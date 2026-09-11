# Collaboration validation — 2026-09-11

## Scope

Changed problem formulation, method design, engineering clarification, teaching, Finder and shared routing/collaboration instructions. Systems/HPC writing, notes and citation tools were excluded. Inputs were synthetic, with browsing and project mutations explicitly prohibited. These results do not validate real literature retrieval or scientific claims.

## Live model checks

Runtime: desktop-bundled Codex CLI 0.153.4, default configured gpt-6-astra. Each scenario used a new session followed by an actual resumed turn. Reviewer criteria were not supplied to the model; it was told to read repository skills and required references, not test files.

| Scenario | Session | Observed result |
|---|---|---|
| Problem definition, first turn | 01a08ecd-a977-7e51-85e0-88f6b910133f | Four requested sections; declarative unexplained waiting-distribution phenomenon; no invented wrong decision, performance gain or novelty; asks whether existing work already explains it. |
| Problem correction | same session | Incorporates B's aggregate-only coverage and deployment as an alternative explanation; preserves four sections and distinguishes a supplied-evidence gap from a field-wide novelty claim. |
| Method discussion, first turn | 01a08ece-5924-7b40-8b97-eda4d4292a80 | Derives two challenges from A/B failures, maps C/D principles, compares partial and combined approaches, discusses allocation/modification granularity and asks about the workload's write behavior. No forced third challenge or final solution claim. |
| Method correction | same session | Withdraws frequent-old-content modification assumption and full-copy candidate; compares tail separation with immutable sharing/private append; explains mapping, granularity, reclamation and read-path costs; asks a reasoned trade-off question. |

The initial attempt through PATH CLI 0.147.0 returned HTTP 400 requiring a newer CLI for the configured model; no model answer was produced. The installed desktop runtime was used without changing global configuration. This failed attempt is not a skill behavior result.

Observed core behaviors passed these two bounded scenarios. This is a small forward test, not a guarantee of compliance across models or long sessions. Engineering, teaching, standalone Finder retrieval, and cross-client model routing were not live-model tested in this run; their cases are retained in `collaboration_forward_cases.md` for subsequent evaluation. No claim that all fixture cases were executed.

## Structural and deployment checks

- Both existing policy/structure validators passed; these inspect files and fixture structure only.
- All 15 repository unit tests passed.
- Six changed skill entrypoints passed the system skill-creator structure validator.
- `sync_expert_skills.ps1 -ProtocolOnly` copied and hash-verified 17 scoped files in a scratch target, without creating excluded skill directories.

Raw generated replies are local-only under `work/collaboration-eval/` (ignored by Git). No private user-thread transcripts are included in this report.
