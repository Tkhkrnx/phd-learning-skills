from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[2]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from shared.obsidian.note_search import has_probable_duplicate, search_vault_notes
from shared.search.discovery import discover_for_query, discover_open_query
from shared.search.paper_search import (
    PAPERQUAY_DATA_DIR,
    describe_pdf_access,
    download_pdf,
    is_probably_downloadable_paper_url,
    resolve_pdf_url,
)
from shared.search.taxonomy import load_taxonomy


SEARCH_MODES = ("study", "problem-boundary", "mechanism-inspiration")


def resolve_search_policy(
    *,
    mode: str,
    recent_years: int,
    min_year: int | None,
    current_year: int | None = None,
) -> dict[str, Any]:
    if mode not in SEARCH_MODES:
        raise ValueError(f"unsupported search mode: {mode}")
    year = current_year or datetime.now().year
    effective_min_year = min_year
    year_policy = "explicit" if min_year is not None else "open"
    if effective_min_year is None and mode == "study":
        effective_min_year = year - recent_years + 1
        year_policy = f"recent-{recent_years}-years"
    return {
        "mode": mode,
        "min_year": effective_min_year,
        "year_policy": year_policy,
        "taxonomy_filter": mode == "study",
        "venue_filter": mode == "study",
        "vault_duplicate_policy": "skip" if mode == "study" else "retain-and-annotate",
        "source_scope": "academic candidate discovery; decisive claims still require primary-source inspection",
    }


def _result_key(row: Any) -> str:
    title = re.sub(
        r"[^\w\s]+",
        " ",
        str(getattr(row, "title", "") or "").strip().lower(),
        flags=re.UNICODE,
    )
    if title:
        return f"title:{' '.join(title.split())}"
    paper_id = str(getattr(row, "paper_id", "") or "").strip().lower()
    if paper_id:
        return f"paper:{paper_id}"
    return f"url:{str(getattr(row, 'url', '') or '').strip().lower()}"


def merge_query_results(query_results: list[tuple[str, list[Any]]], limit: int) -> list[tuple[Any, list[str]]]:
    best_by_key: dict[str, Any] = {}
    matched_queries: dict[str, list[str]] = {}
    query_matches: dict[str, dict[str, dict[str, Any]]] = {}
    for query, rows in query_results:
        for row in rows:
            key = _result_key(row)
            if query not in matched_queries.setdefault(key, []):
                matched_queries[key].append(query)
            source = getattr(row, "source", {}) or {}
            query_matches.setdefault(key, {})[query] = source.get("queryMatch") or {}
            existing = best_by_key.get(key)
            if existing is None or getattr(row, "score", 0) > getattr(existing, "score", 0):
                best_by_key[key] = row
    ranked = sorted(
        best_by_key.items(),
        key=lambda item: (getattr(item[1], "score", 0), getattr(item[1], "year", 0) or 0),
        reverse=True,
    )
    merged_results: list[tuple[Any, list[str]]] = []
    for key, row in ranked[:limit]:
        source = getattr(row, "source", None)
        if isinstance(source, dict):
            source["queryMatches"] = query_matches[key]
        merged_results.append((row, matched_queries[key]))
    return merged_results


