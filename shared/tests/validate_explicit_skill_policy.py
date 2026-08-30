from __future__ import annotations

from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
ROUTER = ROOT / "explicit-skill-router"
ALIASES = ROUTER / "aliases.yaml"
CASES = Path(__file__).with_name("explicit_skill_routing_cases.yaml")


def read_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def parse_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    metadata = yaml.safe_load(text[4:end])
    if not isinstance(metadata, dict):
        raise ValueError(f"{path}: invalid YAML frontmatter")
    return str(metadata.get("description", ""))


def implicit_policy(skill_dir: Path) -> bool | None:
    metadata_path = skill_dir / "agents" / "openai.yaml"
    metadata = read_yaml(metadata_path)
    policy = metadata.get("policy")
    if not isinstance(policy, dict):
        return None
    value = policy.get("allow_implicit_invocation")
    return value if isinstance(value, bool) else None


def main() -> int:
    errors: list[str] = []

    try:
        alias_data = read_yaml(ALIASES)
    except Exception as exc:  # noqa: BLE001 - aggregate validation errors
        print(f"Explicit skill policy validation failed:\n- {exc}")
        return 1

    skills = alias_data.get("skills")
    if not isinstance(skills, dict) or not skills:
        errors.append("aliases.yaml: skills must be a non-empty mapping")
        skills = {}
    external_skills = alias_data.get("external_skills", {})
    if not isinstance(external_skills, dict):
        errors.append("aliases.yaml: external_skills must be a mapping")
        external_skills = {}
    explicit_only_commands = alias_data.get("explicit_only_commands", [])
    if not isinstance(explicit_only_commands, list) or any(
        not isinstance(name, str) or not name for name in explicit_only_commands
    ):
        errors.append("aliases.yaml: explicit_only_commands must be a list of names")
        explicit_only_commands = []

    for name, route in skills.items():
        skill_dir = ROOT / str(name)
        if not (skill_dir / "SKILL.md").is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        if not isinstance(route, dict) or not isinstance(route.get("labels"), list):
            errors.append(f"{name}: labels must be a list")
        elif len(route["labels"]) < 2 or any(not str(label).strip() for label in route["labels"]):
            errors.append(f"{name}: needs at least two non-empty labels")
        try:
            if implicit_policy(skill_dir) is not False:
                errors.append(f"{name}: allow_implicit_invocation must be false")
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    for name, route in external_skills.items():
        if not isinstance(route, dict) or not isinstance(route.get("labels"), list):
            errors.append(f"{name}: external labels must be a list")
        elif len(route["labels"]) < 2 or any(not str(label).strip() for label in route["labels"]):
            errors.append(f"{name}: needs at least two non-empty external labels")
        try:
            description = parse_description(skill_dir / "SKILL.md").lower()
            for marker in (
                "explicit skill-use request only",
                "explicitly asks to use",
                "exact identifier is optional",
                "not authorization",
            ):
                if marker not in description:
                    errors.append(f"{name}: description missing {marker!r}")
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    try:
        if implicit_policy(ROUTER) is not True:
            errors.append("explicit-skill-router: allow_implicit_invocation must be true")
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))

    router_text = (ROUTER / "SKILL.md").read_text(encoding="utf-8")
    for marker in (
        "only implicitly discoverable entry point",
        "Ordinary intent is not authorization",
        "Authorization expires immediately",
        "never authorizes another skill",
        "Do not perform an automatic handoff",
        "do not infer the target from task semantics",
    ):
        if marker not in router_text:
            errors.append(f"explicit-skill-router: missing marker {marker!r}")

    case_data = read_yaml(CASES)
    cases = case_data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("explicit_skill_routing_cases.yaml: cases must be a non-empty list")
        cases = []
    ids: set[str] = set()
    route_targets = set(skills) | set(external_skills)
    expected_values = route_targets | {"none", "clarify"}
    coverage = {value: 0 for value in ("none", "clarify")}
    active_continuations = 0
    active_expirations = 0
    for case in cases:
        if not isinstance(case, dict):
            errors.append("routing case must be a mapping")
            continue
        case_id = case.get("id")
        if not case_id or case_id in ids:
            errors.append(f"routing cases: missing or duplicate id {case_id!r}")
        ids.add(str(case_id))
        if not case.get("user_prompt"):
            errors.append(f"{case_id}: user_prompt is required")
        expected = case.get("expected")
        if expected not in expected_values:
            errors.append(f"{case_id}: invalid expected route {expected!r}")
        if expected in coverage:
            coverage[expected] += 1
        active_skill = case.get("active_skill")
        if active_skill:
            if active_skill not in route_targets or not case.get("active_scope"):
                errors.append(f"{case_id}: active skill cases require a known skill and active_scope")
            if expected == active_skill:
                active_continuations += 1
            if expected == "none":
                active_expirations += 1

    if coverage["none"] < 6:
        errors.append("routing cases need at least six ordinary-request bypasses")
    if coverage["clarify"] < 1:
        errors.append("routing cases need an ambiguous generic-skill clarification case")
    if active_continuations < 1 or active_expirations < 2:
        errors.append("routing cases need same-scope continuation and multiple expiry cases")

    if errors:
        print("Explicit skill policy validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Explicit skill policy validation passed: "
        f"{len(skills)} repository skills, {len(external_skills)} optional installed skills, "
        f"{len(explicit_only_commands)} explicit commands, 1 narrow router, {len(cases)} routing cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
