from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

import requests


USER_AGENT = "reference-validation-report/1.0 (Codex skill)"
REQUEST_TIMEOUT = 4
OFFICIAL_DOMAINS = {
    "doi.org",
    "dl.acm.org",
    "ieeexplore.ieee.org",
    "link.springer.com",
    "springer.com",
    "usenix.org",
    "openreview.net",
    "proceedings.mlr.press",
    "jmlr.org",
    "aaai.org",
    "ojs.aaai.org",
    "neurips.cc",
    "cvf.com",
    "thecvf.com",
    "aclanthology.org",
    "arxiv.org",
}

SEARCH_RESULT_DOMAINS = OFFICIAL_DOMAINS | {
    "dblp.org",
}

TYPE_MAP = {
    "journal-article": "article",
    "proceedings-article": "inproceedings",
    "posted-content": "article",
    "report": "techreport",
    "book-chapter": "incollection",
}


@dataclass
class LocalEntry:
    key: str
    entry_type: str
    fields: dict[str, str]
    bibliography_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify bibliography entries against authoritative online sources.")
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--bib", default="refs.bib")
    parser.add_argument("--bbl", default="main.bbl")
    parser.add_argument("--tex", default="main.tex")
    parser.add_argument("--paper-title")
    parser.add_argument("--venue", default="未知投稿期刊")
    parser.add_argument("--verification-date", default=str(date.today()))
    parser.add_argument("--output", required=True)
    parser.add_argument("--sleep-ms", type=int, default=150)
    return parser.parse_args()


def normalize_text(text: str) -> str:
    text = text or ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", text)
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def split_bbl_entries(bbl_text: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^}]+)\}(?P<body>.*?)(?=(?:\n\\bibitem(?:\[[^\]]*\])?\{|\\end\{thebibliography\}))",
        re.S,
    )
    return [(m.group("key").strip(), m.group("body").strip()) for m in pattern.finditer(bbl_text)]


def split_inline_tex_entries(tex_text: str) -> list[tuple[str, str]]:
    bib_env = re.search(r"\\begin\{thebibliography\}.*?(?P<body>.*)\\end\{thebibliography\}", tex_text, re.S)
    if not bib_env:
        return []
    body = bib_env.group("body")
    pattern = re.compile(
        r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^}]+)\}(?P<body>.*?)(?=(?:\n\\bibitem(?:\[[^\]]*\])?\{|\\end\{thebibliography\}|$))",
        re.S,
    )
    return [(m.group("key").strip(), m.group("body").strip()) for m in pattern.finditer(body)]


def strip_latex(text: str) -> str:
    previous = None
    current = re.sub(r"(?m)^\s*%.*$", " ", text)
    current = current.replace("\n", " ")
    current = current.replace("~", " ")
    current = current.replace("\\&", "&")
    current = re.sub(r"\\newblock\b", " ", current)
    current = re.sub(r"\\providecommand\{[^}]*\}\{[^}]*\}", " ", current)
    wrappers = ["emph", "textit", "textbf", "url", "showarticletitle", "showURL", "showDOI", "showISBNx"]
    while previous != current:
        previous = current
        current = re.sub(r"\\bibinfo\{[^{}]*\}\{([^{}]*)\}", r"\1", current)
        for name in wrappers:
            current = re.sub(rf"\\{name}\{{([^{{}}]*)\}}", r"\1", current)
        current = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", current)
    current = re.sub(r"\\[a-zA-Z@]+\*?", " ", current)
    current = current.replace("{", "").replace("}", "")
    current = re.sub(r"\s+", " ", current)
    return current.strip()


def bibliography_text_from_raw(raw: str) -> str:
    text = strip_latex(raw)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()


