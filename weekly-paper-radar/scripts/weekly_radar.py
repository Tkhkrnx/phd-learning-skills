from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from shared.obsidian.note_search import has_probable_duplicate, search_vault_notes
from shared.search.discovery import discover_for_subtopic
from shared.search.paper_search import (
    PAPERQUAY_DATA_DIR,
    describe_pdf_access,
    download_pdf,
    is_probably_downloadable_paper_url,
    resolve_pdf_url,
)
from shared.search.taxonomy import load_taxonomy


def normalize_title(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def rank_candidate_dicts(candidates: list[dict]) -> list[dict]:
    venue_counts: dict[str, int] = {}
    subtopic_counts: dict[str, int] = {}
    ranked: list[dict] = []

    def sort_key(item: dict) -> tuple:
        bucket_rank = 0 if item.get("bucket") == "preferred" else 1
        duplicate_penalty = 1 if item.get("duplicate_in_vault") else 0
        venue = item.get("venue") or ""
        subtopic = item.get("subtopic_id") or ""
        year = item.get("year") or 0
        title = item.get("title") or ""
        return (
            bucket_rank,
            duplicate_penalty,
            -year,
            title,
        )

    remaining = sorted(candidates, key=sort_key)
    while remaining:
        best_index = 0
        best_score: tuple | None = None
        for index, item in enumerate(remaining):
            venue = item.get("venue") or ""
            subtopic = item.get("subtopic_id") or ""
            fairness = (
                venue_counts.get(venue, 0),
                subtopic_counts.get(subtopic, 0),
                0 if item.get("bucket") == "preferred" else 1,
                -(item.get("year") or 0),
                item.get("title") or "",
            )
            if best_score is None or fairness < best_score:
                best_index = index
                best_score = fairness
        chosen = remaining.pop(best_index)
        venue_counts[chosen.get("venue") or ""] = venue_counts.get(chosen.get("venue") or "", 0) + 1
        subtopic_counts[chosen.get("subtopic_id") or ""] = subtopic_counts.get(chosen.get("subtopic_id") or "", 0) + 1
        ranked.append(chosen)
    return ranked


def summarize_pdf_status(topic_reports: list[dict]) -> dict:
    summary = {
        "total_candidates": 0,
        "auto_download_succeeded": 0,
        "auto_downloadable_but_not_downloaded": 0,
        "manual_search_needed": 0,
        "publisher_blocked_or_login_required": 0,
        "listing_page_only": 0,
        "pdf_not_found_manual_search_needed": 0,
        "download_failed": 0,
    }
    for topic in topic_reports:
        for paper in topic.get("papers", []):
            summary["total_candidates"] += 1
            access = paper.get("pdf_access") or {}
            if access.get("auto_download_succeeded"):
                summary["auto_download_succeeded"] += 1
            elif access.get("auto_downloadable"):
                summary["auto_downloadable_but_not_downloaded"] += 1
            if access.get("manual_search_needed"):
                summary["manual_search_needed"] += 1
            reason = access.get("reason")
            if reason in summary:
                summary[reason] += 1
    return summary


def build_manual_followup_queue(topic_reports: list[dict]) -> list[dict]:
    queue: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for topic in topic_reports:
        topic_name = topic.get("topic_name")
        for paper in topic.get("papers", []):
            access = paper.get("pdf_access") or {}
            if not access.get("manual_search_needed"):
                continue
            reason = access.get("reason") or "manual_search_needed"
            key = ((paper.get("title") or "").strip().lower(), reason)
            if key in seen:
                continue
            seen.add(key)
            queue.append(
                {
                    "title": paper.get("title"),
                    "venue": paper.get("venue"),
                    "year": paper.get("year"),
                    "topic": topic_name,
                    "subtopic_id": paper.get("subtopic_id"),
                    "reason": reason,
                    "doi_url": access.get("doi_url"),
                    "official_url": access.get("official_url"),
                    "pdf_url": access.get("pdf_url"),
                    "authors": paper.get("authors") or [],
                }
            )
    return queue


def build_download_summary(*, paperquay_data_dir: Path, topic_reports: list[dict], manual_followup: list[dict]) -> dict:
    downloaded_files: list[dict] = []
    for topic in topic_reports:
        for paper in topic.get("papers", []):
            pdf_download = paper.get("pdf_download")
            if (
                isinstance(pdf_download, str)
                and pdf_download
                and not pdf_download.startswith("download_failed:")
                and pdf_download != "pdf_not_found_manual_search_needed"
            ):
                downloaded_files.append(
                    {
                        "title": paper.get("title"),
                        "venue": paper.get("venue"),
                        "year": paper.get("year"),
                        "topic": topic.get("topic_name"),
                        "file_path": pdf_download,
                    }
                )
    return {
        "paperquay_data_dir": str(paperquay_data_dir),
        "downloaded_count": len(downloaded_files),
        "downloaded_files": downloaded_files,
        "manual_followup_count": len(manual_followup),
        "manual_followup": manual_followup,
    }




def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except OSError:
            pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(Path(__file__).resolve().parents[1] / "radar_config.yaml"))
    parser.add_argument("--candidate-pool-total", type=int, default=20)
    parser.add_argument("--weekly-target", type=int, default=10)
    parser.add_argument("--deep-read-target", type=int, default=4)
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1] / "outputs"))
    parser.add_argument("--download-pdf", action="store_true")
    args = parser.parse_args()

    taxonomy = load_taxonomy(args.config)
    current_year = datetime.now().year
    min_year = current_year - 2
    topic_reports: list[dict] = []
    used_titles_global: set[str] = set()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for topic in taxonomy.get("topics", []):
        preferred = topic.get("preferred_venues") or []
        fallback = topic.get("fallback_venues") or []
        collected: list[dict] = []
        topic_error = None
        topic_fallbacks: list[str] = []
        duplicate_skips: list[str] = []
        used_venues: set[str] = set()
        used_subtopics: set[str] = set()
        deferred_candidates: list[dict] = []
        topic_target = max(1, args.candidate_pool_total // max(len(taxonomy.get("topics", [])), 1))
        if topic.get("id") == (taxonomy.get("topics", [])[-1].get("id") if taxonomy.get("topics") else None):
            assigned_so_far = topic_target * max(len(taxonomy.get("topics", [])) - 1, 0)
            topic_target = max(1, args.candidate_pool_total - assigned_so_far)
        for subtopic in topic.get("subtopics") or []:
            try:
                results, recovery_notes = discover_for_subtopic(
                    topic_name=topic.get("name") or topic.get("id") or "Unknown Topic",
                    subtopic=subtopic,
                    preferred_venues=preferred,
                    fallback_venues=fallback,
                    min_year=min_year,
                    limit=max(topic_target * 2, 8),
                )
                topic_fallbacks.extend(f"{subtopic.get('id')}: {note}" for note in recovery_notes)
            except RuntimeError as exc:
                topic_error = str(exc)
                break
            ranked_results = sorted(
                results,
                key=lambda item: (
                    item.venue in used_venues,
                    item.subtopic_id in used_subtopics,
                    -(item.year or 0),
                    -item.score,
                ),
            )
            for result in ranked_results:
                title_key = normalize_title(result.title)
                if title_key in used_titles_global:
                    duplicate_skips.append(result.title)
                    continue
                if any(normalize_title(existing["title"]) == title_key for existing in collected):
                    continue
                vault_hits = search_vault_notes(query=result.title, limit=5)
                duplicate = has_probable_duplicate(result.title, vault_hits)
                if duplicate:
                    duplicate_skips.append(result.title)
                    continue
                pdf_download = None
                resolved_pdf_url = result.pdf_url
                if not resolved_pdf_url and is_probably_downloadable_paper_url(result.url):
                    resolved_pdf_url = resolve_pdf_url(result.url)
                if args.download_pdf and resolved_pdf_url:
                    try:
                        pdf_download = str(download_pdf(resolved_pdf_url, PAPERQUAY_DATA_DIR, result.title))
                    except Exception as exc:
                        pdf_download = f"download_failed: {exc}"
                elif args.download_pdf and not resolved_pdf_url:
                    pdf_download = "pdf_not_found_manual_search_needed"
                candidate = {
                    "title": result.title,
                    "year": result.year,
                    "venue": result.venue,
                    "bucket": result.bucket,
                    "subtopic_id": result.subtopic_id,
                    "paper_id": result.paper_id,
                    "authors": result.authors,
                    "pdf_url": resolved_pdf_url,
                    "pdf_download": pdf_download,
                    "url": result.url,
                    "downloadable_url": is_probably_downloadable_paper_url(result.url),
                    "abstract": result.abstract,
                    "vault_hits": vault_hits,
                    "duplicate_in_vault": duplicate,
                    "external_ids": result.source.get("externalIds") or {},
                    "publication_url": result.source.get("publicationUrl"),
                }
                candidate["pdf_access"] = describe_pdf_access(
                    url=candidate.get("publication_url") or candidate.get("url"),
                    pdf_url=resolved_pdf_url,
                    pdf_download=pdf_download,
                )
                if result.venue in used_venues and result.subtopic_id in used_subtopics:
                    deferred_candidates.append(candidate)
                    continue
                collected.append(candidate)
                used_titles_global.add(title_key)
                used_venues.add(result.venue)
                used_subtopics.add(result.subtopic_id)
                if len(collected) >= topic_target:
                    break
            if len(collected) >= topic_target:
                break

        if len(collected) < topic_target and deferred_candidates:
            for candidate in rank_candidate_dicts(deferred_candidates):
                if len(collected) >= topic_target:
                    break
                if any(normalize_title(existing["title"]) == normalize_title(candidate["title"]) for existing in collected):
                    continue
                collected.append(candidate)

        collected = rank_candidate_dicts(collected)

        topic_reports.append(
            {
                "topic_id": topic.get("id"),
                "topic_name": topic.get("name"),
                "requested_count": topic_target,
                "actual_count": len(collected),
                "error": topic_error,
                "recovery": topic_fallbacks,
                "duplicate_skips": duplicate_skips,
                "papers": collected,
            }
        )

    generated_at = datetime.now().isoformat()
    candidate_pool = {
        "status": "success",
        "generated_at": generated_at,
        "year_range": [min_year, current_year],
        "paperquay_data_dir": str(PAPERQUAY_DATA_DIR),
        "candidate_pool_total": args.candidate_pool_total,
        "weekly_target": args.weekly_target,
        "deep_read_target": args.deep_read_target,
        "pdf_status_summary": summarize_pdf_status(topic_reports),
        "topics": topic_reports,
    }
    candidate_pool_path = output_dir / "candidate_pool.json"
    candidate_pool_path.write_text(json.dumps(candidate_pool, ensure_ascii=False, indent=2), encoding="utf-8")

    manual_followup_queue = build_manual_followup_queue(topic_reports)
    manual_followup_path = output_dir / "manual_pdf_followup.json"
    manual_followup_path.write_text(json.dumps(manual_followup_queue, ensure_ascii=False, indent=2), encoding="utf-8")
    download_summary = build_download_summary(
        paperquay_data_dir=PAPERQUAY_DATA_DIR,
        topic_reports=topic_reports,
        manual_followup=manual_followup_queue,
    )

    print(
        json.dumps(
            {
                **candidate_pool,
                "candidate_pool_path": str(candidate_pool_path),
                "manual_pdf_followup_path": str(manual_followup_path),
                "download_summary": download_summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
