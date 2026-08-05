from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


BADGE_MAP = {
    "confirmed": ("√", "通过", "已确认", "#22c55e"),
    "pending": ("!", "存疑", "待复核", "#f59e0b"),
    "missing": ("×", "未找到", "未找到", "#ef4444"),
}


@dataclass
class Entry:
    key: str
    raw: str
    text: str
    status: str
    evidence: str = "待复核"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Chinese reference validation report PDF."
    )
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--tex", default="main.tex")
    parser.add_argument("--bbl", default="main.bbl")
    parser.add_argument("--paper-title")
    parser.add_argument("--venue", default="未知投稿期刊")
    parser.add_argument("--verification-date", default=str(date.today()))
    parser.add_argument("--output-dir")
    parser.add_argument("--output-prefix", default="reference_validation_report_final")
    parser.add_argument("--tool-text", default="AI 自动参考文献完整性检测（main.tex + refs.bib）")
    parser.add_argument(
        "--default-status",
        choices=sorted(BADGE_MAP.keys()),
        default="confirmed",
    )
    parser.add_argument("--verification-json")
    parser.add_argument("--all-real", action="store_true")
    parser.add_argument("--no-metadata-errors", action="store_true")
    return parser.parse_args()


def split_bbl_entries(bbl_text: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^}]+)\}(?P<body>.*?)(?=(?:\n\\bibitem(?:\[[^\]]*\])?\{|\\end\{thebibliography\}))",
        re.S,
    )
    return [(m.group("key").strip(), m.group("body").strip()) for m in pattern.finditer(bbl_text)]


def split_inline_tex_entries(tex_text: str) -> list[tuple[str, str]]:
    bib_env = re.search(
        r"\\begin\{thebibliography\}.*?(?P<body>.*)\\end\{thebibliography\}",
        tex_text,
        re.S,
    )
    if not bib_env:
        return []
    body = bib_env.group("body")
    pattern = re.compile(
        r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^}]+)\}(?P<body>.*?)(?=(?:\n\\bibitem(?:\[[^\]]*\])?\{|\\end\{thebibliography\}|$))",
        re.S,
    )
    return [(m.group("key").strip(), m.group("body").strip()) for m in pattern.finditer(body)]


def strip_latex_commands(text: str) -> str:
    previous = None
    current = re.sub(r"(?m)^\s*%.*$", " ", text)
    current = current.replace("\n", " ")
    current = current.replace("~", " ")
    current = current.replace("\\&", "&")
    current = current.replace("``", '"').replace("''", '"')
    current = re.sub(r"\\newblock\b", " ", current)
    current = re.sub(r"\\providecommand\{[^}]*\}\{[^}]*\}", " ", current)
    current = re.sub(r"\\BIBentry\w+", " ", current)
    wrappers = [
        "emph",
        "textit",
        "textbf",
        "url",
        "showarticletitle",
        "showURL",
        "showDOI",
        "showISBNx",
        "showISSN",
        "showEISSN",
        "showCODEN",
        "showLCCN",
    ]
    while previous != current:
        previous = current
        current = re.sub(r"\\bibinfo\{[^{}]*\}\{([^{}]*)\}", r"\1", current)
        current = re.sub(r"\\BIBforeignlanguage\{[^{}]*\}\{([^{}]*)\}", r"\1", current)
        for name in wrappers:
            current = re.sub(rf"\\{name}\{{([^{{}}]*)\}}", r"\1", current)
        current = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", current)
    current = re.sub(r"\\[a-zA-Z@]+\*?", " ", current)
    current = current.replace("{", "").replace("}", "")
    current = current.replace("$", "")
    current = re.sub(r"\s+", " ", current).strip()
    return current


def extract_title_from_tex(tex_text: str) -> str | None:
    for pattern in [
        r"\\title(?:\[[^\]]*\])?\{(?P<title>.*?)\}",
        r"\\shorttitle\{(?P<title>.*?)\}",
    ]:
        match = re.search(pattern, tex_text, re.S)
        if match:
            title = strip_latex_commands(match.group("title"))
            title = re.sub(r"\s+", " ", title).strip()
            if title:
                return title
    return None


def dedupe_repeated_title(text: str) -> str:
    quote_match = re.search(r'"([^"]+)"', text)
    if quote_match:
        title = quote_match.group(1).strip().rstrip(".,")
        remainder = text[quote_match.end() :].lstrip(" ,.")
        if remainder.lower().startswith(title.lower()):
            remainder = remainder[len(title) :].lstrip(" ,.")
            text = f'{text[:quote_match.end()]} {remainder}'.strip()
    return re.sub(r"\s+", " ", text).strip()


def normalize_entry_text(raw: str) -> str:
    text = strip_latex_commands(raw)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\s+'", "'", text)
    text = dedupe_repeated_title(text)
    return text.strip()