def build_download_summary(*, paperquay_data_dir: Path, results: list[dict], manual_followup: list[dict]) -> dict:
    downloaded_files = [
        {
            "title": item["title"],
            "venue": item["venue"],
            "year": item["year"],
            "file_path": item["pdf_download"],
        }
        for item in results
        if isinstance(item.get("pdf_download"), str)
        and item["pdf_download"]
        and not item["pdf_download"].startswith("download_failed:")
        and item["pdf_download"] != "pdf_not_found_manual_search_needed"
    ]
    return {
        "paperquay_data_dir": str(paperquay_data_dir),
        "downloaded_count": len(downloaded_files),
        "downloaded_files": downloaded_files,
        "manual_followup_count": len(manual_followup),
        "manual_followup": manual_followup,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(Path(__file__).resolve().parents[1] / "finder_config.yaml"))
    parser.add_argument("--taxonomy", default=str(Path(__file__).resolve().parents[2] / "weekly-paper-radar" / "radar_config.yaml"))
    parser.add_argument("--mode", choices=SEARCH_MODES)
    parser.add_argument("--query", action="append", required=True, help="Repeat to supply a query portfolio.")
    parser.add_argument("--min-year", type=int)
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--download-pdf", action="store_true")
    args = parser.parse_args()

    finder_config = load_taxonomy(args.config)
    mode = args.mode or str(finder_config.get("default_mode") or "study")
    policy = resolve_search_policy(
        mode=mode,
        recent_years=int(finder_config.get("recent_years") or 3),
        min_year=args.min_year,
    )
    taxonomy = load_taxonomy(args.taxonomy) if policy["taxonomy_filter"] else {"topics": []}
    topics = taxonomy.get("topics", [])
    preferred = [venue for topic in topics for venue in (topic.get("preferred_venues") or [])]
    fallback = [venue for topic in topics for venue in (topic.get("fallback_venues") or [])]

    query_results: list[tuple[str, list[Any]]] = []
    recovery_notes: list[str] = []
    query_errors: list[str] = []
    per_query_limit = max(args.limit * 2, 8)
    for query in args.query:
        try:
            if mode == "study":
                rows, notes = discover_for_query(
                    query=query,
                    topics=topics,
                    preferred_venues=preferred,
                    fallback_venues=fallback,
                    min_year=int(policy["min_year"]),
                    limit=per_query_limit,
                )
            else:
                rows, notes = discover_open_query(
                    query=query,
                    min_year=policy["min_year"],
                    limit=per_query_limit,
                    evidence_mode=mode,
                )
            query_results.append((query, rows))
            recovery_notes.extend(f"{query}: {note}" for note in notes)
        except RuntimeError as exc:
            query_errors.append(f"{query}: {exc}")

    ranked_rows = merge_query_results(query_results, args.limit)
    results: list[dict] = []
    for row, matched_queries in ranked_rows:
        title = row.title
        pdf_url = row.pdf_url
        if not pdf_url and is_probably_downloadable_paper_url(row.url):
            pdf_url = resolve_pdf_url(row.url)
        pdf_download = None
        if args.download_pdf and pdf_url:
            try:
                pdf_download = str(download_pdf(pdf_url, PAPERQUAY_DATA_DIR, title))
            except Exception as exc:  # noqa: BLE001 - expose per-paper download failure in JSON
                pdf_download = f"download_failed: {exc}"
        elif args.download_pdf and not pdf_url:
            pdf_download = "pdf_not_found_manual_search_needed"
        results.append(
            {
                "title": title,
                "year": row.year,
                "venue": row.venue,
                "paper_id": row.paper_id,
                "url": row.url,
                "pdf_url": pdf_url,
                "pdf_download": pdf_download,
                "authors": row.authors,
                "abstract": row.abstract,
                "matched_queries": matched_queries,
                "discovery_sources": row.source.get("discoverySources") or [],
                "query_matches": row.source.get("queryMatches") or {},
                "vault_hits": search_vault_notes(query=title, limit=5),
                "external_ids": row.source.get("externalIds") or {},
                "publication_url": row.source.get("publicationUrl"),
            }
        )

    filtered_results: list[dict] = []
    duplicate_skips: list[str] = []
    for item in results:
        duplicate = has_probable_duplicate(item["title"], item["vault_hits"])
        item["duplicate_in_vault"] = duplicate
        if duplicate and policy["vault_duplicate_policy"] == "skip":
            duplicate_skips.append(item["title"])
            continue
        item["pdf_access"] = describe_pdf_access(
            url=item.get("publication_url") or item.get("url"),
            pdf_url=item.get("pdf_url"),
            pdf_download=item.get("pdf_download"),
        )
        filtered_results.append(item)

    manual_followup = [
        {
            "title": item["title"],
            "venue": item["venue"],
            "year": item["year"],
            "reason": item["pdf_access"].get("reason"),
            "doi_url": item["pdf_access"].get("doi_url"),
            "official_url": item["pdf_access"].get("official_url"),
            "pdf_url": item["pdf_access"].get("pdf_url"),
        }
        for item in filtered_results
        if item.get("pdf_access", {}).get("manual_search_needed")
    ]
    download_summary = build_download_summary(
        paperquay_data_dir=PAPERQUAY_DATA_DIR,
        results=filtered_results,
        manual_followup=manual_followup,
    )
    error = "; ".join(query_errors) or None
    coverage_status = (
        "partial_index_coverage"
        if query_errors or any(":failed:" in note for note in recovery_notes)
        else "configured_indexes_reached"
    )
    status = "success"
    if query_errors and not filtered_results:
        status = "search_failed"
    elif not filtered_results:
        status = "no_candidates"
    print(
        json.dumps(
            {
                "status": status,
                "mode": mode,
                "query": args.query[0] if len(args.query) == 1 else args.query,
                "queries": args.query,
                "search_policy": policy,
                "coverage_status": coverage_status,
                "year_floor": policy["min_year"],
                "error": error,
                "paperquay_data_dir": str(PAPERQUAY_DATA_DIR),
                "taxonomy_topics": [topic.get("name") for topic in topics],
                "recovery": recovery_notes + query_errors,
                "duplicate_skips": duplicate_skips,
                "download_summary": download_summary,
                "manual_pdf_followup": manual_followup,
                "results": filtered_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
