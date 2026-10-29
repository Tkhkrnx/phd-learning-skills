# Engineering execution

## Select the mode

- Analysis only: inspect current code and define outcome, non-goals, architecture slice, choices, and acceptance. Do not write implementation merely because this skill supports it.
- Implementation: follow authorized requirements through edit-run-inspect-fix-revalidate. Reuse supplied decisions instead of repeating interviews.
- Debugging: reproduce the smallest failure, locate the first bad state, compare a falsifiable cause with evidence, change the cause, and rerun the reproduction plus affected regressions. Do not stack speculative patches or blame the environment without checks.
- Acceptance: map each requirement to actual evidence and residual gaps. Passing a build is not proof of workflow or production acceptance.

## Before a consequential build

Recover user-visible goal and acceptance; current behavior and non-goals; relevant data/control/state boundaries; existing stack and constraints; implementation choices; first end-to-end slice; security and failure behavior; proportionate tests and recovery. For a new product, a concise spec and design sketch may help. For a local bug, the reproduction and a focused test may be enough. Do not manufacture nine separate documents.

Inspect the existing framework, UI language, interfaces, storage, and tests before choosing replacements. Record material architectural decisions near existing project documentation only when they will be reused. Inspect Git/dirty state and preserve unrelated work. Do not auto-commit, push, deploy, or create a remote issue as a substitute for delivery.

## During development

Prefer one demonstrable vertical slice: real input -> relevant state transition -> real output -> assertion/inspection. Set a small edit boundary and leave unrelated refactors out. Split by responsibility when it improves correctness or comprehension, not by arbitrary function length; do not add a one-use wrapper just to satisfy a checklist.

Validate untrusted input at its boundary. Reuse established invariants internally. Catch an error only to recover, translate an interface, or add actionable context; do not hide failures with success-shaped fallback values. Evaluate guards against concrete probability, impact, and complexity. Surface consequential compatibility, dependency, or maintenance tradeoffs before committing to them.

Keep secrets outside committed files. Check user/tenant authorization where data access crosses a boundary; avoid unsafe shell interpolation, sensitive logs, and unbounded external access. Test the boundary involved in this change, not an unrelated universal security program. Preserve permissions and production state unless separately authorized.

## Evidence and finish

For each affected acceptance condition, state input/scenario, observed behavior, and test or artifact location. Distinguish mocked unit tests, local integration, real provider/hardware runs, and production acceptance. Run/inspect the actual output when the requested workflow depends on it; fix failures caused by the patch, rerun, then inspect diff and remaining risk. Stop at an unavailable external dependency with the smallest concrete unblock, not a false claim of completion.

Adapted from the verified chapter themes of the Jiang Vibe Coding video (plan/basics/rules; small iterations, modularity, bounded permissions, security, evidence-led debugging), not a claimed verbatim transcription of its unverified nine-step narration: <https://www.douyin.com/video/7617880126232085627>.
