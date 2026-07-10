from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from shared.search.paper_search import (
    is_source_on_cooldown,
    make_session,
    mark_source_cooldown,
    read_cache,
    write_cache,
)
from shared.search.taxonomy import load_taxonomy

OFFICIAL_SOURCE_CONFIG = Path(__file__).resolve().parent / "official_sources.yaml"


def _strip_tags(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _clean_title(text: str) -> str:
    text = _strip_tags(text)
    text = re.sub(r"^\d+\s*[\.\)]\s*", "", text)
    return text.strip(" -:|")


def _looks_like_paper_title(title: str) -> bool:
    if not title:
        return False
    lowered = title.lower()
    if len(title) < 12:
        return False
    blocked = [
        "accepted papers",
        "technical sessions",
        "call for papers",
        "home",
        "program",
        "registration",
        "authors",
        "schedule",
        "sponsors",
        "organizers",
        "session",
        "workshop",
        "tutorial",
        "poster session",
        "keynote",
        "organizing committee",
        "student travel grants",
        "camera-ready instructions",
        "registration",
        "business meeting",
        "conference overview",
        "program brochure",
        "plenary poster sessions",
        "program overview",
    ]
    if any(token == lowered or lowered.startswith(f"{token} ") for token in blocked):
        return False
    if title.count(" ") < 2:
        return False
    return True


def _extract_year_from_url(url: str) -> int | None:
    match = re.search(r"(20\d{2})", url)
    return int(match.group(1)) if match else None


def _source_key(source: dict[str, Any]) -> str:
    venue = str(source.get("venue") or "unknown").strip().lower().replace(" ", "-")
    year = source.get("year") or _extract_year_from_url(str(source.get("url") or "")) or "unknown"
    adapter = str(source.get("adapter") or "unknown").strip().lower()
    url = str(source.get("url") or "").strip().lower()
    url_key = re.sub(r"[^a-z0-9]+", "-", url).strip("-")[:80]
    return f"official:{venue}:{year}:{adapter}:{url_key}"


def _fetch_html(url: str, source_key: str) -> str:
    session = make_session()
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as exc:
        mark_source_cooldown(source_key)
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status in {401, 403}:
            raise RuntimeError(f"official_source_forbidden:{url}:{status}") from exc
        raise RuntimeError(f"official_source_request_failed: {url}: {exc}") from exc


def _parse_link_pairs(html_text: str, base_url: str) -> list[tuple[str, str]]:
    matches = re.findall(r"<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html_text, flags=re.I | re.S)
    pairs: list[tuple[str, str]] = []
    for href, inner in matches:
        title = _clean_title(inner)
        if not _looks_like_paper_title(title):
            continue
        pairs.append((title, urljoin(base_url, href)))
    return pairs


def _parse_eurosys_papers(html_text: str, base_url: str) -> list[dict[str, Any]]:
    rows = re.findall(r"<tr>([\s\S]*?)</tr>", html_text, flags=re.I)
    results: list[dict[str, Any]] = []
    for row in rows:
        cols = re.findall(r"<td[^>]*>([\s\S]*?)</td>", row, flags=re.I)
        if len(cols) < 2:
            continue
        title_links = _parse_link_pairs(cols[0], base_url)
        if not title_links:
            continue
        title, url = title_links[0]
        authors = [part.strip() for part in _strip_tags(cols[1]).split(",") if part.strip()]
        results.append({"title": title, "url": url, "authors": authors})
    return results


def _parse_usenix_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, url in _parse_link_pairs(html_text, base_url):
        lowered_url = url.lower()
        if "/presentation/" not in lowered_url and "/conference/" not in lowered_url and "/node/" not in lowered_url:
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": url, "authors": []})
    return results


def _parse_sigops_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, url in _parse_link_pairs(html_text, base_url):
        if "doi.org" not in url and "dl.acm.org" not in url and not url.lower().endswith(".pdf"):
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": url, "authors": []})
    return results


def _parse_acm_dl_proceedings(html_text: str, base_url: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, url in _parse_link_pairs(html_text, base_url):
        lowered_url = url.lower()
        if "/doi/" not in lowered_url:
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": url, "authors": []})
    return results


def _parse_simple_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, url in _parse_link_pairs(html_text, base_url):
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": url, "authors": []})
    return results


def _extract_doi_from_text(text: str) -> str | None:
    match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", text, flags=re.I)
    return match.group(0) if match else None


def _parse_researchr_modal_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    row_matches = re.findall(
        r"<tr[^>]+class=\"hidable\"[^>]*>([\s\S]*?)</tr>",
        html_text,
        flags=re.I,
    )
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in row_matches:
        title_match = re.search(
            r'data-event-modal="[^"]+">([\s\S]*?)</a></strong>',
            row,
            flags=re.I,
        )
        if not title_match:
            continue
        title = _clean_title(title_match.group(1))
        if not _looks_like_paper_title(title):
            continue
        authors = [
            _clean_title(match)
            for match in re.findall(r'<a[^>]+class="navigate"[^>]*>([\s\S]*?)</a>', row, flags=re.I)
            if _clean_title(match)
        ]
        link_match = re.search(r'<a[^>]+class="publication-link[^"]*"[^>]+href="([^"]+)"', row, flags=re.I)
        publication_url = urljoin(base_url, link_match.group(1)) if link_match else None
        doi = _extract_doi_from_text(row)
        url = publication_url or (f"https://doi.org/{doi}" if doi else base_url)
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        external_ids = {"DOI": doi} if doi else {}
        results.append(
            {
                "title": title,
                "url": url,
                "authors": authors,
                "externalIds": external_ids,
                "publicationUrl": publication_url,
            }
        )
    return results


def _parse_wordpress_program_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    return _parse_panel_schedule_titles(html_text, base_url)


def _parse_ieee_program_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    panel_results = _parse_panel_schedule_titles(html_text, base_url)
    if panel_results:
        return panel_results
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, url in _parse_link_pairs(html_text, base_url):
        lowered_url = url.lower()
        if not any(token in lowered_url for token in ["/program/", "/session", "/paper", "/presentation/", "/main-program/"]):
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": url, "authors": []})
    return results


def _parse_mlsys_virtual_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, url in _parse_link_pairs(html_text, base_url):
        lowered_url = url.lower()
        if not any(token in lowered_url for token in ["/virtual/", "/poster/", "/talk/", "/paper/"]):
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": url, "authors": []})
    return results


def _parse_socc_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    matches = re.findall(r"<h4[^>]*>\s*<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>([\s\S]*?)</a>\s*</h4>", html_text, flags=re.I)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for href, inner in matches:
        title = _clean_title(inner)
        if not _looks_like_paper_title(title):
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": urljoin(base_url, href), "authors": []})
    if results:
        return results
    return _parse_simple_titles(html_text, base_url)


def _parse_vldb_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    next_data_match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>',
        html_text,
        flags=re.I,
    )
    if not next_data_match:
        return _parse_simple_titles(html_text, base_url)
    try:
        import json

        payload = json.loads(next_data_match.group(1))
    except Exception:
        return _parse_simple_titles(html_text, base_url)
    page_props = ((payload.get("props") or {}).get("pageProps") or {})
    grouped_issues = page_props.get("groupedIssues") or {}
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for issue_rows in grouped_issues.values():
        if not isinstance(issue_rows, list):
            continue
        for row in issue_rows:
            if not isinstance(row, dict):
                continue
            title = _clean_title(str(row.get("title") or ""))
            if not _looks_like_paper_title(title):
                continue
            key = title.lower()
            if key in seen:
                continue
            seen.add(key)
            authors = [part.strip() for part in str(row.get("authors") or "").split(",") if part.strip()]
            pdf_url = urljoin(base_url, str(row.get("pdf") or "").strip()) if row.get("pdf") else base_url
            results.append({"title": title, "url": pdf_url, "authors": authors})
    return results


def _parse_panel_schedule_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    paper_blocks = re.findall(
        r'<div class="paper">([\s\S]*?)</div>\s*(?:<hr[^>]*>\s*)?(?=<div class="paper">|</div>\s*</div>\s*</div>)',
        html_text,
        flags=re.I,
    )
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for block in paper_blocks:
        title_match = re.search(r'<div class="paper-title">\s*([\s\S]*?)\s*</div>', block, flags=re.I)
        if not title_match:
            continue
        title = _clean_title(title_match.group(1))
        if not _looks_like_paper_title(title):
            continue
        authors_match = re.search(r'<div class="paper-authors">\s*([\s\S]*?)\s*</div>', block, flags=re.I)
        authors_text = _strip_tags(authors_match.group(1)) if authors_match else ""
        authors = [part.strip() for part in re.split(r";|,(?=\s*[A-Z])", authors_text) if part.strip()]
        link_match = re.search(r'<a[^>]+class="publication-link[^"]*"[^>]+href="([^"]+)"', block, flags=re.I)
        publication_url = urljoin(base_url, link_match.group(1)) if link_match else None
        doi = _extract_doi_from_text(block)
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        external_ids = {"DOI": doi} if doi else {}
        results.append(
            {
                "title": title,
                "url": publication_url or (f"https://doi.org/{doi}" if doi else base_url),
                "authors": authors,
                "externalIds": external_ids,
                "publicationUrl": publication_url,
            }
        )
    return results


def _parse_sigmod_accepted_titles(html_text: str, base_url: str) -> list[dict[str, Any]]:
    rows = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", html_text, flags=re.I)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        cols = re.findall(r"<td[^>]*>([\s\S]*?)</td>", row, flags=re.I)
        if not cols:
            continue
        cleaned_cols = [_clean_title(col) for col in cols]
        title = next((col for col in cleaned_cols if _looks_like_paper_title(col)), "")
        if not title:
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": base_url, "authors": []})
    return results


ADAPTERS = {
    "sigops_accepted_list": _parse_sigops_titles,
    "usenix_technical_sessions": _parse_usenix_titles,
    "usenix_accepted_papers": _parse_usenix_titles,
    "eurosys_papers": _parse_eurosys_papers,
    "acm_dl_proceedings": _parse_acm_dl_proceedings,
    "simple_title_authors_page": _parse_simple_titles,
    "researchr_track": _parse_researchr_modal_titles,
    "sc_papers": _parse_simple_titles,
    "socc_titles": _parse_socc_titles,
    "vldb_titles": _parse_vldb_titles,
    "wordpress_program": _parse_wordpress_program_titles,
    "ieee_program": _parse_ieee_program_titles,
    "mlsys_virtual": _parse_mlsys_virtual_titles,
    "sigmod_accepted": _parse_sigmod_accepted_titles,
}


def load_official_sources() -> list[dict[str, Any]]:
    config = load_taxonomy(OFFICIAL_SOURCE_CONFIG)
    return config.get("sources") or []


def _title_matches_keywords(title: str, keywords: list[str]) -> bool:
    return _row_match_score(title, keywords) >= 18


def _row_match_score(title: str, keywords: list[str]) -> int:
    lowered_title = title.lower()
    normalized_title = re.sub(r"[^a-z0-9]+", " ", lowered_title)
    title_tokens = {token for token in normalized_title.split() if len(token) >= 3}
    score = 0
    for keyword in keywords:
        normalized = keyword.strip().lower()
        if not normalized:
            continue
        if normalized in lowered_title:
            score += 20 if " " in normalized else 10
            continue
        keyword_tokens = [token for token in re.sub(r"[^a-z0-9]+", " ", normalized).split() if len(token) >= 3]
        overlap = sum(1 for token in keyword_tokens if token in title_tokens)
        if overlap >= 2:
            score += 16
        elif overlap == 1 and len(keyword_tokens) == 1:
            score += 6
    return score


def search_official_sources_for_subtopic(
    subtopic: dict[str, Any],
    preferred_venues: list[str],
    fallback_venues: list[str],
    min_year: int,
    limit: int = 8,
) -> tuple[list[dict[str, Any]], list[str]]:
    keywords = (
        list(subtopic.get("keywords") or [])
        + list(subtopic.get("aliases") or [])
        + [subtopic.get("name") or ""]
    )
    notes: list[str] = []
    collected: list[dict[str, Any]] = []
    seen_titles: set[str] = set()

    for source in load_official_sources():
        year = source.get("year")
        venue = source.get("venue") or "Unknown Venue"
        if isinstance(year, int) and year < min_year:
            continue
        if venue not in preferred_venues and venue not in fallback_venues:
            continue
        source_topics = source.get("topics") or []
        if source_topics and subtopic.get("id") not in source_topics:
            continue
        source_key = _source_key(source)
        cache_key_query = "__all__"
        cached = read_cache(source_key, cache_key_query, 500, min_year)
        if cached is not None:
            rows = cached
        else:
            if is_source_on_cooldown(source_key):
                notes.append(f"{venue}: official_source_on_cooldown")
                continue
            adapter_name = source.get("adapter")
            adapter = ADAPTERS.get(adapter_name)
            if adapter is None:
                notes.append(f"{venue}: missing_adapter:{adapter_name}")
                continue
            try:
                html_text = _fetch_html(source["url"], source_key)
                rows = adapter(html_text, source["url"])
                write_cache(source_key, cache_key_query, 500, min_year, rows)
            except Exception as exc:
                notes.append(f"{venue}: {exc}")
                continue
        ranked_rows = sorted(
            rows,
            key=lambda row: _row_match_score(row.get("title") or "", keywords),
            reverse=True,
        )
        for row in ranked_rows:
            title = row.get("title") or ""
            if not _title_matches_keywords(title, keywords):
                continue
            key = title.lower().strip()
            if key in seen_titles:
                continue
            seen_titles.add(key)
            collected.append(
                {
                    "title": title,
                    "year": year,
                    "venue": venue,
                    "paperId": row.get("paperId"),
                    "url": row.get("url"),
                    "abstract": row.get("abstract"),
                    "authors": row.get("authors") or [],
                    "externalIds": row.get("externalIds") or {},
                    "openAccessPdf": row.get("openAccessPdf") or {},
                    "publicationUrl": row.get("publicationUrl"),
                }
            )
            if len(collected) >= limit:
                return collected, notes
    return collected, notes
