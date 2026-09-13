from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml


MANIFEST = Path(__file__).resolve().parents[2] / "explicit-skill-router" / "aliases.yaml"
EXPLICIT_DESCRIPTION_PREFIX = "Use only when the user explicitly invokes this Skill. "
LEGACY_DESCRIPTION_PREFIXES = (
    "Explicit skill-use request only. Activate only when the user explicitly asks to use, call, "
    "or apply this skill or an unmistakable plain-language label to a stated task; the exact "
    "identifier is optional. Ordinary task matching is not authorization. ",
    "Explicit top-level skill-use request only. Activate as a primary skill only when the user "
    "explicitly asks to use, call, or apply this skill or an unmistakable plain-language label to "
    "a stated task; the exact identifier is optional. Ordinary task matching is not authorization. "
    "An already authorized primary skill may invoke this skill as a bounded supporting dependency "
    "for the same goal; this does not create a new primary activation. ",
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


def update_installed_description(path: Path, check: bool, summary: str | None = None) -> bool:
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
    base_description = description
    for prefix in (EXPLICIT_DESCRIPTION_PREFIX, *LEGACY_DESCRIPTION_PREFIXES):
        if base_description.startswith(prefix):
            base_description = base_description[len(prefix) :]
            break
    desired = EXPLICIT_DESCRIPTION_PREFIX + (summary or base_description)
    changed = description != desired
    if changed and not check:
        metadata["description"] = desired
        frontmatter = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True, width=1000).rstrip()
        path.write_text(f"---\n{frontmatter}\n---\n{text[end + 5 :]}", encoding="utf-8")
    return changed


def process_root(root: Path, check: bool) -> tuple[list[str], list[str]]:
    manifest = load_mapping(MANIFEST)
    repository_skills = list(manifest.get("skills", {}))
    external_routes = manifest.get("external_skills", {})
    external_skills = list(external_routes)
    explicit_commands = list(manifest.get("explicit_only_commands", []))
    required = repository_skills + ["explicit-skill-router"]
    missing = [name for name in required if not (root / name / "SKILL.md").is_file()]
    if missing:
        raise ValueError(f"{root}: missing required skills: {', '.join(missing)}")

    changed: list[str] = []
    for name in repository_skills + external_skills + explicit_commands:
        skill_dir = root / name
        if not (skill_dir / "SKILL.md").is_file():
            continue
        if update_openai_metadata(skill_dir / "agents" / "openai.yaml", False, check):
            changed.append(f"{name}/agents/openai.yaml")
        if name in external_skills or name in explicit_commands:
            summary = external_routes[name].get("deployed_description") if name in external_skills else None
            if update_installed_description(skill_dir / "SKILL.md", check, summary):
                changed.append(f"{name}/SKILL.md")
    router_dir = root / "explicit-skill-router"
    if update_openai_metadata(router_dir / "agents" / "openai.yaml", True, check):
        changed.append("explicit-skill-router/agents/openai.yaml")
    return changed, missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enforce explicit top-level invocation with bounded supporting delegation."
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
