"""Check revision traceability, not the scientific adequacy of a reviewer response."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def check_location(location: dict, root: Path) -> str | None:
    path = (root / location["path"]).resolve()
    if not path.is_relative_to(root.resolve()):
        return "location escapes project root"
    if not path.is_file():
        return f"missing file: {location['path']}"
    line = location.get("line")
    if not isinstance(line, int) or isinstance(line, bool) or line < 1:
        return "location needs a positive line number"
    lines = path.read_text(encoding="utf-8").splitlines()
    if line > len(lines):
        return f"line out of range: {location['path']}:{line}"
    anchor = location.get("anchor")
    if not isinstance(anchor, str) or not anchor.strip() or anchor not in lines[line - 1]:
        return f"anchor no longer matches: {location['path']}:{line}"
    return None


def validate_revision_map(data: dict, root: Path) -> list[str]:
    errors, seen = [], set()
    rows = data.get("revisions")
    if not isinstance(rows, list) or not rows:
        return ["revisions must be a nonempty list"]
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not key.strip() or key in seen:
            errors.append("review IDs must be nonempty and unique")
        seen.add(key)
        if not row.get("concern") or not row.get("action"):
            errors.append(f"{key}: concern and action required")
        status = row.get("status")
        if status not in {"proposed", "changed", "verified", "deferred"}:
            errors.append(f"{key}: invalid status")
        if status == "deferred" and not row.get("reason"):
            errors.append(f"{key}: deferred row needs reason")
        if status in {"changed", "verified"}:
            if not row.get("locations"):
                errors.append(f"{key}: changed/verified row needs manuscript locations")
            for location in row.get("locations", []):
                issue = check_location(location, root)
                if issue:
                    errors.append(f"{key}: {issue}")
        if status == "verified":
            if not row.get("verification") or not row.get("evidence"):
                errors.append(f"{key}: verified row needs verification explanation and evidence locations")
            for location in row.get("evidence", []):
                issue = check_location(location, root)
                if issue:
                    errors.append(f"{key}: {issue}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        errors = validate_revision_map(json.loads(args.input.read_text(encoding="utf-8")), args.project_root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [str(exc)]
    print(json.dumps({"structural_errors": errors, "scientific_adequacy": "not assessed"}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
