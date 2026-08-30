from __future__ import annotations

from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "AGENT_COLLABORATION_SKILL_BLUEPRINT.md"
CASES = Path(__file__).with_name("expert_skill_transcript_cases.yaml")

SPECS = {
    "research-problem-formulation": {
        "stages": {"observe", "localize", "contrast", "state", "pressure-test"},
        "markers": {
            "Academic Problem Viability Audit",
            "Evidence Acquisition Gate",
            "query portfolio",
            "evidence ledger",
            "what the problem is",
            "why it matters",
            "why existing work still fails",
        },
        "trigger_markers": {"research idea", "academic problem", "not authorization"},
    },
    "research-method-design": {
        "stages": {
            "root-challenge",
            "mechanism-source",
            "fact-gate",
            "assumptions",
            "simpler-alternative",
            "kill-criterion",
            "minimal-experiment",
        },
        "markers": {
            "Mechanism Evidence Gate",
            "structural signature",
            "repositories",
            "analogy-break condition",
            "root challenge and relevant boundary conditions",
            "causal mechanism and feasible system carrier",
            "kill criterion",
            "first discriminating experiment",
        },
        "trigger_markers": {"established", "solution directions", "replay repair or execution"},
    },
    "engineering-task-decomposition": {
        "stages": {
            "requirement-contract",
            "architecture-slice",
            "dependency-boundary",
            "options",
            "first-slice",
            "execution-handoff",
        },
        "markers": {"real requirement, non-goals, and acceptance evidence", "real codebase and runtime understanding", "first reversible execution slice"},
        "trigger_markers": {"requirement-analysis", "before implementation", "direct coding"},
    },
    "targeted-knowledge-closure": {
        "stages": {"diagnose", "explain-one-grain", "correct", "transfer"},
        "markers": {"accurate mental model with repaired prerequisites", "discrimination from a plausible near miss", "reduced scaffolding"},
        "trigger_markers": {"concept-learning", "concrete artifact", "not authorization"},
    },
}

REQUIRED_HEADINGS = {
    "## Goal and Expert Role",
    "## Convergence Target",
    "## Interaction Gate",
    "## Stage Machine",
    "## Exit and Handoff",
    "## Completion Evidence",
}