def infer_unstructured_fields(raw: str, bibliography_text: str) -> tuple[str, dict[str, str]]:
    fields: dict[str, str] = {}
    text = bibliography_text.strip()
    raw = raw.strip()

    italic_match = re.search(r"\\textit\{([^{}]+)\}", raw)
    title = ""
    if italic_match:
        title = strip_latex(italic_match.group(1))
        prefix = strip_latex(raw[: italic_match.start()]).strip(" ,.")
    else:
        prefix = ""
        # Fallback: capture leading author block, then title before venue marker.
        m = re.match(
            r"(?P<authors>.+?),(?:\s+)?(?P<title>[^.,][^,]+?)(?:(?:,\s+in:)|(?:,\s+[A-Z][^,]+,\s*\(?\d{4}\)?)|(?:\.\s+[A-Z][^,]+,\s*\d{4}))",
            text,
        )
        if m:
            prefix = m.group("authors").strip(" ,.")
            title = m.group("title").strip(" ,.")

    if title:
        fields["title"] = title
    if prefix:
        author_text = prefix.replace(" and et al.", "").replace(" et al.", "")
        author_text = re.sub(r"\band\s+et al\.?", "", author_text, flags=re.I)
        author_text = re.sub(r"\bet al\.?", "", author_text, flags=re.I)
        author_parts = [a.strip(" ,.") for a in re.split(r",\s*", author_text) if a.strip(" ,.")]
        if author_parts:
            fields["author"] = " and ".join(author_parts)

    year = parse_year(text)
    if year:
        fields["year"] = str(year)

    doi_match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", text, re.I)
    if doi_match:
        fields["doi"] = doi_match.group(0)
    url_match = re.search(r"https?://\S+", text)
    if url_match:
        fields["url"] = url_match.group(0).rstrip(".,)")
    arxiv_match = re.search(r"(?:arXiv:|abs/)(\d{4}\.\d{4,5})", text, re.I)
    if arxiv_match and "url" not in fields:
        fields["url"] = f"https://arxiv.org/abs/{arxiv_match.group(1)}"
        fields["journal"] = f"arXiv preprint arXiv:{arxiv_match.group(1)}"

    entry_type = "inproceedings" if re.search(r"\bin:\s|Proceedings|Conference|Symposium|Workshop", text, re.I) else "article"
    if "journal" not in fields and "in:" not in text.lower():
        after_title = text
        if title and title in text:
            after_title = text.split(title, 1)[1].lstrip(" ,.:-")
        venue_match = re.match(r"([^,]+(?:,[^,(]+)?)", after_title)
        if venue_match:
            venue = venue_match.group(1).strip(" ,.")
            if venue and parse_year(venue) is None:
                fields["journal"] = venue
    return entry_type, fields


def extract_title_from_tex(tex_text: str) -> str | None:
    for pattern in [r"\\title(?:\[[^\]]*\])?\{(?P<title>.*?)\}", r"\\shorttitle\{(?P<title>.*?)\}"]:
        match = re.search(pattern, tex_text, re.S)
        if match:
            title = strip_latex(match.group("title"))
            if title:
                return title
    return None


