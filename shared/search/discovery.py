from __future__ import annotations

import re
from typing import Any

from shared.search.official_sources import search_official_sources_for_subtopic
from shared.search.paper_search import rows_to_search_results, search_short_queries_for_subtopic


def discover_for_subtopic(
    *,
    topic_name: str,
    subtopic: dict[str, Any],
    preferred_venues: list[str],
    fallback_venues: list[str],
    min_year: int,
    limit: int,
) -> tuple[list, list[str]]:
    keywords = list(subtopic.get("keywords") or []) + list(subtopic.get("seed_papers") or [])
    notes: list[str] = []
    preferred = preferred_venues
    fallback = fallback_venues

    official_rows, official_notes = search_official_sources_for_subtopic(
        subtopic=subtopic,
        preferred_venues=preferred,
        fallback_venues=fallback,
        min_year=min_year,
        limit=limit,
    )
    notes.extend(f"official:{note}" for note in official_notes)
    official_results = rows_to_search_results(
        official_rows,
        preferred_venues=preferred,
        fallback_venues=fallback,
        subtopic_id=subtopic.get("id") or "unknown",
        keywords=keywords,
        min_year=min_year,
    )
    if len(official_results) >= limit:
        return official_results[:limit], notes

    aggregate_results, aggregate_notes = search_short_queries_for_subtopic(
        topic_name=topic_name,
        subtopic=subtopic,
        preferred_venues=preferred,
        fallback_venues=fallback,
        min_year=min_year,
        limit=limit,
    )
    notes.extend(f"aggregate:{note}" for note in aggregate_notes)
    results = official_results + [row for row in aggregate_results if all(row.title != existing.title for existing in official_results)]
    return results[:limit], notes


def _normalize_text(text: str) -> str:
    lowered = (text or "").lower().replace("-", " ")
    lowered = re.sub(r"[^a-z0-9\s]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def _keywords_from_query(query: str) -> list[str]:
    parts = [part.strip() for part in query.replace("/", " ").replace(",", " ").split()]
    return [part for part in parts if len(part) >= 3]


def _query_matches_subtopic(query: str, subtopic: dict[str, Any]) -> bool:
    lowered = _normalize_text(query)
    name = _normalize_text(str(subtopic.get("name") or ""))
    if name and name in lowered:
        return True
    for keyword in list(subtopic.get("keywords") or []) + list(subtopic.get("seed_papers") or []) + list(subtopic.get("aliases") or []):
        normalized = _normalize_text(str(keyword).strip())
        if normalized and normalized in lowered:
            return True
    return False


def _subtopic_overlap_score(query: str, subtopic: dict[str, Any]) -> int:
    lowered = _normalize_text(query)
    score = 0
    name = _normalize_text(str(subtopic.get("name") or ""))
    if name and name in lowered:
        score += 80
    for keyword in list(subtopic.get("keywords") or []) + list(subtopic.get("seed_papers") or []) + list(subtopic.get("aliases") or []):
        normalized = _normalize_text(str(keyword).strip())
        if not normalized:
            continue
        if normalized in lowered:
            score += 40 if " " in normalized else 20
    return score


def discover_for_query(
    *,
    query: str,
    topics: list[dict[str, Any]],
    preferred_venues: list[str],
    fallback_venues: list[str],
    min_year: int,
    limit: int,
) -> tuple[list, list[str]]:
    keywords = _keywords_from_query(query)
    notes: list[str] = []
    matched_subtopics: list[tuple[int, dict[str, Any], dict[str, Any]]] = []

    topic_overlap: dict[str, int] = {}
    for topic in topics:
        topic_name = _normalize_text(str(topic.get("name") or ""))
        aliases = [topic_name] + [_normalize_text(str(alias).strip()) for alias in topic.get("aliases") or []]
        topic_score = 0
        for alias in aliases:
            if alias and alias in _normalize_text(query):
                topic_score += 80 if " " in alias else 20
        topic_overlap[topic.get("id") or topic_name] = topic_score
        for subtopic in topic.get("subtopics") or []:
            overlap = _subtopic_overlap_score(query, subtopic)
            overlap += topic_overlap.get(topic.get("id") or topic_name, 0)
            if overlap > 0:
                matched_subtopics.append((overlap, topic, subtopic))

    if not matched_subtopics:
        query_l = _normalize_text(query)
        topic_matches: list[dict[str, Any]] = []
        for topic in topics:
            topic_name = _normalize_text(str(topic.get("name") or ""))
            aliases = [topic_name] + [_normalize_text(str(alias).strip()) for alias in topic.get("aliases") or []]
            if any(alias and alias in query_l for alias in aliases):
                topic_matches.append(topic)
        if not topic_matches:
            topic_matches = topics
        for topic in topic_matches:
            for subtopic in topic.get("subtopics") or []:
                matched_subtopics.append((1, topic, subtopic))

    matched_subtopics.sort(key=lambda item: item[0], reverse=True)

    seen: set[str] = set()
    results: list[Any] = []
    for _, topic, subtopic in matched_subtopics[:5]:
        topic_preferred = topic.get("preferred_venues") or preferred_venues
        topic_fallback = topic.get("fallback_venues") or fallback_venues
        subtopic_results, subtopic_notes = discover_for_subtopic(
            topic_name=topic.get("name") or topic.get("id") or "Unknown Topic",
            subtopic=subtopic,
            preferred_venues=topic_preferred,
            fallback_venues=topic_fallback,
            min_year=min_year,
            limit=max(limit * 2, 6),
        )
        notes.extend(f"{subtopic.get('id')}: {note}" for note in subtopic_notes)
        for result in subtopic_results:
            title_key = result.title.strip().lower()
            if title_key in seen:
                continue
            seen.add(title_key)
            bonus = 0
            lowered_title = _normalize_text(result.title)
            lowered_query = _normalize_text(query)
            lowered_abstract = _normalize_text(result.abstract or "")
            if lowered_query and lowered_query in lowered_title:
                bonus += 40
            if any(_normalize_text(keyword) in lowered_title for keyword in keywords):
                bonus += 24
            if any(_normalize_text(keyword) in lowered_abstract for keyword in keywords):
                bonus += 12
            if topic_overlap.get(topic.get("id") or "", 0) > 0:
                bonus += 20
            result.score += bonus
            results.append(result)
        if len(results) >= limit * 3:
            break

    results.sort(key=lambda item: (item.score, item.year or 0), reverse=True)
    return results[:limit], notes
