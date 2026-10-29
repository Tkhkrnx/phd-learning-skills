"""Local learning records; assessments are supplied judgments, not automated mastery."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import sys


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_session(goal: str, materials: list[Path]) -> dict:
    if not goal.strip():
        raise ValueError("goal must not be blank")
    return {
        "schema_version": 1,
        "goal": goal,
        "sources": [{"path": str(p.resolve()), "sha256": fingerprint(p)} for p in materials],
        "concepts": [],
        "exercises": [],
        "attempts": [],
    }


def set_plan(state: dict, concepts: list[dict]) -> None:
    ids = [c["id"] for c in concepts]
    if not ids or any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("concept IDs must be nonempty and unique")
    by_id = {c["id"]: c for c in concepts}
    for concept in concepts:
        if not concept.get("title") or not concept.get("source"):
            raise ValueError("each concept needs a title and source locator")
        dependencies = concept.get("prerequisites", [])
        if not isinstance(dependencies, list) or any(dep not in by_id for dep in dependencies):
            raise ValueError("unknown prerequisite")
    visiting, visited = set(), set()

    def visit(key: str) -> None:
        if key in visiting:
            raise ValueError("cyclic prerequisite graph")
        if key in visited:
            return
        visiting.add(key)
        for dep in by_id[key].get("prerequisites", []):
            visit(dep)
        visiting.remove(key)
        visited.add(key)

    for key in ids:
        visit(key)
    used = {e["concept"] for e in state["exercises"]} | {a["concept"] for a in state["attempts"]}
    if used - set(ids):
        raise ValueError("new plan would orphan exercises or attempts")
    state["concepts"] = concepts


def add_exercise(state: dict, item: dict) -> None:
    if not all(isinstance(item.get(k), str) and item[k].strip() for k in ("id", "concept", "prompt", "answer", "source")):
        raise ValueError("exercise requires id, concept, prompt, answer, and source")
    if item["concept"] not in {c["id"] for c in state["concepts"]}:
        raise ValueError("unknown concept")
    if item["id"] in {e["id"] for e in state["exercises"]}:
        raise ValueError("exercise ID already exists; preserve historical questions")
    state["exercises"].append(item)


def record_attempt(state: dict, *, exercise: str, response: str, assessment: str,
                   feedback: str, error_type: str = "", review_on: str | None = None) -> None:
    item = next((e for e in state["exercises"] if e["id"] == exercise), None)
    if item is None:
        raise ValueError("unknown exercise")
    if not response.strip() or not feedback.strip():
        raise ValueError("record the actual learner response and feedback")
    if assessment not in {"correct", "partial", "incorrect", "unassessed"}:
        raise ValueError("invalid assessment")
    if assessment in {"partial", "incorrect"} and not error_type.strip():
        raise ValueError("partial/incorrect attempts need a concrete error type")
    if review_on:
        date.fromisoformat(review_on)
    state["attempts"].append({
        "exercise": exercise, "concept": item["concept"], "response": response,
        "assessment": assessment, "feedback": feedback, "error_type": error_type,
        "review_on": review_on, "recorded_at": datetime.now(timezone.utc).isoformat(),
        "assessment_origin": "tutor-supplied; not independently validated",
    })


def session_status(state: dict, today: date | None = None) -> dict:
    today = today or date.today()
    source_changes = []
    for source in state["sources"]:
        path = Path(source["path"])
        status = "missing" if not path.is_file() else ("unchanged" if fingerprint(path) == source["sha256"] else "changed")
        source_changes.append({"path": str(path), "status": status})
    latest = {}
    for attempt in state["attempts"]:
        latest[attempt["exercise"]] = attempt
    return {
        "goal": state["goal"], "sources": source_changes,
        "source_review_required": any(s["status"] != "unchanged" for s in source_changes),
        "concepts": [{"id": c["id"], "evidence": [a for a in latest.values() if a["concept"] == c["id"]]} for c in state["concepts"]],
        "due": [a for a in latest.values() if a.get("review_on") and date.fromisoformat(a["review_on"]) <= today],
        "last_attempt": state["attempts"][-1] if state["attempts"] else None,
        "mastery": "not inferred; inspect learner reasoning and transfer evidence",
    }


def export_markdown(state: dict) -> str:
    lines = ["# Learning Session", "", state["goal"], "", "## Sources", ""]
    for source in session_status(state)["sources"]:
        lines.append(f"- {source['path']} ({source['status']})")
    lines.extend(["", "## Learning Path", ""])
    for concept in state["concepts"]:
        dependencies = ", ".join(concept.get("prerequisites", [])) or "none"
        lines.append(f"- {concept['id']}: {concept['title']}; prerequisites: {dependencies}; source: {concept['source']}")
    lines.extend(["", "## Attempts and Next Review", ""])
    for attempt in state["attempts"]:
        lines.extend([f"### {attempt['exercise']} ({attempt['assessment']})", "", attempt["response"], "",
                      attempt["feedback"], f"Error: {attempt['error_type'] or 'none recorded'}; review: {attempt['review_on'] or 'not scheduled'}", ""])
    lines.append("Recorded assessments do not establish whole-topic mastery.")
    return "\n".join(lines) + "\n"


def save_session(path: Path, state: dict, previous: str) -> None:
    payload = json.dumps(state, ensure_ascii=False, indent=2)
    temporary = path.with_suffix(path.suffix + ".tmp")
    # Exclusive staging serializes helper writers; stale readers must not erase new attempts.
    with temporary.open("x", encoding="utf-8") as stream:
        try:
            if path.read_text(encoding="utf-8") != previous:
                raise ValueError("session changed in another process; reload before updating")
            stream.write(payload)
        except BaseException:
            stream.close()
            temporary.unlink()
            raise
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--goal", required=True)
    init.add_argument("--material", action="append", type=Path, default=[])
    for name in ("plan", "exercise"):
        command = commands.add_parser(name)
        command.add_argument("--input", required=True, type=Path)
    attempt = commands.add_parser("attempt")
    attempt.add_argument("--exercise", required=True)
    attempt.add_argument("--response", required=True)
    attempt.add_argument("--assessment", choices=("correct", "partial", "incorrect", "unassessed"), required=True)
    attempt.add_argument("--feedback", required=True)
    attempt.add_argument("--error-type", default="")
    attempt.add_argument("--review-on")
    commands.add_parser("status")
    export = commands.add_parser("export")
    export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            state = create_session(args.goal, args.material)
            args.state.parent.mkdir(parents=True, exist_ok=True)
            with args.state.open("x", encoding="utf-8") as stream:
                json.dump(state, stream, ensure_ascii=False, indent=2)
        else:
            previous = args.state.read_text(encoding="utf-8")
            state = json.loads(previous)
            if state.get("schema_version") != 1:
                raise ValueError("unsupported session schema")
            if args.command == "status":
                print(json.dumps(session_status(state), ensure_ascii=False, indent=2))
                return 0
            if args.command == "export":
                args.output.parent.mkdir(parents=True, exist_ok=True)
                with args.output.open("x", encoding="utf-8") as stream:
                    stream.write(export_markdown(state))
                return 0
            if args.command == "plan":
                set_plan(state, json.loads(args.input.read_text(encoding="utf-8"))["concepts"])
            elif args.command == "exercise":
                add_exercise(state, json.loads(args.input.read_text(encoding="utf-8")))
            else:
                record_attempt(state, exercise=args.exercise, response=args.response, assessment=args.assessment,
                               feedback=args.feedback, error_type=args.error_type, review_on=args.review_on)
            save_session(args.state, state, previous)
        print(f"saved={args.state.resolve()}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Learning session failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
