from __future__ import annotations

import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urljoin, urlparse

import requests
from requests import HTTPError

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
ARXIV_API = "https://export.arxiv.org/api/query"
OPENALEX_API = "https://api.openalex.org/works"
DBLP_API = "https://dblp.org/search/publ/api"
DEFAULT_SUBMISSION_DIR = Path.home() / "Documents" / "PHR" / "Intellistream" / "papers" / "read"

def _paperquay_data_dir() -> Path:
    configured = os.environ.get("PAPERQUAY_DATA_DIR", "").strip()
    if configured:
        return Path(configured)
    submission_dir = os.environ.get("PHD_PAPER_SUBMISSION_DIR", "").strip()
    if submission_dir:
        return Path(submission_dir)
    paperquay_root = os.environ.get("PAPERQUAY_ROOT", "").strip()
    if paperquay_root:
        return Path(paperquay_root) / "paperquay-data"
    return DEFAULT_SUBMISSION_DIR


PAPERQUAY_DATA_DIR = _paperquay_data_dir()
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
SEARCH_CACHE_DIR = Path(__file__).resolve().parents[2] / ".cache" / "paper-discovery"
SOURCE_COOLDOWN_SECONDS = 600
CACHE_TTL_SECONDS = 60 * 60 * 12
SOURCE_COOLDOWN_UNTIL: dict[str, float] = {}
AGGREGATE_QUERY_BUDGET = 3
PDF_CACHE_DIR = SEARCH_CACHE_DIR / "pdf-resolution"


def env_flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


def make_session(*, trust_env: bool | None = None) -> requests.Session:
    session = requests.Session()
    session.trust_env = env_flag("PAPER_SEARCH_TRUST_ENV", False) if trust_env is None else trust_env
    session.headers.update(
        {
            "User-Agent": "phd-learning-skills/0.1 (+https://github.com/Tkhkrnx/phd-learning-skills)",
            "Accept": "application/json",
        }
    )
    return session


@dataclass
class SearchResult:
    title: str
    year: int | None
    venue: str
    paper_id: str | None
    url: str | None
    abstract: str | None
    authors: list[str]
    pdf_url: str | None
    source: dict[str, Any]
    bucket: str
    subtopic_id: str
    score: int


class SearchRateLimitError(RuntimeError):
    pass


def _cache_key(source: str, query: str, limit: int, min_year: int | None) -> Path:
    payload = f"{source}|{query}|{limit}|{min_year}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return SEARCH_CACHE_DIR / f"{digest}.json"


def read_cache(source: str, query: str, limit: int, min_year: int | None) -> list[dict[str, Any]] | None:
    path = _cache_key(source, query, limit, min_year)
    try:
        if not path.exists():
            return None
        if time.time() - path.stat().st_mtime > CACHE_TTL_SECONDS:
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("rows")
        if isinstance(rows, list):
            return rows
    except (OSError, json.JSONDecodeError):
        return None
    return None


def write_cache(source: str, query: str, limit: int, min_year: int | None, rows: list[dict[str, Any]]) -> None:
    SEARCH_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_key(source, query, limit, min_year)
    path.write_text(json.dumps({"rows": rows}, ensure_ascii=False), encoding="utf-8")


def _pdf_cache_path(url: str) -> Path:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return PDF_CACHE_DIR / f"{digest}.json"


def read_pdf_cache(url: str) -> str | None:
    path = _pdf_cache_path(url)
    try:
        if not path.exists():
            return None
        if time.time() - path.stat().st_mtime > CACHE_TTL_SECONDS:
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        value = payload.get("pdf_url")
        return value if isinstance(value, str) and value else None
    except (OSError, json.JSONDecodeError):
        return None


def write_pdf_cache(url: str, pdf_url: str | None) -> None:
    PDF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _pdf_cache_path(url).write_text(json.dumps({"pdf_url": pdf_url}, ensure_ascii=False), encoding="utf-8")


def is_source_on_cooldown(source: str) -> bool:
    return SOURCE_COOLDOWN_UNTIL.get(source, 0) > time.time()


def mark_source_cooldown(source: str) -> None:
    SOURCE_COOLDOWN_UNTIL[source] = time.time() + SOURCE_COOLDOWN_SECONDS


