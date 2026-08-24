from __future__ import annotations

import json
from collections import Counter

from .library_reader import LibraryReader


def normalize_note_paper_id(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if value.startswith("native-library:"):
        return value.split(":", 1)[1]
    return value


class PaperMatcher:
    def __init__(self, library_reader: LibraryReader):
        self.library_reader = library_reader

    def _parse_json_value(self, raw_value: object) -> object:
        if not isinstance(raw_value, str) or not raw_value.strip():
            return None
        try:
            return json.loads(raw_value)
        except Exception:
            return None

    def _anchor_paper_ids(self, note: dict) -> list[str]:
        anchors = self._parse_json_value(note.get("anchors"))
        if not isinstance(anchors, list):
            return []
        paper_ids: list[str] = []
        for anchor in anchors:
            if not isinstance(anchor, dict):
                continue
            for key in ("paperId", "workspaceId", "targetPaperId"):
                normalized = normalize_note_paper_id(anchor.get(key))
                if normalized:
                    paper_ids.append(normalized)
        return paper_ids

    def _linked_paper_ids(self, note: dict) -> list[str]:
        values: list[str] = []
        parsed = self._parse_json_value(note.get("linked_paper_ids"))
        if isinstance(parsed, list):
            for item in parsed:
                normalized = normalize_note_paper_id(item if isinstance(item, str) else None)
                if normalized:
                    values.append(normalized)
        single = normalize_note_paper_id(note.get("linked_paper_id"))
        if single:
            values.append(single)
        return values

    def resolve_from_note_details(self, note: dict, explicit_paper_id: str | None = None) -> dict:
        anchor_ids = self._anchor_paper_ids(note)
        linked_ids = self._linked_paper_ids(note)
        note_paper_id = normalize_note_paper_id(note.get("paper_id"))

        scores: Counter[str] = Counter()
        reasons: dict[str, list[str]] = {}

        for paper_id in anchor_ids:
            scores[paper_id] += 100
            reasons.setdefault(paper_id, []).append("anchor")
        for paper_id in linked_ids:
            scores[paper_id] += 30
            reasons.setdefault(paper_id, []).append("linked")
        if note_paper_id:
            scores[note_paper_id] += 10
            reasons.setdefault(note_paper_id, []).append("note.paper_id")

        ranked_candidates = [
            {
                "paper_id": paper_id,
                "score": score,
                "reasons": reasons.get(paper_id, []),
                "anchor_hits": anchor_ids.count(paper_id),
            }
            for paper_id, score in scores.most_common()
        ]

        explicit_paper_id = normalize_note_paper_id(explicit_paper_id)
        unique_anchor_ids = list(dict.fromkeys(anchor_ids))
        conflicts: list[str] = []
        if len(unique_anchor_ids) > 1:
            conflicts.append("anchors reference multiple papers")
        if note_paper_id and unique_anchor_ids and note_paper_id not in unique_anchor_ids:
            conflicts.append("note.paper_id disagrees with anchors")

        if explicit_paper_id:
            paper = self.library_reader.get_paper(explicit_paper_id)
            return {
                "paper": paper,
                "resolution": {
                    "status": "explicit-override" if paper else "paper-not-found",
                    "strategy": "explicit-paper-id",
                    "selected_paper_id": explicit_paper_id if paper else None,
                    "selected_reasons": ["explicit-paper-id"] if paper else [],
                    "selected_score": None,
                    "anchor_paper_ids": anchor_ids,
                    "linked_paper_ids": linked_ids,
                    "note_paper_id": note_paper_id,
                    "conflicts": conflicts,
                    "candidates": ranked_candidates,
                },
            }

        if conflicts:
            return {
                "paper": None,
                "resolution": {
                    "status": "conflict",
                    "strategy": "refuse-conflicted-mapping",
                    "selected_paper_id": None,
                    "selected_reasons": [],
                    "selected_score": None,
                    "anchor_paper_ids": anchor_ids,
                    "linked_paper_ids": linked_ids,
                    "note_paper_id": note_paper_id,
                    "conflicts": conflicts,
                    "candidates": ranked_candidates,
                },
            }

        for candidate in ranked_candidates:
            paper = self.library_reader.get_paper(candidate["paper_id"])
            if paper:
                return {
                    "paper": paper,
                    "resolution": {
                        "status": "resolved",
                        "strategy": "anchor-weighted-candidates",
                        "selected_paper_id": candidate["paper_id"],
                        "selected_reasons": candidate["reasons"],
                        "selected_score": candidate["score"],
                        "anchor_paper_ids": anchor_ids,
                        "linked_paper_ids": linked_ids,
                        "note_paper_id": note_paper_id,
                        "conflicts": [],
                        "candidates": ranked_candidates,
                    },
                }

        return {
            "paper": None,
            "resolution": {
                "status": "paper-not-found",
                "strategy": "anchor-weighted-candidates",
                "selected_paper_id": None,
                "selected_reasons": [],
                "selected_score": None,
                "anchor_paper_ids": anchor_ids,
                "linked_paper_ids": linked_ids,
                "note_paper_id": note_paper_id,
                "conflicts": [],
                "candidates": ranked_candidates,
            },
        }

    def resolve_from_note(self, note: dict) -> dict | None:
        return self.resolve_from_note_details(note)["paper"]
