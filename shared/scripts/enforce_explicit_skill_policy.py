from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml


MANIFEST = Path(__file__).resolve().parents[2] / "explicit-skill-router" / "aliases.yaml"
EXTERNAL_DESCRIPTION_PREFIX = (
    "Explicit skill-use request only. Activate only when the user explicitly asks to use, call, "
    "or apply this skill or an unmistakable plain-language label to a stated task; the exact "
    "identifier is optional. Ordinary task matching is not authorization. "
)


def load_mapping(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def update_openai_metadata(path: Path, allow_implicit: bool, check: bool) -> bool:
    metadata = load_mapping(path) if path.is_file() else {}
    policy = metadata.get("policy")
    if not isinstance(policy, dict):
        policy = {}
        metadata["policy"] = policy
    changed = policy.get("allow_implicit_invocation") is not allow_implicit
    policy["allow_implicit_invocation"] = allow_implicit
    if changed and not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True, width=1000),
            encoding="utf-8",
        )
    return changed


def update_external_description(path: Path, check: bool) -> bool:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    metadata = yaml.safe_load(text[4:end])
    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: invalid YAML frontmatter")
    description = str(metadata.get("description", ""))
    changed = not description.startswith(EXTERNAL_DESCRIPTION_PREFIX)
    if changed and not check:
        metadata["description"] = EXTERNAL_DESCRIPTION_PREFIX + description
        frontmatter = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True, width=1000).rstrip()
        body = text[end + 5 :]
        path.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
    return changed


def process_root(root: Path, check: bool) -> tuple[list[str], list[str]]:
    manifest = load_mapping(MANIFEST)
    repository_skills = list(manifest.get("skills", {}))
    external_skills = list(manifest.get("external_skills", {}))
    explicit_commands = list(manifest.get("explicit_only_commands", []))
    required = repository_skills + ["explicit-skill-router"]
    missing = [name for name in required if not (root / name / "SKILL.md").is_file()]
    if missing:
        raise ValueError(f"{root}: missing required skills: {', '.join(missing)}")

    changed: list[str] = []
    protected = repository_skills + external_skills + explicit_commands
    for name in protected:
        skill_dir = root / name
        if not (skill_dir / "SKILL.md").is_file():
            continue
        if update_openai_metadata(skill_dir / "agents" / "openai.yaml", False, check):
            changed.append(f"{name}/agents/openai.yaml")
        if name in external_skills and update_external_description(skill_dir / "SKILL.md", check):
            changed.append(f"{name}/SKILL.md")

    router_dir = root / "explicit-skill-router"
    if update_openai_metadata(router_dir / "agents" / "openai.yaml", True, check):
        changed.append("explicit-skill-router/agents/openai.yaml")
    return changed, missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enforce explicit-only invocation for user-authored task skills."
    )
    parser.add_argument("--root", action="append", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    drift: list[str] = []
    try:
        for root in args.root:
            changed, _ = process_root(root.resolve(), args.check)
            if args.check and changed:
                drift.extend(f"{root}: {path}" for path in changed)
            mode = "checked" if args.check else "enforced"
            print(f"{mode}={root.resolve()} changed={len(changed)}")
    except Exception as exc:  # noqa: BLE001 - command-line validation boundary
        print(f"Explicit skill policy enforcement failed: {exc}", file=sys.stderr)
        return 1

    if drift:
        print("Explicit skill policy drift detected:", file=sys.stderr)
        for item in drift:
            print(f"- {item}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