def unique_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        ordered.append(item.strip())
    return ordered


def normalize_venue(venue: str | None) -> str:
    return (venue or "").strip()


def venue_aliases(name: str) -> list[str]:
    normalized = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
    aliases = [normalized]
    compact = normalized.replace(" ", "")
    if compact != normalized:
        aliases.append(compact)
    words = normalized.split()
    if words:
        aliases.append(" ".join(words))
    return unique_preserve_order([alias for alias in aliases if alias])


def venue_matches(venue: str, venue_name: str) -> bool:
    normalized_venue = re.sub(r"[^a-z0-9]+", " ", (venue or "").lower()).strip()
    compact_venue = normalized_venue.replace(" ", "")
    token_set = set(normalized_venue.split())
    for alias in venue_aliases(venue_name):
        alias_tokens = alias.split()
        if not alias_tokens:
            continue
        if len(alias_tokens) == 1 and len(alias_tokens[0]) <= 4:
            if alias in token_set or alias == compact_venue:
                return True
            continue
        if alias in normalized_venue or alias.replace(" ", "") in compact_venue:
            return True
    return False


def choose_pdf_url(item: dict[str, Any]) -> str | None:
    publication_url = item.get("publicationUrl")
    if isinstance(publication_url, str) and publication_url.lower().endswith(".pdf"):
        return publication_url
    open_access = item.get("openAccessPdf") or {}
    for candidate in [open_access.get("url"), item.get("url")]:
        if isinstance(candidate, str) and candidate.lower().endswith(".pdf"):
            return candidate
    external_ids = item.get("externalIds") or {}
    arxiv_id = external_ids.get("ArXiv")
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return None


def _looks_like_listing_page_url(url: str) -> bool:
    lowered = (url or "").lower()
    listing_tokens = [
        "/program",
        "/programs",
        "/technical-sessions",
        "/accepted",
        "/papers",
        "sigmod_papers",
        "/track/",
        "/sessions",
        "/schedule",
    ]
    return any(token in lowered for token in listing_tokens)


def is_probably_downloadable_paper_url(url: str | None) -> bool:
    if not isinstance(url, str) or not url.strip():
        return False
    lowered = url.strip().lower()
    if lowered.endswith(".pdf") or "/doi/" in lowered or "doi.org/" in lowered:
        return True
    if any(token in lowered for token in ["/presentation/", "/poster/", "/eventlistwithbios/", "/details/"]):
        return True
    return not _looks_like_listing_page_url(lowered)


def extract_doi_url(url: str | None) -> str | None:
    if not isinstance(url, str) or not url.strip():
        return None
    cleaned = url.strip()
    lowered = cleaned.lower()
    if "doi.org/" in lowered:
        return cleaned
    match = re.search(r"/doi/(?:pdf/)?(10\.\d{4,9}/[^/?#]+)", cleaned, flags=re.I)
    if match:
        return f"https://doi.org/{match.group(1)}"
    return None


def describe_pdf_access(*, url: str | None, pdf_url: str | None, pdf_download: str | None) -> dict[str, Any]:
    doi_url = extract_doi_url(url) or extract_doi_url(pdf_url)
    source_url = (url or "").strip()
    pdf_candidate = (pdf_url or "").strip()
    resolved = {
        "auto_downloadable": False,
        "auto_download_succeeded": False,
        "manual_search_needed": False,
        "reason": None,
        "doi_url": doi_url,
        "official_url": source_url or None,
        "pdf_url": pdf_candidate or None,
    }
    if isinstance(pdf_download, str) and pdf_download and not pdf_download.startswith("download_failed:") and pdf_download != "pdf_not_found_manual_search_needed":
        resolved["auto_downloadable"] = True
        resolved["auto_download_succeeded"] = True
        resolved["reason"] = "downloaded"
        return resolved
    if pdf_candidate:
        resolved["auto_downloadable"] = True
        if isinstance(pdf_download, str) and pdf_download.startswith("download_failed:"):
            resolved["manual_search_needed"] = True
            resolved["reason"] = "download_failed"
        else:
            resolved["reason"] = "pdf_url_resolved"
        return resolved
    if doi_url:
        resolved["manual_search_needed"] = True
        resolved["reason"] = "publisher_blocked_or_login_required"
        return resolved
    if source_url and not is_probably_downloadable_paper_url(source_url):
        resolved["manual_search_needed"] = True
        resolved["reason"] = "listing_page_only"
        return resolved
    if source_url:
        resolved["manual_search_needed"] = True
        resolved["reason"] = "pdf_not_found_manual_search_needed"
    return resolved


