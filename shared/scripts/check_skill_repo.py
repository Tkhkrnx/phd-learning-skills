from __future__ import annotations

import sys
from pathlib import Path


SKILLS = [
    "targeted-knowledge-closure",
    "engineering-task-decomposition",
    "research-problem-formulation",
    "research-method-design",
]

REQUIRED_REPO_FILES = [
    "README.md",
    "AGENT_COLLABORATION_SKILL_BLUEPRINT.md",
    "shared/references/artifact-schemas.md",
    "shared/references/forward-test-rubric.md",
    "shared/references/stop-rules.md",
]

REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/theory-map.md",
    "references/artifact-schemas.md",
    "references/stop-rules.md",
    "references/examples.md",
]


def check_paths(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_REPO_FILES:
        if not (root / rel).exists():
            errors.append(f"missing repo file: {rel}")
    for skill in SKILLS:
        skill_root = root / skill
        if not skill_root.exists():
            errors.append(f"missing skill directory: {skill}")
            continue
        for rel in REQUIRED_SKILL_FILES:
            if not (skill_root / rel).exists():
                errors.append(f"missing skill file: {skill}/{rel}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    errors = check_paths(root)
    if errors:
        print("Repository check failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Repository check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
