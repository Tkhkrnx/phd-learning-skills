"""Traceable metadata discovery and bibliography export; not citation verification."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote
import xml.etree.ElementTree as ET

import requests

from shared.search import paper_search as search

CROSSREF = "https://api.crossref.org/works"
PUBMED = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def normalize_doi(value: str | None) -> str:
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value or "", flags=re.I).strip().lower()


def crossref_record(item: dict) -> dict:
    parts = (item.get("published") or item.get("issued") or {}).get("date-parts") or [[]]
    return {
        "title": (item.get("title") or [""])[0], "year": parts[0][0] if parts[0] else None,
        "authors": [{"name": " ".join(filter(None, (a.get("given"), a.get("family")))) or a.get("name", "")} for a in item.get("author", [])],
        "venue": (item.get("container-title") or [""])[0], "type": item.get("type"),
        "volume": item.get("volume"), "issue": item.get("issue"), "pages": item.get("page"),
        "externalIds": {"DOI": item.get("DOI")}, "url": item.get("URL"),
    }


def query_crossref(query: str, limit: int, min_year: int | None = None) -> list[dict]:
    params = {"query.bibliographic": query, "rows": limit}
    if min_year:
        params["filter"] = f"from-pub-date:{min_year}-01-01"
    response = search.make_session().get(CROSSREF, params=params, timeout=20)
    response.raise_for_status()
    return [crossref_record(item) for item in response.json()["message"]["items"]]


def query_pubmed(query: str, limit: int, min_year: int | None = None) -> list[dict]:
    session = search.make_session()
    params = {"db": "pubmed", "term": query, "retmax": limit, "retmode": "json", "tool": "phd-learning-skills"}
    if min_year:
        params.update({"mindate": str(min_year), "datetype": "pdat", "maxdate": "3000"})
    response = session.get(PUBMED + "esearch.fcgi", params=params, timeout=20)
    response.raise_for_status()
    ids = response.json()["esearchresult"]["idlist"]
    if not ids:
        return []
    response = session.get(PUBMED + "efetch.fcgi", params={"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}, timeout=20)
    response.raise_for_status()
    tree = ET.fromstring(response.text)
    rows = []
    for article in tree.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.find(".//ArticleTitle")
        year = article.findtext(".//JournalIssue/PubDate/Year")
        if not year:
            match = re.search(r"\b\d{4}\b", article.findtext(".//JournalIssue/PubDate/MedlineDate", ""))
            year = match.group() if match else None
        doi = next((node.text for node in article.findall(".//ArticleId") if node.get("IdType") == "doi"), None)
        authors = []
        for author in article.findall(".//AuthorList/Author"):
            name = author.findtext("CollectiveName") or " ".join(filter(None, (author.findtext("ForeName"), author.findtext("LastName"))))
            if name:
                authors.append({"name": name})
        rows.append({"title": "".join(title.itertext()) if title is not None else "", "year": int(year) if year else None,
                     "authors": authors, "venue": article.findtext(".//Journal/Title", ""), "type": "journal-article",
                     "externalIds": {"DOI": doi, "PMID": pmid}, "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"})
    return rows


def normalized_record(row: dict, provider: str) -> dict:
    ids = row.get("externalIds") or {}
    return {
        "title": str(row.get("title") or "").strip(), "year": row.get("year"),
        "authors": [a["name"] if isinstance(a, dict) else str(a) for a in row.get("authors") or []],
        "venue": "" if row.get("venue") in {None, "Unknown Venue", "Unknown"} else row["venue"],
        "doi": normalize_doi(ids.get("DOI") or row.get("doi")),
        "arxiv": ids.get("ArXiv"), "pmid": ids.get("PMID"), "url": row.get("url"),
        "type": row.get("type"), "volume": row.get("volume"), "issue": row.get("issue"), "pages": row.get("pages"),
        "status": "candidate", "provenance": [{"provider": provider, "url": row.get("url"), "paper_id": row.get("paperId")}],
        "conflicts": [],
    }


def title_key(title: str) -> str:
    return re.sub(r"[\W_]+", " ", title, flags=re.UNICODE).casefold().strip()


def merge_records(records: list[dict]) -> list[dict]:
    merged = []
    for record in records:
        if not record["title"]:
            continue
        existing = next((item for item in merged if (
            (record["doi"] and item["doi"] == record["doi"]) or
            (title_key(item["title"]) == title_key(record["title"]) and
             not (item["doi"] and record["doi"] and item["doi"] != record["doi"]) and
             not (item["year"] and record["year"] and item["year"] != record["year"]))
        )), None)
        if existing is None:
            merged.append(record)
            continue
        existing["provenance"].extend(record["provenance"])
        for field in ("title", "year", "authors", "venue", "doi", "arxiv", "pmid", "url", "type", "volume", "issue", "pages"):
            old, new = existing.get(field), record.get(field)
            if old and new and old != new and field != "url":
                existing["conflicts"].append({"field": field, "retained": old, "alternative": new, "provider": record["provenance"][0]["provider"]})
            elif not old and new:
                existing[field] = new
    for record in merged:
        identity = record["doi"] or f"{title_key(record['title'])}|{record['year']}"
        record["id"] = "ref" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    return merged


def discover(query: str, providers: list[str], limit: int, min_year: int | None = None) -> dict:
    registry = {"crossref": query_crossref, "pubmed": query_pubmed,
                "arxiv": search.query_arxiv, "openalex": search.query_openalex,
                "dblp": search.query_dblp, "semantic_scholar": search.query_semantic_scholar}
    if not query.strip() or not 1 <= limit <= 100 or not providers or any(p not in registry for p in providers):
        raise ValueError("nonempty query, known providers, and limit 1..100 required")
    records, coverage = [], []
    for provider in dict.fromkeys(providers):
        try:
            rows = registry[provider](query=query, limit=limit, min_year=min_year)
            records.extend(normalized_record(row, provider) for row in rows)
            coverage.append({"provider": provider, "status": "ok", "count": len(rows)})
        except (requests.RequestException, RuntimeError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
            coverage.append({"provider": provider, "status": "failed", "error": str(exc)})
    return {"schema_version": 1, "query": query, "providers": providers,
            "retrieved_at": datetime.now(timezone.utc).isoformat(), "min_year": min_year,
            "coverage": coverage, "records": merge_records(records), "verification": "not performed"}


def tex_escape(value: object) -> str:
    escapes = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "%": r"\%", "&": r"\&", "#": r"\#", "_": r"\_", "$": r"\$", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(escapes.get(char, char) for char in str(value).replace("\n", " ").replace("\r", " "))


def export_records(records: list[dict], fmt: str) -> str:
    if fmt not in {"bib", "ris"}:
        raise ValueError("unsupported export format")
    blocks = []
    for row in records:
        if fmt == "bib":
            kind = {"journal-article": "article", "proceedings-article": "inproceedings"}.get(row.get("type"), "misc")
            fields = {"title": row["title"], "author": " and ".join(row["authors"]), "year": row.get("year"),
                      "doi": row.get("doi"), "url": row.get("url"), "volume": row.get("volume"), "number": row.get("issue"), "pages": row.get("pages")}
            if row.get("venue") and kind != "misc":
                fields["journal" if kind == "article" else "booktitle"] = row["venue"]
            if row.get("arxiv"):
                fields.update({"eprint": row["arxiv"], "archivePrefix": "arXiv"})
            encoded = {k: (str(v).replace("\n", "").replace("\r", "") if k in {"doi", "url", "eprint"} else tex_escape(v)) for k, v in fields.items() if v}
            if any("{" in encoded[k] or "}" in encoded[k] for k in ("doi", "url", "eprint") if k in encoded):
                raise ValueError("identifier contains unencoded braces; inspect the source metadata")
            blocks.append("@" + kind + "{" + row["id"] + ",\n" + ",\n".join(f"  {k} = {{{v}}}" for k, v in encoded.items()) + "\n}")
        else:
            kind = {"journal-article": "JOUR", "proceedings-article": "CONF"}.get(row.get("type"), "GEN")
            fields = [("TY", kind), ("ID", row["id"]), ("TI", row["title"])] + [("AU", a) for a in row["authors"]]
            fields += [("PY", row.get("year")), ("DO", row.get("doi")), ("UR", row.get("url")), ("JO", row.get("venue"))]
            blocks.append("\n".join(f"{k}  - {str(v).replace(chr(10), ' ').replace(chr(13), ' ')}" for k, v in fields if v) + "\nER  -")
    return "\n\n".join(blocks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    find = commands.add_parser("search")
    find.add_argument("--query", required=True)
    find.add_argument("--sources", default="crossref,arxiv,openalex,dblp")
    find.add_argument("--limit", type=int, default=10)
    find.add_argument("--min-year", type=int)
    lookup = commands.add_parser("lookup")
    lookup.add_argument("--doi", required=True)
    export = commands.add_parser("export")
    export.add_argument("--input", type=Path, required=True)
    export.add_argument("--format", choices=("bib", "ris"), required=True)
    export.add_argument("--ids", nargs="+")
    for command in (find, lookup, export):
        command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        failed = False
        if args.command == "search":
            payload = discover(args.query, args.sources.split(","), args.limit, args.min_year)
            failed = all(c["status"] == "failed" for c in payload["coverage"])
            output = json.dumps(payload, ensure_ascii=False, indent=2)
        elif args.command == "lookup":
            doi = normalize_doi(args.doi)
            if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
                raise ValueError("invalid DOI")
            response = search.make_session().get(CROSSREF + "/" + quote(doi, safe=""), timeout=20)
            response.raise_for_status()
            payload = {"records": merge_records([normalized_record(crossref_record(response.json()["message"]), "crossref-doi")]), "verification": "metadata retrieved; manuscript match and claim support not checked"}
            output = json.dumps(payload, ensure_ascii=False, indent=2)
        else:
            records = json.loads(args.input.read_text(encoding="utf-8"))["records"]
            if args.ids:
                selected = set(args.ids)
                if selected - {r["id"] for r in records}:
                    raise ValueError("unknown selected record ID")
                records = [r for r in records if r["id"] in selected]
            if not records:
                raise ValueError("no records selected")
            output = export_records(records, args.format)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(output)
        print(f"output={args.output.resolve()}")
        return int(failed)
    except (OSError, ValueError, KeyError, TypeError, requests.RequestException) as exc:
        print(f"Academic search failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