def resolve_pdf_url(url: str | None) -> str | None:
    if not isinstance(url, str) or not url.strip():
        return None
    url = url.strip()
    if url.lower().endswith(".pdf"):
        return url
    cached = read_pdf_cache(url)
    if cached is not None:
        return cached
    session = make_session()
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException:
        write_pdf_cache(url, None)
        return None
    html_text = response.text
    candidates: list[tuple[int, str]] = []
    meta_patterns = [
        r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']og:pdf["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    for pattern in meta_patterns:
        matches = re.findall(pattern, html_text, flags=re.I)
        candidates.extend((200, match) for match in matches)
    if _looks_like_listing_page_url(url) and candidates:
        best_meta = sorted(candidates, key=lambda item: item[0], reverse=True)[0][1]
        write_pdf_cache(url, best_meta)
        return best_meta
    if _looks_like_listing_page_url(url):
        write_pdf_cache(url, None)
        return None
    href_matches = re.findall(
        r"<a[^>]+href=[\"']([^\"']+\.pdf(?:\?[^\"']*)?)[\"'][^>]*>(.*?)</a>",
        html_text,
        flags=re.I | re.S,
    )
    page_host = (urlparse(url).hostname or "").lower()
    trusted_pdf_hosts = {
        page_host,
        "arxiv.org",
        "export.arxiv.org",
        "openreview.net",
        "usenix.org",
        "www.usenix.org",
        "dl.acm.org",
        "doi.org",
        "ieeexplore.ieee.org",
        "www.vldb.org",
    }
    for href, anchor_text in href_matches:
        resolved = urljoin(url, href)
        host = (urlparse(resolved).hostname or "").lower()
        anchor = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", anchor_text)).strip().lower()
        score = 0
        if host in trusted_pdf_hosts:
            score += 120
        if "citation_pdf_url" in anchor or "pdf" == anchor:
            score += 40
        if any(token in anchor for token in ["paper", "publication", "manuscript", "download", "pdf"]):
            score += 30
        if host == page_host:
            score += 20
        if score > 0:
            candidates.append((score, resolved))
    if "arxiv.org/abs/" in url:
        candidates.append((180, url.replace("/abs/", "/pdf/") + ".pdf"))
    for _, candidate in sorted(candidates, key=lambda item: item[0], reverse=True):
        if candidate.lower().endswith(".pdf") or ".pdf?" in candidate.lower():
            write_pdf_cache(url, candidate)
            return candidate
    write_pdf_cache(url, None)
    return None


def extract_author_names(authors: list[Any] | None) -> list[str]:
    results: list[str] = []
    for author in authors or []:
        if isinstance(author, dict):
            name = author.get("name")
        else:
            name = str(author).strip()
        if name:
            results.append(name)
    return results


def venue_bucket(venue: str, preferred: list[str], fallback: list[str]) -> tuple[str, int]:
    for index, name in enumerate(preferred):
        if venue_matches(venue, name):
            return "preferred", 200 - index
    for index, name in enumerate(fallback):
        if venue_matches(venue, name):
            return "fallback", 100 - index
    return "other", 10


def is_allowed_venue(venue: str, preferred: list[str], fallback: list[str]) -> bool:
    bucket, _ = venue_bucket(venue, preferred, fallback)
    return bucket in {"preferred", "fallback"}


def _sleep_seconds(attempt: int) -> float:
    return min(2**attempt, 8)


def _get_json_with_retry(
    source_name: str,
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any],
    timeout: int,
    max_attempts: int = 2,
) -> dict[str, Any]:
    last_error: Exception | None = None
    saw_rate_limit = False
    for attempt in range(max_attempts):
        response = session.get(url, params=params, timeout=timeout)
        try:
            response.raise_for_status()
            payload = response.json() or {}
            if isinstance(payload, dict):
                return payload
            return {}
        except HTTPError as exc:
            last_error = exc
            status = exc.response.status_code if exc.response is not None else None
            if status == 429:
                saw_rate_limit = True
                mark_source_cooldown(source_name)
            if status not in RETRYABLE_STATUS_CODES or attempt == max_attempts - 1:
                break
            time.sleep(_sleep_seconds(attempt))
        except requests.RequestException as exc:
            last_error = exc
            mark_source_cooldown(source_name)
            if attempt == max_attempts - 1:
                break
            time.sleep(_sleep_seconds(attempt))
    if saw_rate_limit:
        raise SearchRateLimitError("semantic_scholar_rate_limited") from last_error
    if last_error:
        raise RuntimeError(f"semantic_scholar_request_failed: {last_error}") from last_error
    raise RuntimeError("semantic_scholar_request_failed")


