from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from shared.obsidian.note_search import has_probable_duplicate, search_vault_notes
from shared.search.discovery import discover_for_query
from shared.search.paper_search import (
    PAPERQUAY_DATA_DIR,
    describe_pdf_access,
    download_pdf,
    is_probably_downloadable_paper_url,
    resolve_pdf_url,
)
from shared.search.taxonomy import load_taxonomy


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
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--download-pdf", action="store_true")
    args = parser.parse_args()

    finder_config = load_taxonomy(args.config)
    taxonomy = load_taxonomy(args.taxonomy)
    min_year = datetime.now().year - int(finder_config.get("recent_years") or 3) + 1
    preferred = []
    fallback = []
    topics = taxonomy.get("topics", [])
    for topic in topics:
        preferred.extend(topic.get("preferred_venues") or [])
        fallback.extend(topic.get("fallback_venues") or [])
    recovery_notes: list[str] = []
    try:
        results_rows, fallback_status = discover_for_query(
            query=args.query,
            topics=topics,
            preferred_venues=preferred,
            fallback_venues=fallback,
            min_year=min_year,
            limit=args.limit,
        )
        recovery_notes = fallback_status
        error = fallback_status[0] if len(fallback_status) == 1 else None
    except RuntimeError as exc:
        results_rows, error = [], str(exc)
    results: list[dict] = []

    topic_names = [topic.get("name") for topic in taxonomy.get("topics", [])]
    for row in results_rows:
        title = row.title
        pdf_url = row.pdf_url
        if not pdf_url and is_probably_downloadable_paper_url(row.url):
            pdf_url = resolve_pdf_url(row.url)
        pdf_download = None
        if args.download_pdf and pdf_url:
            try:
                pdf_download = str(download_pdf(pdf_url, PAPERQUAY_DATA_DIR, title))
            except Exception as exc:
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
        if duplicate:
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

    print(
        json.dumps(
            {
                "status": "success",
                "query": args.query,
                "year_floor": min_year,
                "error": error,
                "paperquay_data_dir": str(PAPERQUAY_DATA_DIR),
                "taxonomy_topics": topic_names,
                "recovery": recovery_notes if recovery_notes else ([] if error is None else [error]),
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