def split_bib_entries(text: str) -> list[str]:
    entries: list[str] = []
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        brace = text.find("{", at)
        if brace == -1:
            break
        depth = 0
        for j in range(brace, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    entries.append(text[at : j + 1])
                    i = j + 1
                    break
        else:
            break
    return entries


def parse_bib_entry(entry_text: str) -> tuple[str, str, dict[str, str]] | None:
    header = re.match(r"@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,]+)\s*,", entry_text, re.S)
    if not header:
        return None
    entry_type = header.group("type").lower()
    key = header.group("key").strip()
    body = entry_text[header.end() :].rsplit("}", 1)[0]
    fields: dict[str, str] = {}
    i = 0
    while i < len(body):
        while i < len(body) and body[i] in " \t\r\n,":
            i += 1
        if i >= len(body):
            break
        m = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", body[i:])
        if not m:
            break
        field = m.group(1).lower()
        i += m.end()
        if i >= len(body):
            break
        if body[i] == "{":
            depth = 0
            start = i + 1
            while i < len(body):
                if body[i] == "{":
                    depth += 1
                elif body[i] == "}":
                    depth -= 1
                    if depth == 0:
                        fields[field] = body[start:i]
                        i += 1
                        break
                i += 1
        elif body[i] == '"':
            i += 1
            start = i
            while i < len(body) and body[i] != '"':
                if body[i] == "\\" and i + 1 < len(body):
                    i += 2
                else:
                    i += 1
            fields[field] = body[start:i]
            i += 1
        else:
            start = i
            while i < len(body) and body[i] not in ",\n":
                i += 1
            fields[field] = body[start:i].strip()
    return key, entry_type, {k: strip_latex(v) for k, v in fields.items()}


def load_local_entries(project_dir: Path, bib_name: str, bbl_name: str, tex_name: str) -> tuple[list[LocalEntry], str | None]:
    bib_path = project_dir / bib_name
    bbl_path = project_dir / bbl_name
    tex_path = project_dir / tex_name

    bib_map: dict[str, tuple[str, dict[str, str]]] = {}
    if bib_path.exists():
        bib_text = bib_path.read_text(encoding="utf-8", errors="ignore")
        for raw_entry in split_bib_entries(bib_text):
            parsed = parse_bib_entry(raw_entry)
            if parsed:
                key, entry_type, fields = parsed
                bib_map[key] = (entry_type, fields)

    tex_text = tex_path.read_text(encoding="utf-8", errors="ignore") if tex_path.exists() else ""
    pairs = split_bbl_entries(bbl_path.read_text(encoding="utf-8", errors="ignore")) if bbl_path.exists() else []
    if not pairs and tex_text:
        pairs = split_inline_tex_entries(tex_text)
    if not pairs:
        raise ValueError("No bibliography entries found. Need .bbl or inline \\bibitem.")

    entries: list[LocalEntry] = []
    for key, raw in pairs:
        entry_type, fields = bib_map.get(key, ("unknown", {}))
        bibliography_text = bibliography_text_from_raw(raw)
        if not fields:
            inferred_type, inferred_fields = infer_unstructured_fields(raw, bibliography_text)
            entry_type = inferred_type
            fields = inferred_fields
        entries.append(
            LocalEntry(
                key=key,
                entry_type=entry_type,
                fields=fields,
                bibliography_text=bibliography_text,
            )
        )
    return entries, extract_title_from_tex(tex_text)


def extract_author_surnames(author_field: str) -> list[str]:
    if not author_field:
        return []
    if " and " in author_field:
        authors = [a.strip() for a in author_field.split(" and ") if a.strip()]
    else:
        authors = [a.strip() for a in re.split(r",\s*", author_field) if a.strip()]
    surnames: list[str] = []
    for author in authors:
        if "," in author:
            surname = author.split(",", 1)[0]
        else:
            surname = author.split()[-1]
        surnames.append(normalize_text(surname))
    return [s for s in surnames if s]


def parse_year(value: str) -> int | None:
    if not value:
        return None
    m = re.search(r"(19|20)\d{2}", value)
    return int(m.group(0)) if m else None


def extract_arxiv_id(entry: LocalEntry) -> str | None:
    fields = entry.fields
    candidates = [
        fields.get("eprint", ""),
        fields.get("url", ""),
        fields.get("doi", ""),
        fields.get("journal", ""),
    ]
    for value in candidates:
        match = re.search(r"(?:arXiv:|abs/|pdf/)?(\d{4}\.\d{4,5})(?:v\d+)?", value, re.I)
        if match:
            return match.group(1)
    return None


def pick_title(entry: LocalEntry) -> str:
    return entry.fields.get("title") or entry.bibliography_text


def pick_year(entry: LocalEntry) -> int | None:
    return parse_year(entry.fields.get("year", "")) or parse_year(entry.bibliography_text)


def local_venue(entry: LocalEntry) -> str:
    return entry.fields.get("journal") or entry.fields.get("booktitle") or ""


def venue_similarity(a: str, b: str) -> float:
    a_norm = normalize_text(a)
    b_norm = normalize_text(b)
    if not a_norm or not b_norm:
        return 0.0
    if a_norm in b_norm or b_norm in a_norm:
        return 1.0
    return SequenceMatcher(None, a_norm, b_norm).ratio()


def compare_metadata(entry: LocalEntry, matched: dict[str, Any]) -> dict[str, list[str]]:
    critical: list[str] = []
    advisory: list[str] = []
    local_title = entry.fields.get("title", "")
    matched_title = matched.get("title", "")
    if local_title and matched_title and similarity(local_title, matched_title) < 0.9:
        critical.append("标题不一致")

    local_year = pick_year(entry)
    matched_year = matched.get("year")
    if local_year and matched_year:
        delta = abs(local_year - int(matched_year))
        if delta > 1:
            critical.append("年份不一致")
        elif delta == 1:
            advisory.append("年份建议复核")

    local_author_field = entry.fields.get("author", "")
    local_authors = extract_author_surnames(entry.fields.get("author", ""))
    matched_authors = [normalize_text(a) for a in matched.get("author_surnames", []) if a]
    if (
        local_authors
        and matched_authors
        and "others" not in normalize_text(local_author_field)
        and "et al" not in normalize_text(local_author_field)
    ):
        overlap = set(local_authors[:2]) & set(matched_authors[:3])
        if not overlap:
            critical.append("作者不一致")

    local_venue_name = local_venue(entry)
    matched_venue = matched.get("venue", "")
    if local_venue_name and matched_venue:
        score = venue_similarity(local_venue_name, matched_venue)
        if score < 0.55:
            critical.append("会议/期刊不一致")
        elif score < 0.8:
            advisory.append("会议/期刊建议复核")

    local_doi = (entry.fields.get("doi") or "").strip().lower()
    matched_doi = (matched.get("doi") or "").strip().lower()
    if local_doi and matched_doi and local_doi != matched_doi:
        critical.append("DOI不一致")

    local_type = entry.entry_type
    matched_type = matched.get("entry_type")
    if local_type and matched_type and local_type != "unknown" and matched_type and local_type != matched_type:
        critical.append("条目类型不一致")

    local_pages = (entry.fields.get("pages") or "").strip()
    matched_pages = (matched.get("pages") or "").strip()
    if local_pages and matched_pages and normalize_text(local_pages) != normalize_text(matched_pages):
        advisory.append("页码建议复核")

    local_volume = (entry.fields.get("volume") or "").strip()
    matched_volume = (matched.get("volume") or "").strip()
    if local_volume and matched_volume and normalize_text(local_volume) != normalize_text(matched_volume):
        advisory.append("卷期建议复核")
    return {"critical": critical, "advisory": advisory}


class Verifier:
    def __init__(self, sleep_ms: int) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.sleep_ms = sleep_ms

    def sleep(self) -> None:
        time.sleep(self.sleep_ms / 1000)

    def get_json(self, url: str, **kwargs: Any) -> Any:
        response = self.session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        response.raise_for_status()
        self.sleep()
        return response.json()

    def get_text(self, url: str, **kwargs: Any) -> str:
        response = self.session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        response.raise_for_status()
        self.sleep()
        return response.text

    def verify(self, entry: LocalEntry) -> dict[str, Any]:
        methods = [
            self.try_doi,
            self.try_arxiv,
            self.try_crossref_bibliographic,
            self.try_crossref_title,
            self.try_official_url,
            self.try_official_search,
        ]
        for method in methods:
            result = method(entry)
            if result:
                issue_groups = compare_metadata(entry, result.get("matched_metadata", {}))
                critical_issues = issue_groups["critical"]
                advisory_issues = issue_groups["advisory"]
                result["metadata_issues"] = critical_issues + advisory_issues
                result["critical_issues"] = critical_issues
                result["advisory_issues"] = advisory_issues
                if result["status"] == "confirmed" and critical_issues:
                    result["status"] = "pending"
                    result["evidence_label"] = result.get("evidence_label", "已确认") + "，关键字段有差异"
                elif result["status"] == "confirmed" and advisory_issues:
                    result["evidence_label"] = result.get("evidence_label", "已确认") + "，建议复核次要字段"
                return result
        return {
            "status": "missing",
            "evidence_label": "未找到权威命中",
            "source_type": "none",
            "source_url": "",
            "matched_metadata": {},
            "metadata_issues": [],
            "critical_issues": [],
            "advisory_issues": [],
            "reason": "未能在 DOI、arXiv、Crossref 或官方 URL 中找到足够可信的匹配",
        }

    def try_doi(self, entry: LocalEntry) -> dict[str, Any] | None:
        doi = (entry.fields.get("doi") or "").strip()
        if not doi:
            return None
        if doi.lower().startswith("10.48550/arxiv."):
            return self.try_arxiv(entry)
        try:
            data = self.get_json(f"https://api.crossref.org/works/{quote(doi)}")
        except Exception:
            return None
        message = data.get("message", {})
        title = " ".join(message.get("title", []))
        matched = {
            "title": title,
            "year": (message.get("issued", {}).get("date-parts", [[None]])[0][0]),
            "author_surnames": [a.get("family", "") for a in message.get("author", [])],
            "entry_type": TYPE_MAP.get(message.get("type", ""), ""),
            "venue": " ".join(message.get("container-title", [])),
            "doi": message.get("DOI", ""),
        }
        if similarity(pick_title(entry), title) < 0.88:
            return None
        return {
            "status": "confirmed",
            "evidence_label": "DOI/Crossref",
            "source_type": "doi",
            "source_url": message.get("URL", f"https://doi.org/{doi}"),
            "matched_metadata": matched,
        }

    def try_arxiv(self, entry: LocalEntry) -> dict[str, Any] | None:
        arxiv_id = extract_arxiv_id(entry)
        if not arxiv_id:
            return None
        try:
            xml_text = self.get_text(f"https://export.arxiv.org/api/query?id_list={quote(arxiv_id)}")
        except Exception:
            return None
        root = ET.fromstring(xml_text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        item = root.find("atom:entry", ns)
        if item is None:
            return None
        title = (item.findtext("atom:title", default="", namespaces=ns) or "").replace("\n", " ").strip()
        published = item.findtext("atom:published", default="", namespaces=ns) or ""
        authors = [a.findtext("atom:name", default="", namespaces=ns) or "" for a in item.findall("atom:author", ns)]
        if similarity(pick_title(entry), title) < 0.88:
            return None
        return {
            "status": "confirmed",
            "evidence_label": "arXiv",
            "source_type": "arxiv",
            "source_url": f"https://arxiv.org/abs/{arxiv_id}",
            "matched_metadata": {
                "title": title,
                "year": parse_year(published),
                "author_surnames": [a.split()[-1] for a in authors if a],
                "entry_type": "article",
                "venue": "arXiv",
                "doi": f"10.48550/arXiv.{arxiv_id}",
            },
        }

    def try_crossref_title(self, entry: LocalEntry) -> dict[str, Any] | None:
        title = pick_title(entry)
        if not title:
            return None
        try:
            data = self.get_json(
                "https://api.crossref.org/works",
                params={"query.title": title, "rows": 5},
            )
        except Exception:
            return None
        items = data.get("message", {}).get("items", [])
        best: dict[str, Any] | None = None
        best_score = 0.0
        local_year = pick_year(entry)
        local_authors = extract_author_surnames(entry.fields.get("author", ""))
        for item in items:
            remote_title = " ".join(item.get("title", []))
            score = similarity(title, remote_title)
            remote_year = (item.get("issued", {}).get("date-parts", [[None]])[0][0])
            remote_authors = [normalize_text(a.get("family", "")) for a in item.get("author", []) if a.get("family")]
            if local_year and remote_year and abs(local_year - int(remote_year)) > 1:
                score -= 0.12
            if local_authors and remote_authors and not (set(local_authors[:2]) & set(remote_authors[:3])):
                score -= 0.08
            if score > best_score:
                best_score = score
                best = item
        if not best or best_score < 0.92:
            return None
        return {
            "status": "confirmed",
            "evidence_label": "Crossref标题匹配",
            "source_type": "crossref-search",
            "source_url": best.get("URL", ""),
            "matched_metadata": {
                "title": " ".join(best.get("title", [])),
                "year": (best.get("issued", {}).get("date-parts", [[None]])[0][0]),
                "author_surnames": [a.get("family", "") for a in best.get("author", [])],
                "entry_type": TYPE_MAP.get(best.get("type", ""), ""),
                "venue": " ".join(best.get("container-title", [])),
                "doi": best.get("DOI", ""),
            },
        }

    def try_crossref_bibliographic(self, entry: LocalEntry) -> dict[str, Any] | None:
        query_text = entry.bibliography_text or pick_title(entry)
        if not query_text:
            return None
        try:
            data = self.get_json(
                "https://api.crossref.org/works",
                params={"query.bibliographic": query_text, "rows": 6},
            )
        except Exception:
            return None
        items = data.get("message", {}).get("items", [])
        best: dict[str, Any] | None = None
        best_score = 0.0
        title = pick_title(entry)
        local_year = pick_year(entry)
        local_authors = extract_author_surnames(entry.fields.get("author", ""))
        local_venue_name = local_venue(entry)
        for item in items:
            remote_title = " ".join(item.get("title", []))
            score = similarity(title, remote_title) * 0.62
            remote_year = (item.get("issued", {}).get("date-parts", [[None]])[0][0])
            remote_venue = " ".join(item.get("container-title", []))
            remote_authors = [normalize_text(a.get("family", "")) for a in item.get("author", []) if a.get("family")]
            if local_year and remote_year:
                delta = abs(local_year - int(remote_year))
                score += 0.16 if delta == 0 else (0.08 if delta == 1 else -0.12)
            if local_authors and remote_authors and set(local_authors[:2]) & set(remote_authors[:3]):
                score += 0.12
            if local_venue_name and remote_venue:
                score += venue_similarity(local_venue_name, remote_venue) * 0.10
            if score > best_score:
                best_score = score
                best = item
        if not best or best_score < 0.74:
            return None
        return {
            "status": "confirmed",
            "evidence_label": "Crossref著录匹配",
            "source_type": "crossref-bibliographic",
            "source_url": best.get("URL", ""),
            "matched_metadata": {
                "title": " ".join(best.get("title", [])),
                "year": (best.get("issued", {}).get("date-parts", [[None]])[0][0]),
                "author_surnames": [a.get("family", "") for a in best.get("author", [])],
                "entry_type": TYPE_MAP.get(best.get("type", ""), ""),
                "venue": " ".join(best.get("container-title", [])),
                "doi": best.get("DOI", ""),
                "pages": best.get("page", ""),
                "volume": str(best.get("volume", "") or ""),
            },
        }

    def try_official_url(self, entry: LocalEntry) -> dict[str, Any] | None:
        url = (entry.fields.get("url") or "").strip()
        if not url:
            return None
        if not any(domain in url for domain in OFFICIAL_DOMAINS):
            return None
        try:
            text = self.get_text(url, allow_redirects=True)
        except Exception:
            return None
        title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        page_title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
        if page_title and similarity(pick_title(entry), page_title) >= 0.85:
            return {
                "status": "confirmed",
                "evidence_label": "官方URL",
                "source_type": "official-url",
                "source_url": url,
                "matched_metadata": {
                    "title": page_title,
                    "year": pick_year(entry),
                    "author_surnames": [],
                    "entry_type": "",
                    "venue": "",
                    "doi": "",
                },
            }
        return None

    def try_official_search(self, entry: LocalEntry) -> dict[str, Any] | None:
        title = pick_title(entry)
        if not title:
            return None
        try:
            search_html = self.get_text(
                f"https://duckduckgo.com/html/?q={quote(title)}",
                headers={"User-Agent": "Mozilla/5.0"},
            )
        except Exception:
            return None

        results = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', search_html)
        for href, label in results[:8]:
            url = html.unescape(href)
            if url.startswith("//duckduckgo.com/l/?"):
                parsed = urlparse("https:" + url)
                actual = parse_qs(parsed.query).get("uddg", [""])[0]
                url = unquote(actual) if actual else ""
            if not url:
                continue
            if not any(domain in url for domain in SEARCH_RESULT_DOMAINS):
                continue
            label_text = re.sub(r"<.*?>", " ", html.unescape(label))
            if similarity(title, label_text) < 0.72:
                continue
            try:
                page_html = self.get_text(url, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
            except Exception:
                continue
            title_match = re.search(r"<title[^>]*>(.*?)</title>", page_html, re.I | re.S)
            page_title = re.sub(r"\s+", " ", html.unescape(title_match.group(1))).strip() if title_match else ""
            best_text = page_title or label_text
            if similarity(title, best_text) < 0.78:
                continue

            source_type = "official-search"
            evidence_label = "官方搜索命中"
            if "arxiv.org" in url:
                source_type = "arxiv-search"
                evidence_label = "arXiv搜索命中"
            elif "usenix.org" in url:
                source_type = "usenix-search"
                evidence_label = "USENIX搜索命中"
            elif "dl.acm.org" in url:
                source_type = "acm-search"
                evidence_label = "ACM DL搜索命中"
            elif "dblp.org" in url:
                source_type = "dblp-search"
                evidence_label = "DBLP搜索命中"

            return {
                "status": "confirmed",
                "evidence_label": evidence_label,
                "source_type": source_type,
                "source_url": url,
                "matched_metadata": {
                    "title": best_text,
                    "year": pick_year(entry),
                    "author_surnames": [],
                    "entry_type": "",
                    "venue": "",
                    "doi": "",
                },
            }
        return None


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).resolve()
    entries, inferred_title = load_local_entries(project_dir, args.bib, args.bbl, args.tex)
    verifier = Verifier(sleep_ms=args.sleep_ms)

    out_entries: list[dict[str, Any]] = []
    metadata_issue_count = 0
    critical_issue_count = 0
    advisory_issue_count = 0
    all_real = True
    no_metadata_errors = True

    for idx, entry in enumerate(entries, start=1):
        result = verifier.verify(entry)
        metadata_issues = result.get("metadata_issues", [])
        critical_issues = result.get("critical_issues", [])
        advisory_issues = result.get("advisory_issues", [])
        metadata_issue_count += len(metadata_issues)
        critical_issue_count += len(critical_issues)
        advisory_issue_count += len(advisory_issues)
        if critical_issues:
            no_metadata_errors = False
        if result["status"] != "confirmed":
            all_real = False
        out_entries.append(
            {
                "key": entry.key,
                "entry_type": entry.entry_type,
                "local_fields": entry.fields,
                "bibliography_text": entry.bibliography_text,
                "status": result["status"],
                "evidence_label": result["evidence_label"],
                "source_type": result["source_type"],
                "source_url": result["source_url"],
                "matched_metadata": result.get("matched_metadata", {}),
                "metadata_issues": metadata_issues,
                "critical_issues": critical_issues,
                "advisory_issues": advisory_issues,
                "reason": result.get("reason", ""),
            }
        )
        if idx % 5 == 0 or idx == len(entries):
            print(f"Verified {idx}/{len(entries)}: {entry.key} -> {result['status']}", flush=True)

    data = {
        "paper_title": args.paper_title or inferred_title or "",
        "venue": args.venue,
        "verification_date": args.verification_date,
        "all_real": all_real,
        "no_metadata_errors": no_metadata_errors,
        "metadata_issue_count": metadata_issue_count,
        "critical_issue_count": critical_issue_count,
        "advisory_issue_count": advisory_issue_count,
        "entries": out_entries,
    }
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Verification JSON: {output_path}", flush=True)
    print(f"Entries: {len(out_entries)}", flush=True)
    print(f"All real: {all_real}", flush=True)
    print(
        f"Metadata issues: {metadata_issue_count} (critical={critical_issue_count}, advisory={advisory_issue_count})",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