def parse_arxiv_atom(xml_text: str) -> list[dict[str, Any]]:
    try:
        import xml.etree.ElementTree as ET

        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise RuntimeError(f"arxiv_parse_failed: {exc}") from exc

    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    rows: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", namespaces):
        entry_id = (entry.findtext("atom:id", default="", namespaces=namespaces) or "").strip()
        title = " ".join((entry.findtext("atom:title", default="", namespaces=namespaces) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=namespaces) or "").split())
        published = (entry.findtext("atom:published", default="", namespaces=namespaces) or "").strip()
        year = None
        if len(published) >= 4 and published[:4].isdigit():
            year = int(published[:4])
        authors = []
        for author in entry.findall("atom:author", namespaces):
            name = (author.findtext("atom:name", default="", namespaces=namespaces) or "").strip()
            if name:
                authors.append({"name": name})
        pdf_url = None
        for link in entry.findall("atom:link", namespaces):
            title_attr = (link.attrib.get("title") or "").lower()
            type_attr = (link.attrib.get("type") or "").lower()
            href = link.attrib.get("href")
            if href and (title_attr == "pdf" or type_attr == "application/pdf"):
                pdf_url = href
                break
        arxiv_id = entry_id.rsplit("/", 1)[-1] if entry_id else None
        rows.append(
            {
                "title": title or "Untitled Paper",
                "year": year,
                "venue": "arXiv",
                "abstract": summary or None,
                "authors": authors,
                "externalIds": {"ArXiv": arxiv_id} if arxiv_id else {},
                "openAccessPdf": {"url": pdf_url} if pdf_url else {},
                "url": entry_id or None,
                "paperId": f"arxiv:{arxiv_id}" if arxiv_id else None,
            }
        )
    return rows


def query_semantic_scholar(
    query: str,
    limit: int = 20,
    min_year: int | None = None,
) -> list[dict[str, Any]]:
    cached = read_cache("semantic_scholar", query, limit, min_year)
    if cached is not None:
        return cached
    if is_source_on_cooldown("semantic_scholar"):
        raise SearchRateLimitError("semantic_scholar_rate_limited")
    session = make_session()
    params = {
        "query": query,
        "limit": limit,
        "fields": ",".join(
            [
                "title",
                "year",
                "venue",
                "abstract",
                "authors",
                "externalIds",
                "openAccessPdf",
                "url",
                "paperId",
            ]
        ),
    }
    if min_year:
        params["year"] = f"{min_year}-"
    payload = _get_json_with_retry("semantic_scholar", session, SEMANTIC_SCHOLAR_API, params=params, timeout=15)
    rows = payload.get("data") or []
    write_cache("semantic_scholar", query, limit, min_year, rows)
    return rows


def query_arxiv(
    query: str,
    limit: int = 20,
    min_year: int | None = None,
) -> list[dict[str, Any]]:
    cached = read_cache("arxiv", query, limit, min_year)
    if cached is not None:
        return cached
    if is_source_on_cooldown("arxiv"):
        raise RuntimeError("arxiv_source_on_cooldown")
    session = make_session()
    search_query = f"all:{quote_plus(query)}"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": limit,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        response = session.get(ARXIV_API, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        mark_source_cooldown("arxiv")
        raise RuntimeError(f"arxiv_request_failed: {exc}") from exc
    rows = parse_arxiv_atom(response.text)
    if min_year:
        rows = [row for row in rows if not isinstance(row.get("year"), int) or row["year"] >= min_year]
    write_cache("arxiv", query, limit, min_year, rows)
    return rows