def parse_skill(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    metadata = yaml.safe_load(text[4:end])
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter is not a mapping")
    return metadata, text[end + 5 :]


def main() -> int:
    errors: list[str] = []
    blueprint = BLUEPRINT.read_text(encoding="utf-8")
    for marker in (
        "user-facing collaboration protocols",
        "Adaptive Interaction and Shared-Confidence Gate",
        "The agent may lead with",
        "90% confidence",
        "meaningful user exchange",
        "Automatic Failure Conditions",
        "explicit skill-use request",
        "exact repository identifier is not required",
        "Authorization expires",
        "Skill Composition and Handoff Rules",
        "supporting delegation",
        "primary skill remains accountable",
        "return control",
        "new primary",
        "Exit silently",
        "ordinary execution request triggers",
        "Expert Strength Without Takeover",
        "progressive transfer",
        "Track the active skill",
        "Do not expose protocol syntax",
        "yes/no questions",
        "evidence acquisition is a hard gate",
        "research_evidence_acquisition.md",
    ):
        if marker not in blueprint:
            errors.append(f"blueprint: missing marker {marker!r}")

    for name, spec in SPECS.items():
        path = ROOT / name / "SKILL.md"
        try:
            metadata, body = parse_skill(path)
        except Exception as exc:  # noqa: BLE001 - aggregate validator errors
            errors.append(f"{name}: {exc}")
            continue

        if set(metadata) != {"name", "description"}:
            errors.append(f"{name}: frontmatter must contain only name and description")
        if metadata.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        description = str(metadata.get("description", "")).lower()
        for marker in (
            "explicit skill-use request only",
            "trigger only when",
            "explicitly asks to use",
            "exact identifier is optional",
            "not authorization",
            "already authorized primary skill",
            "bounded supporting dependency",
            "does not create a new primary activation",
            "do not trigger merely",
        ):
            if marker not in description:
                errors.append(f"{name}: description lacks explicit-use boundary marker {marker!r}")
        for marker in spec["trigger_markers"]:
            if marker not in description:
                errors.append(f"{name}: description lacks trigger marker {marker!r}")
        if len(description) > 900:
            errors.append(f"{name}: description is too long")

        openai_metadata = ROOT / name / "agents" / "openai.yaml"
        try:
            openai_data = yaml.safe_load(openai_metadata.read_text(encoding="utf-8"))
            if openai_data.get("policy", {}).get("allow_implicit_invocation") is not False:
                errors.append(f"{name}: implicit invocation must be disabled")
        except Exception as exc:  # noqa: BLE001 - aggregate validator errors
            errors.append(f"{name}: invalid agents/openai.yaml: {exc}")

        headings = {line for line in body.splitlines() if line.startswith("## ")}
        missing_headings = REQUIRED_HEADINGS - headings
        if missing_headings:
            errors.append(f"{name}: missing headings {sorted(missing_headings)}")
        if "90%" not in body:
            errors.append(f"{name}: missing practical shared-confidence gate")
        if "meaningful exchange" not in body and "meaningful interaction" not in body:
            errors.append(f"{name}: missing iterative interaction evidence")
        if "Open question:" not in body:
            errors.append(f"{name}: missing open-question stage interface")
        if "Keep the skill name, stage name, status, and reasoning focus internal" not in body:
            errors.append(f"{name}: missing user-facing internal-state boundary")
        if "User-owned judgment:" in body:
            errors.append(f"{name}: legacy judgment interface remains")
        if "yes/no" not in body:
            errors.append(f"{name}: missing yes/no anti-pattern")
        if "Advance exactly one stage" in body or "ask exactly one" in body:
            errors.append(f"{name}: legacy rigid turn gate remains")
        for stage in spec["stages"]:
            if f"`{stage}`" not in body:
                errors.append(f"{name}: missing stage {stage!r}")
        for marker in spec["markers"]:
            if marker not in body:
                errors.append(f"{name}: missing skill-specific marker {marker!r}")
        if len(body.splitlines()) > 220:
            errors.append(f"{name}: SKILL.md exceeds 220-line context budget")
        if "execution-support" in body:
            errors.append(f"{name}: forbidden agent-only execution mode found")
        if "Suspend this skill" in body or "Suspend immediately" in body:
            errors.append(f"{name}: visible suspension behavior remains")

    for forbidden_marker in ("[skill-run] skill=", "[skill-run-result] skill="):
        if forbidden_marker in blueprint:
            errors.append(f"blueprint: visible lifecycle marker remains {forbidden_marker!r}")

    case_data = yaml.safe_load(CASES.read_text(encoding="utf-8"))
    trigger_cases = case_data.get("trigger_cases", []) if isinstance(case_data, dict) else []
    trigger_coverage = {name: {True: 0, False: 0} for name in SPECS}
    trigger_ids: set[str] = set()
    for case in trigger_cases:
        case_id = case.get("id")
        skill = case.get("skill")
        activate = case.get("activate")
        if not case_id or case_id in trigger_ids:
            errors.append(f"trigger_cases: missing or duplicate id {case_id!r}")
        trigger_ids.add(case_id)
        if skill not in SPECS:
            errors.append(f"trigger_cases: unknown skill {skill!r}")
            continue
        if not isinstance(activate, bool):
            errors.append(f"{case_id}: activate must be boolean")
            continue
        trigger_coverage[skill][activate] += 1
        if not case.get("user_prompt") or not case.get("reason"):
            errors.append(f"{case_id}: user_prompt and reason are required")
        prompt = str(case.get("user_prompt", "")).lower()
        if activate and "skill" not in prompt and "技能" not in prompt:
            errors.append(f"{case_id}: activating prompt lacks an explicit skill-use request")
    for skill, counts in trigger_coverage.items():
        if counts[True] < 2 or counts[False] < 2:
            errors.append(f"trigger_cases: {skill} needs at least two activate and two bypass cases")

    cases = case_data.get("cases", []) if isinstance(case_data, dict) else []
    coverage = {name: 0 for name in SPECS}
    ids: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        skill = case.get("skill")
        if not case_id or case_id in ids:
            errors.append(f"cases: missing or duplicate id {case_id!r}")
        ids.add(case_id)
        if skill not in SPECS:
            errors.append(f"cases: unknown skill {skill!r}")
            continue
        coverage[skill] += 1
        if case.get("expected_stage") not in SPECS[skill]["stages"]:
            errors.append(f"{case_id}: invalid expected_stage")
        if not case.get("required") or not case.get("forbidden"):
            errors.append(f"{case_id}: required and forbidden checks must be non-empty")
    for skill, count in coverage.items():
        if count < 2:
            errors.append(f"cases: {skill} needs at least two regression cases")

    theory = ROOT / "shared" / "expert-skill-references" / "collaboration_theory.md"
    if not theory.is_file():
        errors.append("missing collaboration theory reference")

    evidence_protocol = ROOT / "shared" / "expert-skill-references" / "research_evidence_acquisition.md"
    if not evidence_protocol.is_file():
        errors.append("missing research evidence acquisition reference")
    else:
        evidence_text = evidence_protocol.read_text(encoding="utf-8")
        for marker in (
            "Problem-boundary evidence",
            "Mechanism-inspiration evidence",
            "Query Portfolio",
            "Evidence Ledger",
            "Coverage and Stop Rule",
            "Cross-domain observation is a hypothesis source, not design proof",
            "internal evidence backend",
        ):
            if marker not in evidence_text:
                errors.append(f"research evidence protocol: missing marker {marker!r}")

    if errors:
        print("Expert skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Expert skill validation passed: "
        f"{len(SPECS)} skills, {len(trigger_cases)} trigger cases, {len(cases)} transcript cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