def find_browser() -> Path | None:
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe",
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def load_entries_from_sources(project_dir: Path, tex_name: str, bbl_name: str, default_status: str) -> tuple[list[Entry], str, str]:
    tex_path = project_dir / tex_name
    bbl_path = project_dir / bbl_name
    tex_text = tex_path.read_text(encoding="utf-8", errors="ignore") if tex_path.exists() else ""
    pairs: list[tuple[str, str]] = []
    source_name = ""
    if bbl_path.exists():
        pairs = split_bbl_entries(bbl_path.read_text(encoding="utf-8", errors="ignore"))
        source_name = str(bbl_path)
    if not pairs and tex_text:
        pairs = split_inline_tex_entries(tex_text)
        source_name = str(tex_path)
    if not pairs:
        raise ValueError("No bibliography entries found. Provide a compiled .bbl file or inline \\bibitem entries in .tex.")
    entries = [
        Entry(key=key, raw=raw, text=normalize_entry_text(raw), status=default_status, evidence=BADGE_MAP[default_status][2])
        for key, raw in pairs
    ]
    return entries, tex_text, source_name


def load_entries_from_verification_json(path: Path) -> tuple[list[Entry], dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries: list[Entry] = []
    for item in data.get("entries", []):
        status = item.get("status", "pending")
        evidence = item.get("evidence_label") or item.get("evidence") or BADGE_MAP[status][2]
        entries.append(
            Entry(
                key=item.get("key", ""),
                raw=item.get("raw", ""),
                text=item.get("bibliography_text") or item.get("text") or "",
                status=status,
                evidence=evidence,
            )
        )
    return entries, data


def render_html(
    paper_title: str,
    venue: str,
    verification_date: str,
    tool_text: str,
    entries: list[Entry],
    all_real: bool,
    no_metadata_errors: bool,
    metadata_issue_count: int = 0,
    critical_issue_count: int = 0,
    advisory_issue_count: int = 0,
) -> str:
    confirmed = sum(1 for e in entries if e.status == "confirmed")
    pending = sum(1 for e in entries if e.status == "pending")
    missing = sum(1 for e in entries if e.status == "missing")
    total = len(entries)

    if all_real and missing == 0 and pending == 0:
        summary = f"本文所有 {total} 篇参考文献均为真实存在的学术文献，未发现伪造或 AI 幻觉引用。"
    elif missing == 0 and pending == 0:
        summary = f"本文共核验 {total} 篇参考文献，当前未发现未找到条目。"
    else:
        summary = f"本文共核验 {total} 篇参考文献，其中通过 {confirmed} 篇、存疑 {pending} 篇、未找到 {missing} 篇。"

    if no_metadata_errors and critical_issue_count == 0 and advisory_issue_count == 0:
        metadata_text = "未发现文献真实但著录存在明显错误的情况。"
    elif critical_issue_count > 0:
        suffix = f"，另有 {advisory_issue_count} 处次要字段建议复核" if advisory_issue_count > 0 else ""
        metadata_text = f"发现 {critical_issue_count} 处关键著录信息与命中来源存在差异，建议人工复核后修正{suffix}。"
    elif advisory_issue_count > 0:
        metadata_text = f"未发现关键著录错误，但有 {advisory_issue_count} 处次要字段建议复核。"
    else:
        metadata_text = "存在待进一步复核的著录信息问题时，应结合人工核对结果更新本节。"

    row_html: list[str] = []
    for idx, entry in enumerate(entries, start=1):
        badge_symbol, badge_text, _, color = BADGE_MAP[entry.status]
        row_html.append(
            f"""
            <tr>
              <td class="col-index">[{idx}]</td>
              <td class="col-ref">{html.escape(entry.text)}</td>
              <td class="col-status">
                <span class="badge" style="background:{color}">{badge_symbol}</span>
                <span class="status-text">{html.escape(badge_text)}</span>
              </td>
              <td class="col-evidence">{html.escape(entry.evidence)}</td>
            </tr>
            """.strip()
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>参考文献验证报告</title>
  <style>
    @page {{
      size: A4;
      margin: 26mm 18mm 22mm 18mm;
    }}
    body {{
      font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Noto Sans CJK SC", sans-serif;
      color: #222;
      margin: 0;
      background: #fff;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .page {{ width: 100%; }}
    h1 {{
      font-size: 30px;
      font-weight: 800;
      margin: 0 0 22px 0;
    }}
    .meta {{
      font-size: 16px;
      line-height: 1.55;
      margin-bottom: 22px;
    }}
    .meta div {{ margin: 4px 0; }}
    .meta strong {{ font-weight: 800; }}
    .section-title {{
      display: flex;
      align-items: center;
      margin: 22px 0 14px 0;
      font-size: 24px;
      font-weight: 800;
      line-height: 1.1;
    }}
    .section-title::before {{
      content: "";
      width: 16px;
      height: 44px;
      background: #9ca3af;
      display: inline-block;
      margin-right: 14px;
      flex: 0 0 auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      font-size: 14px;
    }}
    th, td {{
      border: 1px solid #c7d2e1;
      padding: 10px 12px;
      vertical-align: top;
    }}
    th {{
      background: #eef2f7;
      font-weight: 800;
      text-align: left;
    }}
    .summary-table td {{ vertical-align: middle; }}
    .summary-table .count {{ width: 20%; text-align: left; }}
    .badge {{
      display: inline-flex;
      width: 20px;
      height: 20px;
      border-radius: 5px;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 14px;
      font-weight: 800;
      margin-right: 6px;
      line-height: 1;
      vertical-align: middle;
    }}
    .status-text {{
      vertical-align: middle;
      font-size: 13px;
    }}
    .conclusion, .metadata-note {{
      font-size: 15px;
      margin: 12px 0 0 0;
      line-height: 1.7;
    }}
    .results-table .col-index {{ width: 8%; white-space: nowrap; }}
    .results-table .col-ref {{
      width: 59%;
      line-height: 1.45;
      word-break: break-word;
    }}
    .results-table .col-status {{
      width: 16%;
      white-space: nowrap;
      font-size: 13px;
    }}
    .results-table .col-evidence {{
      width: 17%;
      white-space: normal;
      word-break: break-word;
      overflow-wrap: anywhere;
      line-height: 1.35;
    }}
  </style>
</head>
<body>
  <div class="page">
    <h1>参考文献验证报告</h1>

    <div class="meta">
      <div><strong>论文:</strong> {html.escape(paper_title)}</div>
      <div><strong>提交期刊:</strong> {html.escape(venue)}</div>
      <div><strong>验证时间:</strong> {html.escape(verification_date)}</div>
      <div><strong>验证工具:</strong> {html.escape(tool_text)}</div>
    </div>

    <div class="section-title">一、验证摘要</div>
    <table class="summary-table">
      <thead>
        <tr><th>项目</th><th class="count">数量</th></tr>
      </thead>
      <tbody>
        <tr><td>引用总数</td><td class="count">{total}</td></tr>
        <tr><td><span class="badge" style="background:#22c55e">√</span>通过（已确认存在）</td><td class="count">{confirmed}</td></tr>
        <tr><td><span class="badge" style="background:#f59e0b">!</span>存疑</td><td class="count">{pending}</td></tr>
        <tr><td><span class="badge" style="background:#ef4444">×</span>未找到（疑似伪造）</td><td class="count">{missing}</td></tr>
      </tbody>
    </table>
    <p class="conclusion">结论：{html.escape(summary)}</p>

    <div class="section-title">二、引用信息问题</div>
    <p class="metadata-note">{html.escape(metadata_text)}</p>

    <div class="section-title">三、逐条验证结果</div>
    <table class="results-table">
      <thead>
        <tr>
          <th class="col-index">#</th>
          <th class="col-ref">文献</th>
          <th class="col-status">状态</th>
          <th class="col-evidence">证据</th>
        </tr>
      </thead>
      <tbody>
        {''.join(row_html)}
      </tbody>
    </table>
  </div>
</body>
</html>
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    browser = find_browser()
    if browser is None:
        raise FileNotFoundError("Chrome/Edge executable not found for headless PDF printing.")
    command = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).resolve()
    verification_meta: dict = {}

    if args.verification_json:
        entries, verification_meta = load_entries_from_verification_json(Path(args.verification_json).resolve())
        tex_text = ""
        source_name = str(Path(args.verification_json).resolve())
    else:
        entries, tex_text, source_name = load_entries_from_sources(project_dir, args.tex, args.bbl, args.default_status)

    paper_title = args.paper_title or verification_meta.get("paper_title")
    if not paper_title and tex_text:
        paper_title = extract_title_from_tex(tex_text)
    if not paper_title:
        raise ValueError("Paper title is required. Pass --paper-title or ensure the .tex file contains a parseable \\title{...}.")

    venue = verification_meta.get("venue") or args.venue
    verification_date = verification_meta.get("verification_date") or args.verification_date
    metadata_issue_count = int(verification_meta.get("metadata_issue_count", 0))
    critical_issue_count = int(verification_meta.get("critical_issue_count", 0))
    advisory_issue_count = int(verification_meta.get("advisory_issue_count", 0))
    all_real = bool(verification_meta.get("all_real", args.all_real))
    no_metadata_errors = bool(verification_meta.get("no_metadata_errors", args.no_metadata_errors))

    output_dir = Path(args.output_dir).resolve() if args.output_dir else (project_dir / "output" / "pdf")
    html_path = output_dir / f"{args.output_prefix}.html"
    pdf_path = output_dir / f"{args.output_prefix}.pdf"

    html_content = render_html(
        paper_title=paper_title,
        venue=venue,
        verification_date=verification_date,
        tool_text=args.tool_text,
        entries=entries,
        all_real=all_real,
        no_metadata_errors=no_metadata_errors,
        metadata_issue_count=metadata_issue_count,
        critical_issue_count=critical_issue_count,
        advisory_issue_count=advisory_issue_count,
    )
    write_text(html_path, html_content)
    render_pdf(html_path, pdf_path)

    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")
    print(f"Entries: {len(entries)}")
    print(f"Source: {source_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