def query_openalex(
    query: str,
    limit: int = 20,
    min_year: int | None = None,
) -> list[dict[str, Any]]:
    cached = read_cache("openalex", query, limit, min_year)
    if cached is not None:
        return cached
    if is_source_on_cooldown("openalex"):
        raise RuntimeError("openalex_source_on_cooldown")
    session = make_session()
    params: dict[str, Any] = {
        "search": query,
        "per-page": limit,
        "sort": "publication_year:desc",
    }
    if min_year:
        params["filter"] = f"from_publication_date:{min_year}-01-01"
    try:
        response = session.get(OPENALEX_API, params=params, timeout=12)
        response.raise_for_status()
    except requests.RequestException as exc:
        mark_source_cooldown("openalex")
        raise RuntimeError(f"openalex_request_failed: {exc}") from exc
    payload = response.json() or {}
    rows: list[dict[str, Any]] = []
    for item in payload.get("results") or []:
        locations = item.get("locations") or []
        pdf_url = None
        for location in locations:
            pdf_url = (location.get("pdf_url") or location.get("landing_page_url") or None)
            if pdf_url:
                break
        if isinstance(pdf_url, str) and not pdf_url.lower().endswith(".pdf"):
            pdf_url = None
        authors = []
        for authorship in item.get("authorships") or []:
            author = authorship.get("author") or {}
            name = author.get("display_name")
            if name:
                authors.append({"name": name})
        venue = ((item.get("primary_location") or {}).get("source") or {}).get("display_name") or "Unknown Venue"
        year = item.get("publication_year")
        rows.append(
            {
                "title": item.get("display_name") or "Untitled Paper",
                "year": year if isinstance(year, int) else None,
                "venue": venue,
                "abstract": None,
                "authors": authors,
                "doi": item.get("doi"),
                "externalIds": {},
                "openAccessPdf": {"url": pdf_url} if pdf_url else {},
                "url": item.get("id"),
                "paperId": item.get("id"),
            }
        )
    if min_year:
        rows = [row for row in rows if not isinstance(row.get("year"), int) or row["year"] >= min_year]
    write_cache("openalex", query, limit, min_year, rows)
    return rows


