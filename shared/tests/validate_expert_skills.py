from __future__ import annotations

from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "AGENT_COLLABORATION_SKILL_BLUEPRINT.md"
CASES = Path(__file__).with_name("expert_skill_transcript_cases.yaml")
MAX_DESCRIPTION_CHARS = 180
MAX_ENTRYPOINT_LINES = 80

SPECS = {
    "research-problem-formulation": {
        "stages": {"observe", "localize", "contrast", "state", "pressure-test"},
        "root": {
            "declarative problem",
            "what the problem is",
            "why it matters",
            "why existing work still fails",
            "Collaboration contract",
            "Load on demand",
        },
        "reference": {"Semantic model", "New-problem route", "Revision route", "Evidence stop rule"},
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
        "root": {"prior-method failure", "Collaboration contract", "Load on demand", "kill criterion"},
        "reference": {"Root challenge", "Candidate principles", "Fact gate", "Kill criterion"},
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
        "root": {"relevant architecture slice", "Collaboration contract", "Load on demand", "edit-run-inspect-fix-revalidate"},
        "reference": {"Requirement contract", "Architecture slice", "First slice", "Handoff and execution"},
    },
    "targeted-knowledge-closure": {
        "stages": {"diagnose", "explain-one-grain", "correct", "transfer"},
        "root": {"smallest concept", "Collaboration contract", "Load on demand", "observable user reasoning"},
        "reference": {"Diagnose the smallest gap", "Choose a representation", "Repair and transfer", "Process integrity"},
    },
}

FORBIDDEN_SCAFFOLD = (
    r"90%",
    r"ten-percent",
    r"completely before responding",
    r"read .+ completely before",
    r"advance exactly one stage",
    r"ask exactly one",
)


def parse_skill(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
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
        "explicit-only through `agents/openai.yaml`",
        "Ask a focused question when",
        "Do not close a consequential collaboration as an agent-only monologue",
        "Evidence boundaries",
        "Supporting Skills",
        "implement, run, inspect, repair",
        "loading every shared reference",
    ):
        if marker not in blueprint:
            errors.append(f"blueprint: missing marker {marker!r}")

    for pattern in FORBIDDEN_SCAFFOLD:
        if re.search(pattern, blueprint, flags=re.IGNORECASE):
            errors.append(f"blueprint: legacy scaffold remains: {pattern!r}")

    for name, spec in SPECS.items():
        skill_path = ROOT / name / "SKILL.md"
        reference_path = ROOT / name / "references" / "deep-workflow.md"
        try:
            metadata, body = parse_skill(skill_path)
        except Exception as exc:  # noqa: BLE001 - aggregate validation boundary
            errors.append(f"{name}: {exc}")
            continue

        if metadata.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        description = str(metadata.get("description", ""))
        if not description or len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{name}: description must be 1-{MAX_DESCRIPTION_CHARS} characters")
        if "explicitly" not in description.lower():
            errors.append(f"{name}: description must state its explicit trigger")
        if len(body.splitlines()) > MAX_ENTRYPOINT_LINES:
            errors.append(f"{name}: entrypoint exceeds {MAX_ENTRYPOINT_LINES} lines")
        for marker in spec["root"]:
            if marker not in body:
                errors.append(f"{name}: root missing marker {marker!r}")
        for marker in ("agent-only monologue", "yes/no"):
            if marker not in body:
                errors.append(f"{name}: root missing collaboration invariant {marker!r}")
        if not reference_path.is_file():
            errors.append(f"{name}: missing references/deep-workflow.md")
        else:
            reference = reference_path.read_text(encoding="utf-8")
            for marker in spec["reference"]:
                if marker not in reference:
                    errors.append(f"{name}: reference missing marker {marker!r}")

        combined = body + "\n" + (reference_path.read_text(encoding="utf-8") if reference_path.is_file() else "")
        for pattern in FORBIDDEN_SCAFFOLD:
            if re.search(pattern, combined, flags=re.IGNORECASE):
                errors.append(f"{name}: legacy scaffold remains: {pattern!r}")

        try:
            openai_data = yaml.safe_load((ROOT / name / "agents" / "openai.yaml").read_text(encoding="utf-8"))
            if openai_data.get("policy", {}).get("allow_implicit_invocation") is not False:
                errors.append(f"{name}: implicit invocation must be disabled")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: invalid agents/openai.yaml: {exc}")

    case_data = yaml.safe_load(CASES.read_text(encoding="utf-8"))
    trigger_cases = case_data.get("trigger_cases", []) if isinstance(case_data, dict) else []
    coverage = {name: {True: 0, False: 0} for name in SPECS}
    for case in trigger_cases:
        name = case.get("skill")
        activate = case.get("activate")
        if name not in SPECS or not isinstance(activate, bool):
            errors.append(f"trigger case {case.get('id')!r}: invalid skill or activate value")
            continue
        coverage[name][activate] += 1
        if activate and "skill" not in str(case.get("user_prompt", "")).lower() and "技能" not in str(case.get("user_prompt", "")):
            errors.append(f"trigger case {case.get('id')!r}: missing explicit Skill request")
    for name, counts in coverage.items():
        if counts[True] < 2 or counts[False] < 2:
            errors.append(f"trigger cases: {name} needs at least two activate and two bypass cases")

    transcript_cases = case_data.get("cases", []) if isinstance(case_data, dict) else []
    transcript_coverage = {name: 0 for name in SPECS}
    for case in transcript_cases:
        name = case.get("skill")
        if name not in SPECS:
            errors.append(f"transcript case {case.get('id')!r}: unknown skill")
            continue
        transcript_coverage[name] += 1
        if case.get("expected_stage") not in SPECS[name]["stages"]:
            errors.append(f"transcript case {case.get('id')!r}: invalid expected_stage")
        if not case.get("required") or not case.get("forbidden"):
            errors.append(f"transcript case {case.get('id')!r}: required and forbidden must be non-empty")
    for name, count in transcript_coverage.items():
        if count < 2:
            errors.append(f"transcript cases: {name} needs at least two cases")

    evidence = ROOT / "shared" / "expert-skill-references" / "research_evidence_acquisition.md"
    if not evidence.is_file():
        errors.append("missing research evidence acquisition reference")

    if errors:
        print("Expert skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Expert skill validation passed: "
        f"{len(SPECS)} routed Skills, {len(trigger_cases)} trigger cases, "
        f"{len(transcript_cases)} transcript cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
