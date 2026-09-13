from __future__ import annotations

from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
ROUTER = ROOT / "explicit-skill-router"
ALIASES = ROUTER / "aliases.yaml"
CASES = Path(__file__).with_name("explicit_skill_routing_cases.yaml")
MAX_DESCRIPTION_CHARS = 180
STALE_DESCRIPTION_MARKERS = (
    "exact identifier is optional",
    "ordinary task matching is not authorization",
    "already authorized primary skill",
    "bounded supporting dependency",
    "does not create a new primary activation",
)


def read_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def parse_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
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
    metadata = read_yaml(skill_dir / "agents" / "openai.yaml")
    policy = metadata.get("policy")
    return policy.get("allow_implicit_invocation") if isinstance(policy, dict) else None


def main() -> int:
    errors: list[str] = []
    aliases = read_yaml(ALIASES)
    skills = aliases.get("skills", {})
    external_skills = aliases.get("external_skills", {})
    commands = aliases.get("explicit_only_commands", [])
    if not isinstance(skills, dict) or not skills:
        errors.append("aliases.yaml: skills must be a non-empty mapping")
        skills = {}
    if not isinstance(external_skills, dict):
        errors.append("aliases.yaml: external_skills must be a mapping")
        external_skills = {}
    if not isinstance(commands, list):
        errors.append("aliases.yaml: explicit_only_commands must be a list")
        commands = []

    for name, route in skills.items():
        skill_dir = ROOT / str(name)
        if not (skill_dir / "SKILL.md").is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        labels = route.get("labels") if isinstance(route, dict) else None
        if not isinstance(labels, list) or len(labels) < 2:
            errors.append(f"{name}: needs at least two aliases")
        try:
            if implicit_policy(skill_dir) is not False:
                errors.append(f"{name}: allow_implicit_invocation must be false")
            description = parse_description(skill_dir / "SKILL.md")
            if not description or len(description) > MAX_DESCRIPTION_CHARS:
                errors.append(f"{name}: description must be 1-{MAX_DESCRIPTION_CHARS} characters")
            if "explicitly" not in description.lower():
                errors.append(f"{name}: description must state its explicit trigger")
            for marker in STALE_DESCRIPTION_MARKERS:
                if marker in description.lower():
                    errors.append(f"{name}: stale policy boilerplate remains: {marker!r}")
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    try:
        if implicit_policy(ROUTER) is not True:
            errors.append("explicit-skill-router: allow_implicit_invocation must be true")
        router_description = parse_description(ROUTER / "SKILL.md")
        if len(router_description) > MAX_DESCRIPTION_CHARS:
            errors.append("explicit-skill-router: description is too long")
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))

    router_text = (ROUTER / "SKILL.md").read_text(encoding="utf-8")
    for marker in (
        "only implicitly discoverable entrypoint",
        "do not infer it from task semantics",
        "authorization covers follow-ups",
        "supporting Skill",
        "normal execution",
    ):
        if marker not in router_text:
            errors.append(f"explicit-skill-router: missing marker {marker!r}")

    case_data = read_yaml(CASES)
    cases = case_data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        errors.append("routing cases must be a non-empty list")
        cases = []
    route_targets = set(skills) | set(external_skills)
    valid_expected = route_targets | {"none", "clarify"}

    for name, route in external_skills.items():
        summary = route.get("deployed_description") if isinstance(route, dict) else None
        if not isinstance(summary, str) or not summary.strip() or len(summary) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{name}: deployed_description must be 1-{MAX_DESCRIPTION_CHARS} characters")
    seen: set[str] = set()
    ordinary_bypasses = 0
    clarifications = 0
    supporting_delegations = 0
    for case in cases:
        case_id = str(case.get("id", ""))
        if not case_id or case_id in seen:
            errors.append(f"routing cases: missing or duplicate id {case_id!r}")
        seen.add(case_id)
        expected = case.get("expected")
        if expected not in valid_expected:
            errors.append(f"{case_id}: invalid expected route {expected!r}")
        ordinary_bypasses += expected == "none"
        clarifications += expected == "clarify"
        expected_support = case.get("expected_support", [])
        if expected_support:
            supporting_delegations += 1
            if expected not in route_targets:
                errors.append(f"{case_id}: supporting delegation requires a primary target")
        for field in ("expected_support", "forbidden_support"):
            values = case.get(field, [])
            if not isinstance(values, list) or any(value not in route_targets for value in values):
                errors.append(f"{case_id}: {field} contains an unknown target")

    if ordinary_bypasses < 6:
        errors.append("routing cases need at least six ordinary-request bypasses")
    if clarifications < 1:
        errors.append("routing cases need an ambiguous-label clarification case")
    if supporting_delegations < 2:
        errors.append("routing cases need at least two bounded supporting cases")

    if errors:
        print("Explicit skill policy validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Explicit skill policy validation passed: "
        f"{len(skills)} repository Skills, {len(external_skills)} optional Skills, "
        f"{len(commands)} explicit command adapters, {len(cases)} routing cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