def query_dblp(
    query: str,
    limit: int = 20,
    min_year: int | None = None,
) -> list[dict[str, Any]]:
    cached = read_cache("dblp", query, limit, min_year)
    if cached is not None:
        return cached
    if is_source_on_cooldown("dblp"):
        raise RuntimeError("dblp_source_on_cooldown")
    session = make_session()
    params = {
        "q": query,
        "h": limit,
        "format": "json",
    }
    try:
        response = session.get(DBLP_API, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        mark_source_cooldown("dblp")
        raise RuntimeError(f"dblp_request_failed: {exc}") from exc
    payload = response.json() or {}
    hits = (((payload.get("result") or {}).get("hits") or {}).get("hit") or [])
    rows: list[dict[str, Any]] = []
    for hit in hits:
        info = hit.get("info") or {}
        year_raw = info.get("year")
        try:
            year = int(year_raw) if year_raw is not None else None
        except (TypeError, ValueError):
            year = None
        venue = info.get("venue") or info.get("booktitle") or info.get("journal") or "Unknown Venue"
        authors_raw = ((info.get("authors") or {}).get("author") or [])
        if isinstance(authors_raw, dict):
            authors_raw = [authors_raw]
        authors: list[dict[str, str]] = []
        for author in authors_raw:
            if isinstance(author, dict):
                name = author.get("text") or author.get("name")
            else:
                name = str(author)
            if name:
                authors.append({"name": name})
        url = info.get("ee") or info.get("url")
        rows.append(
            {
                "title": info.get("title") or "Untitled Paper",
                "year": year,
                "venue": venue,
                "abstract": None,
                "authors": authors,
                "externalIds": {},
                "openAccessPdf": {"url": url} if isinstance(url, str) and url.lower().endswith(".pdf") else {},
                "url": url or info.get("url"),
                "paperId": info.get("key") or info.get("url"),
            }
        )
    if min_year:
        rows = [row for row in rows if not isinstance(row.get("year"), int) or row["year"] >= min_year]
    write_cache("dblp", query, limit, min_year, rows)
    return rows


def query_papers_resilient(
    query: str,
    limit: int = 20,
    min_year: int | None = None,
) -> tuple[list[dict[str, Any]], str | None]:
    try:
        return query_semantic_scholar(query=query, limit=limit, min_year=min_year), None
    except SearchRateLimitError:
        try:
            rows = query_arxiv(query=query, limit=limit, min_year=min_year)
            return rows, "semantic_scholar_rate_limited_fallback_arxiv"
        except Exception as exc:
            try:
                rows = query_dblp(query=query, limit=limit, min_year=min_year)
                return rows, f"semantic_scholar_rate_limited_arxiv_failed_fallback_dblp: {exc}"
            except Exception as dblp_exc:
                try:
                    rows = query_openalex(query=query, limit=limit, min_year=min_year)
                    return rows, f"semantic_scholar_rate_limited_arxiv_dblp_failed_fallback_openalex: {exc}; {dblp_exc}"
                except Exception as openalex_exc:
                    return [], f"semantic_scholar_rate_limited_arxiv_dblp_openalex_fallback_failed: {exc}; {dblp_exc}; {openalex_exc}"
    except RuntimeError as exc:
        try:
            rows = query_arxiv(query=query, limit=limit, min_year=min_year)
            return rows, f"{exc}_fallback_arxiv"
        except Exception as arxiv_exc:
            try:
                rows = query_dblp(query=query, limit=limit, min_year=min_year)
                return rows, f"{exc}_arxiv_failed_fallback_dblp: {arxiv_exc}"
            except Exception as dblp_exc:
                try:
                    rows = query_openalex(query=query, limit=limit, min_year=min_year)
                    return rows, f"{exc}_arxiv_dblp_failed_fallback_openalex: {arxiv_exc}; {dblp_exc}"
                except Exception:
                    raise


def _paper_discovery_identity(row: dict[str, Any]) -> str:
    title = re.sub(r"[^a-z0-9]+", " ", str(row.get("title") or "").lower()).strip()
    if title:
        return f"title:{title}"
    external_ids = row.get("externalIds") or {}
    for field in ("DOI", "ArXiv", "DBLP", "CorpusId"):
        value = external_ids.get(field)
        if value:
            return f"{field.lower()}:{str(value).strip().lower()}"
    return f"url:{str(row.get('url') or row.get('paperId') or '').strip().lower()}"


def query_papers_ensemble(
    query: str,
    limit: int = 20,
    min_year: int | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Query complementary academic indexes for evidence-oriented recall."""
    sources = (
        ("semantic_scholar", query_semantic_scholar),
        ("openalex", query_openalex),
        ("dblp", query_dblp),
        ("arxiv", query_arxiv),
    )
    merged: dict[str, dict[str, Any]] = {}
    notes: list[str] = []
    successful_sources = 0
    for source_name, source_query in sources:
        try:
            rows = source_query(query=query, limit=limit, min_year=min_year)
            successful_sources += 1
            notes.append(f"{source_name}:ok:{len(rows)}")
        except Exception as exc:  # noqa: BLE001 - preserve partial multi-index coverage
            notes.append(f"{source_name}:failed:{exc}")
            continue
        for raw_row in rows:
            row = dict(raw_row)
            key = _paper_discovery_identity(row)
            existing = merged.get(key)
            if existing is None:
                row["discoverySources"] = [source_name]
                merged[key] = row
                continue
            sources_seen = list(existing.get("discoverySources") or [])
            if source_name not in sources_seen:
                sources_seen.append(source_name)
            existing["discoverySources"] = sources_seen
            for field in ("abstract", "url", "publicationUrl", "paperId", "venue", "year"):
                if not existing.get(field) and row.get(field):
                    existing[field] = row[field]
            if not existing.get("authors") and row.get("authors"):
                existing["authors"] = row["authors"]
            if not existing.get("openAccessPdf") and row.get("openAccessPdf"):
                existing["openAccessPdf"] = row["openAccessPdf"]
            existing_ids = dict(existing.get("externalIds") or {})
            existing_ids.update({key: value for key, value in (row.get("externalIds") or {}).items() if value})
            existing["externalIds"] = existing_ids
    if successful_sources == 0:
        raise RuntimeError("all academic discovery indexes failed: " + "; ".join(notes))
    return list(merged.values()), notes


def search_subtopic(
    topic_name: str,
    subtopic: dict[str, Any],
    preferred_venues: list[str],
    fallback_venues: list[str],
    min_year: int,
    limit: int = 8,
) -> tuple[list[SearchResult], str | None]:
    keyword_query = " OR ".join(subtopic.get("keywords") or [])
    venue_query = " OR ".join(preferred_venues[:6] + fallback_venues[:2])
    query = f"({topic_name}) ({subtopic.get('name')}) ({keyword_query}) ({venue_query})"
    rows, fallback_status = query_papers_resilient(query=query, limit=limit * 3, min_year=min_year)
    results: list[SearchResult] = []
    for row in rows:
        year = row.get("year")
        if min_year and isinstance(year, int) and year < min_year:
            continue
        venue = normalize_venue(row.get("venue"))
        bucket, bucket_score = venue_bucket(venue, preferred_venues, fallback_venues)
        score = bucket_score
        if choose_pdf_url(row):
            score += 20
        if row.get("abstract"):
            score += 5
        results.append(
            SearchResult(
                title=row.get("title") or "Untitled Paper",
                year=year if isinstance(year, int) else None,
                venue=venue or "Unknown Venue",
                paper_id=row.get("paperId"),
                url=row.get("url"),
                abstract=row.get("abstract"),
                authors=extract_author_names(row.get("authors")),
                pdf_url=choose_pdf_url(row),
                source=row,
                bucket=bucket,
                subtopic_id=subtopic.get("id") or "unknown",
                score=score,
            )
        )
    results.sort(key=lambda item: (item.score, item.year or 0), reverse=True)
    return results[:limit], fallback_status


def search_short_queries_for_subtopic(
    topic_name: str,
    subtopic: dict[str, Any],
    preferred_venues: list[str],
    fallback_venues: list[str],
    min_year: int,
    limit: int = 8,
) -> tuple[list[SearchResult], list[str]]:
    subtopic_name = subtopic.get("name") or subtopic.get("id") or "unknown"
    keywords = unique_preserve_order(list(subtopic.get("keywords") or []) + list(subtopic.get("seed_papers") or []))
    aliases = unique_preserve_order(list(subtopic.get("aliases") or []))
    queries = unique_preserve_order(
        [
            f"{topic_name} {subtopic_name}",
            *keywords,
            *aliases,
            *(f"{topic_name} {keyword}" for keyword in keywords[:4]),
            *(f"{topic_name} {alias}" for alias in aliases[:3]),
        ]
    )
    queries = queries[:AGGREGATE_QUERY_BUDGET]
    all_results: list[SearchResult] = []
    recovery_notes: list[str] = []
    seen_titles: set[str] = set()

    def _normalize_text(text: str) -> str:
        lowered = (text or "").lower().replace("-", " ")
        lowered = re.sub(r"[^a-z0-9\s]+", " ", lowered)
        return re.sub(r"\s+", " ", lowered).strip()

    def relevance_score(row: dict[str, Any], query: str) -> int:
        title = (row.get("title") or "").lower()
        abstract = (row.get("abstract") or "").lower()
        query_l = query.lower()
        score = 0
        if query_l and query_l in title:
            score += 40
        if query_l and query_l in abstract:
            score += 20
        for keyword in keywords:
            keyword_l = _normalize_text(keyword)
            if keyword_l and keyword_l in title:
                score += 35 if " " in keyword_l else 14
            elif keyword_l and keyword_l in abstract:
                score += 16 if " " in keyword_l else 8
        for alias in aliases:
            alias_l = _normalize_text(alias)
            if alias_l and alias_l in title:
                score += 28 if " " in alias_l else 10
            elif alias_l and alias_l in abstract:
                score += 12 if " " in alias_l else 5
        return score

    for query in queries:
        try:
            rows, fallback_status = query_papers_resilient(query=query, limit=max(limit * 2, 8), min_year=min_year)
        except RuntimeError as exc:
            recovery_notes.append(f"{query}: {exc}")
            continue
        if fallback_status:
            recovery_notes.append(f"{query}: {fallback_status}")
        for row in rows:
            year = row.get("year")
            if min_year and isinstance(year, int) and year < min_year:
                continue
            venue = normalize_venue(row.get("venue"))
            if not is_allowed_venue(venue, preferred_venues, fallback_venues):
                continue
            title = row.get("title") or "Untitled Paper"
            title_key = title.strip().lower()
            if title_key in seen_titles:
                continue
            matched_relevance = relevance_score(row, query)
            if matched_relevance < 30:
                continue
            bucket, bucket_score = venue_bucket(venue, preferred_venues, fallback_venues)
            query_match_score = 0
            lowered_query = _normalize_text(query)
            lowered_title = _normalize_text(title)
            lowered_abstract = _normalize_text(row.get("abstract") or "")
            if lowered_query in lowered_title:
                query_match_score += 35
            if any(_normalize_text(keyword) in lowered_title for keyword in keywords):
                query_match_score += 24
            if any(_normalize_text(alias) in lowered_title for alias in aliases):
                query_match_score += 18
            if any(_normalize_text(keyword) in lowered_abstract for keyword in keywords):
                query_match_score += 10
            if choose_pdf_url(row):
                query_match_score += 15
            if row.get("abstract"):
                query_match_score += 10
            seen_titles.add(title_key)
            all_results.append(
                SearchResult(
                    title=title,
                    year=year if isinstance(year, int) else None,
                    venue=venue or "Unknown Venue",
                    paper_id=row.get("paperId"),
                    url=row.get("url"),
                    abstract=row.get("abstract"),
                    authors=extract_author_names(row.get("authors")),
                    pdf_url=choose_pdf_url(row),
                    source=row,
                    bucket=bucket,
                    subtopic_id=subtopic.get("id") or "unknown",
                    score=bucket_score + query_match_score + matched_relevance,
                )
            )
        if len(all_results) >= limit * 2:
            break

    all_results.sort(key=lambda item: (item.score, item.year or 0), reverse=True)
    return all_results[:limit], recovery_notes


def rows_to_search_results(
    rows: list[dict[str, Any]],
    *,
    preferred_venues: list[str],
    fallback_venues: list[str],
    subtopic_id: str,
    keywords: list[str],
    min_year: int | None,
) -> list[SearchResult]:
    results: list[SearchResult] = []
    seen_titles: set[str] = set()
    for row in rows:
        title = row.get("title") or "Untitled Paper"
        title_key = title.strip().lower()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        year = row.get("year")
        if min_year and isinstance(year, int) and year < min_year:
            continue
        venue = normalize_venue(row.get("venue"))
        bucket, bucket_score = venue_bucket(venue, preferred_venues, fallback_venues)
        score = bucket_score
        lowered_title = title.lower()
        if any(keyword.lower() in lowered_title for keyword in keywords):
            score += 30
        if choose_pdf_url(row):
            score += 15
        if row.get("abstract"):
            score += 10
        results.append(
            SearchResult(
                title=title,
                year=year if isinstance(year, int) else None,
                venue=venue or "Unknown Venue",
                paper_id=row.get("paperId"),
                url=row.get("url"),
                abstract=row.get("abstract"),
                authors=extract_author_names(row.get("authors")),
                pdf_url=choose_pdf_url(row),
                source=row,
                bucket=bucket,
                subtopic_id=subtopic_id,
                score=score,
            )
        )
    results.sort(key=lambda item: (item.score, item.year or 0), reverse=True)
    return results


def sanitize_filename(text: str) -> str:
    value = "".join("-" if char in '<>:"/\\|?*' else char for char in text)
    value = " ".join(value.split())
    return value[:96].strip(" .-_") or "paper"


def download_pdf(url: str, target_dir: Path, stem: str) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    session = make_session()
    resolved_url = resolve_pdf_url(url) or url
    response = session.get(resolved_url, timeout=120)
    response.raise_for_status()
    file_path = target_dir / f"{sanitize_filename(stem)}.pdf"
    file_path.write_bytes(response.content)
    return file_path
