from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.obsidian.vault_paths import DEFAULT_VAULT, formal_review_path
from shared.paperquay.evidence_schema import build_paperquay_evidence_bundle
from shared.paperquay.legacy_skill_bridge import build_manifest_like
from shared.paperquay.library_reader import LibraryReader
from shared.paperquay.mineru_cache_locator import resolve_cache_bundle
from shared.paperquay.note_matcher import NoteMatcher
from shared.paperquay.note_to_markdown import tiptap_to_markdown
from shared.paperquay.paper_matcher import PaperMatcher


def resolve_paperquay_root() -> Path:
    configured = os.environ.get("PAPERQUAY_ROOT", "").strip()
    if configured:
        return Path(configured)
    appdata = os.environ.get("APPDATA", "").strip()
    if appdata:
        return Path(appdata) / "PaperQuay" / "PaperQuay"
    return Path.home() / "AppData" / "Roaming" / "PaperQuay" / "PaperQuay"


PAPERQUAY_ROOT = resolve_paperquay_root()

REVIEW_SECTIONS = [
    "Summary and High Level Discussion",
    "Strengths",
    "Weaknesses",
    "Comments for Rebuttal",
    "Detailed Comments for Authors",
    "Scored Review Questions",
    "Reproducibility",
    "Confidential Comments to the Program Committee",
    "你当前审稿笔记的遗漏与纠偏",
]

SUMMARY_HEADINGS = [
    "Overview",
    "Background",
    "Research Problem",
    "Approach",
    "Experiment Setup",
    "Key Findings",
    "Conclusions",
    "Limitations",
    "Takeaways",
    "Keywords",
]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def clip_text(text: str, limit: int = 320) -> str:
    normalized = normalize_text(text)
    if len(normalized) <= limit:
        return normalized
    window = normalized[:limit]
    cut = max(window.rfind("。"), window.rfind("；"), window.rfind("."), window.rfind(";"))
    if cut >= int(limit * 0.55):
        return window[: cut + 1].strip()
    return window.strip()


def section_label(item: dict[str, Any]) -> str:
    heading = normalize_text(item.get("heading") or "")
    if not heading:
        return "未命名小节"
    return heading


def figure_label(item: dict[str, Any]) -> str:
    kind = normalize_text(item.get("kind") or "figure").lower()
    number = normalize_text(item.get("number") or "")
    page = item.get("page")
    if not number:
        caption = normalize_text(item.get("caption") or item.get("snippet") or "")
        match = re.search(r"(?i)\b(figure|table|algorithm)\s+(\d+[a-z]?)\b", caption)
        if match:
            kind = match.group(1).lower()
            number = match.group(2).lower()
    if number:
        return f"{kind.capitalize()} {number}"
    if page is not None:
        return f"{kind.capitalize()} p{page}"
    return kind.capitalize()


def parse_markdown_sections(text: str) -> dict[str, str]:
    source = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    pattern = re.compile(
        r"##\s*(" + "|".join(re.escape(item) for item in SUMMARY_HEADINGS) + r")\s*(.*?)(?=##\s*(?:"
        + "|".join(re.escape(item) for item in SUMMARY_HEADINGS)
        + r")\s*|\Z)",
        re.S,
    )
    sections: dict[str, str] = {}
    for match in pattern.finditer(source):
        sections[match.group(1).strip()] = normalize_text(match.group(2))
    return sections


def export_original_note(note: dict, title: str, vault: Path, paper_id: str | None) -> tuple[str, Path]:
    note_markdown = tiptap_to_markdown(note.get("content_json")) or (note.get("content_text") or "")
    enhanced_path = formal_review_path(title, vault, paper_id=paper_id, note_id=note.get("id"))
    original_path = enhanced_path.with_name("original.md")
    original_path.parent.mkdir(parents=True, exist_ok=True)
    original_path.write_text(note_markdown, encoding="utf-8")
    return note_markdown, original_path


def build_frontmatter(note: dict, paper: dict | None, manifest: dict) -> str:
    metadata = {
        "title": (paper or {}).get("title") or note.get("title") or "Untitled Paper",
        "paper_id": manifest.get("paper_id"),
        "paperquay_note_id": note.get("id"),
        "authors": manifest.get("authors"),
        "year": manifest.get("year"),
        "venue": manifest.get("venue"),
        "domain": manifest.get("domain"),
        "source_url": manifest.get("source_url") or "",
        "pdf": manifest.get("pdf") or "",
        "mineru_md": manifest.get("mineru_md") or "",
        "cache_dir": manifest.get("paperquay_cache_dir") or "",
        "tags": ["paper-note", "paperquay-import", "review-note"],
    }
    lines = ["---"]
    for key, value in metadata.items():
        if key == "tags":
            lines.append("tags:")
            for item in value:
                lines.append(f"  - {item}")
            continue
        escaped = str(value or "").replace('"', '\\"')
        lines.append(f'{key}: "{escaped}"')
    lines.append("---")
    return "\n".join(lines)


def summarize_entries(entries: list[dict[str, Any]], text_key: str, *, limit: int = 4, per_item: int = 160) -> str:
    parts: list[str] = []
    for item in entries[:limit]:
        label = section_label(item) if item.get("heading") else figure_label(item)
        body = clip_text(item.get(text_key) or item.get("caption") or item.get("snippet") or "", per_item)
        if body:
            parts.append(f"{label}，可用于核对：{body}")
        else:
            parts.append(label)
    return "；".join(parts)


def format_evidence_list(entries: list[dict[str, Any]], text_key: str, *, limit: int = 5, per_item: int = 150) -> list[str]:
    bullets: list[str] = []
    for item in entries[:limit]:
        label = section_label(item) if item.get("heading") else figure_label(item)
        body = clip_text(item.get(text_key) or item.get("caption") or item.get("snippet") or "", per_item)
        if body:
            bullets.append(f"`{label}`: {body}")
        else:
            bullets.append(f"`{label}`")
    return bullets


def summarize_alignment(alignment: list[dict[str, Any]], limit: int = 5) -> str:
    parts: list[str] = []
    for item in alignment[:limit]:
        note_text = clip_text(item.get("note_text") or "", 90)
        section_hits = item.get("section_evidence") or []
        if not note_text or not section_hits:
            continue
        first = section_hits[0]
        parts.append(
            f"笔记点“{note_text}”可先回看 {section_label(first)}，检查当前批评是否真的由正文支撑"
        )
    return "；".join(parts)


def format_alignment_evidence(alignment: list[dict[str, Any]], limit: int = 5) -> list[str]:
    rows: list[str] = []
    for item in alignment[:limit]:
        note_text = clip_text(item.get("note_text") or "", 90)
        section_hits = item.get("section_evidence") or []
        if not note_text or not section_hits:
            continue
        rows.append(f"原审稿点“{note_text}”优先回看 `{section_label(section_hits[0])}`。")
    return rows


def format_labels(entries: list[dict[str, Any]], *, limit: int = 6) -> str:
    labels: list[str] = []
    seen: set[str] = set()
    for item in entries[:limit]:
        label = section_label(item) if item.get("heading") else figure_label(item)
        if label in seen:
            continue
        seen.add(label)
        labels.append(label)
    return "、".join(f"`{label}`" for label in labels if label)


def build_internal_review_backbone(evidence: dict[str, Any]) -> list[str]:
    main_figures = evidence.get("main_figures") or evidence.get("figure_index") or []
    prompts = [
        "1. What is the problem? 先回答论文真正要解决的总问题，不要把现象误写成问题本体。",
        "2. Why it matters? 说明这个问题为什么会影响系统价值、方法价值或部署价值。",
        "3. Why existing works fail? 把已有路线的结构性代价、实验盲区和系统代价分开讲。",
        "4. What is the key idea? 用一段话概括作者的核心解法与主要控制变量。",
        "5. What is the design? 讲完整设计链条，指出每个关键模块补的是哪层短板、代价是什么、默认方案为什么成立。",
        "6. What is the experimental plan? 把实验分成几组 claim，并明确主要图表/表格分别在验证什么。",
        "7. What is the takeaway? 写清楚结论、适用边界和哪些 claim 还只在特定系统条件下成立。",
    ]
    if main_figures:
        prompts.append(
            "图表覆盖提醒：至少把这些关键图表挂到内部七问里，再转成审稿意见。"
        )
        for item in main_figures[:6]:
            prompts.append(f"- `{figure_label(item)}`: {clip_text(item.get('caption') or '', 120)}")
    return prompts


def build_review_prompt(note: dict, paper: dict | None, manifest: dict, evidence: dict) -> str:
    title = (paper or {}).get("title") or note.get("title") or "Untitled Paper"
    metadata = evidence.get("metadata") or {}
    summary_sections = parse_markdown_sections(metadata.get("abstract") or "")
    related_sections = evidence.get("related_sections") or []
    method_sections = evidence.get("method_sections") or []
    experiment_sections = evidence.get("experiment_sections") or []
    gap_sections = evidence.get("gap_sections") or []
    figure_index = evidence.get("figure_index") or []
    main_figures = evidence.get("main_figures") or figure_index
    note_alignment = evidence.get("note_alignment") or []

    overview_hint = str(summary_sections.get("Overview") or summary_sections.get("Research Problem") or "").strip()
    method_hint = format_labels(method_sections, limit=5)
    experiment_hint = format_labels(experiment_sections, limit=5)
    related_hint = format_labels(related_sections, limit=4)
    gap_hint = format_labels(gap_sections, limit=4)
    figure_hint = format_labels(main_figures, limit=6)
    alignment_hint = summarize_alignment(note_alignment, limit=5)

    lines = [
        build_frontmatter(note, paper, manifest),
        "",
        f"# Review: {title}",
        "",
        "> 这是给当前主模型的审稿写作合同。脚本只收集证据，不在代码里调用任何额外模型。",
        "",
        "## 审稿合同",
        "",
        "- 先在内部完成一版“七问式增强理解”，尤其要把 `What is the problem?`、`What is the design?`、`What is the experimental plan?` 真正想清楚，再把这份理解转译成正式 review。这个内部七问理解不要原样输出成最终 review section，但它应当支撑后面的全部判断。",
        "- 这份内部七问增强理解，质量和水准必须与 reading-note-builder 产出的正式七问笔记对齐，不能因为最后要写 review 就降低理解深度或证据密度。",
        "- 审稿风格对齐旧 `paper-review`：像真正的顶会系统 reviewer 一样写，而不是做论文摘要。",
        "- 站在系统顶会审稿人的视角去做判断：严格、严谨、细致、认真，优先检查 soundness、边界、实验支撑、工程代价与 claim 是否匹配。",
        "- Appendix 不是本轮重点，不要把主要精力放在 Appendix 挖掘上；先把主文中能决定接收判断的核心证据吃透。",
        "- 每一句关键批评都必须能在 `full.md` 或 `content_list_v2.json` 中找到证据锚点，找不到就不要下重结论。",
        "- 原审稿笔记不是事实来源，只是待校正草稿。要主动指出它哪里过强、过弱、漏抓关键缺陷、误读作者论点。",
        "- 优先抓 soundness、comparison fairness、evaluation boundary、deployment realism、reproducibility，而不是纠缠措辞。",
        "- 如果正文证据不足以支持强批评，要明确写成“当前正文证据不足”，不要把怀疑直接写成定论。",
        "",
        "## 可用证据",
        "",
        f"- 原始导出笔记：`{manifest.get('paperquay_note_id')}` 对应目录下的 `original.md`",
        f"- 正文 Markdown：`{manifest.get('mineru_md') or '缺失'}`",
        f"- 结构化块：`{evidence.get('content_json_path') or '缺失'}`",
        f"- 图表索引数量：{len(figure_index)}",
        f"- 笔记-正文对齐点数量：{len(note_alignment)}",
        "",
        "## 内部理解骨架（不要原样输出）",
        "",
    ]
    for row in build_internal_review_backbone(evidence):
        if row.startswith("- "):
            lines.append(row)
        else:
            lines.append(f"- {row}")
    lines.extend(
        [
            "",
            "## 证据工作台",
            "",
            "### 方法与设计线索",
        ]
    )
    for bullet in format_evidence_list(method_sections, "snippet", limit=5, per_item=150):
        lines.append(f"- {bullet}")
    if not method_sections:
        lines.append("- 当前未抽到稳定的方法小节，请直接回看正文方法主线。")
    lines.extend(
        [
            "",
            "### 实验与图表线索",
        ]
    )
    for bullet in format_evidence_list(experiment_sections, "snippet", limit=5, per_item=150):
        lines.append(f"- {bullet}")
    for bullet in format_evidence_list(main_figures, "caption", limit=6, per_item=120):
        lines.append(f"- {bullet}")
    if not experiment_sections and not main_figures:
        lines.append("- 当前实验线索不足，请直接沿正文实验部分重建 claim-to-evidence 映射。")
    lines.extend(
        [
            "",
            "### 相关工作、局限与边界线索",
        ]
    )
    for bullet in format_evidence_list(related_sections, "snippet", limit=4, per_item=150):
        lines.append(f"- {bullet}")
    for bullet in format_evidence_list(gap_sections, "snippet", limit=4, per_item=150):
        lines.append(f"- {bullet}")
    if not related_sections and not gap_sections:
        lines.append("- 当前未抽到稳定的相关工作/局限段落，注意主动收紧 claims。")
    lines.extend(
        [
            "",
            "### 原审稿笔记回钩线索",
        ]
    )
    for bullet in format_alignment_evidence(note_alignment, limit=5):
        lines.append(f"- {bullet}")
    if not note_alignment:
        lines.append("- 当前没有稳定的笔记-正文对齐点，需要你直接逐条回正文核对原审稿草稿。")
    lines.extend(
        [
            "",
        ]
    )
    for section in REVIEW_SECTIONS:
        lines.append(f"## {section}")
        if section == "Summary and High Level Discussion":
            lines.append(
                "写作提示：先给出总体判断与推荐动作，再解释决定性证据。这里应当建立在你已经完成的内部七问理解之上，尤其要把问题定义、方法链条和实验支撑范围压缩成审稿口径。"
                + (f" 论文主线可从这里起笔：{overview_hint}" if overview_hint else "")
            )
        elif section == "Strengths":
            lines.append(
                "写作提示：只保留真正被正文证据支撑的优点，例如问题重要、方法链条完整、实验覆盖到关键 claim、线上部署可信。可以把你内部七问中已经确认无误的设计亮点和实验亮点，压缩成 reviewer 会认可的 strengths。"
                + (f" 可优先参考的方法与实验证据：{method_hint}；{experiment_hint}" if method_hint or experiment_hint else "")
            )
        elif section == "Weaknesses":
            lines.append(
                "写作提示：这里要最严苛。按‘证据/缺失证据 -> 为什么构成方法或实验缺陷 -> 影响哪个审稿维度’来写。尤其利用你内部七问中的 `What is the design?` 与 `What is the experimental plan?` 去找设计链条断点、实验支撑不足和结论边界问题。"
                + (f" 可重点从这些相关工作/局限线索追问：{related_hint}；{gap_hint}" if related_hint or gap_hint else "")
                + (f" 如需图表交叉核验，可先看：{figure_hint}" if figure_hint else "")
            )
        elif section == "Comments for Rebuttal":
            lines.append("写作提示：只保留那些作者若能在 rebuttal 中回答清楚，就真的可能改变评分的问题。问题要具体、可验证、非空泛。")
        elif section == "Detailed Comments for Authors":
            lines.append("写作提示：给可执行改法，不要只说“请澄清”。要指出该补什么实验、该收紧什么 claim、该解释哪个机制。")
        elif section == "Scored Review Questions":
            lines.append("写作提示：分数必须和正文一致。若核心证据链不闭合，`Technical Soundness` 不应给高分。")
        elif section == "Reproducibility":
            lines.append("写作提示：检查实现细节、训练/部署设置、数据与基线公平性是否足以复现关键结论。")
        elif section == "Confidential Comments to the Program Committee":
            lines.append("写作提示：直说这篇稿件最关键的接收/拒稿原因，不要重复前文摘要。")
        elif section == "你当前审稿笔记的遗漏与纠偏":
            lines.append(
                "写作提示：逐条指出原审稿笔记哪里批评成立、哪里批评过强、哪里遗漏了更关键的问题、哪里把现象误说成根因。"
                + (f" 可先从这些对齐点入手：{alignment_hint}" if alignment_hint else "")
            )
        else:
            lines.append("写作提示：请基于原审稿笔记与正文证据完成本节。")
        lines.append("")
    lines.extend(
        [
            "## 审稿底线",
            "",
            "- 不要把没有证据的怀疑包装成确定性 weakness。",
            "- 不要把小 typo 或表述问题伪装成决定性技术缺陷。",
            "- 不要复述原笔记，要做证据复核、查漏补缺和严苛重写。",
            "- 不要引用不存在的图表或 Appendix 内容；如果当前 Markdown 证据缺失，就直接说明边界。",
            "- review 的结论要能回溯到你内部完成的七问理解，尤其是 design 与 experiment 两问。",
            "- 如果这篇稿子在审稿人标准下经不起推敲，就要明确指出，而不是为了保持笔记顺滑而放松标准。",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def build_mapping_report(note: dict, paper: dict | None, cache: dict | None, resolution: dict | None, manifest: dict) -> dict[str, Any]:
    return {
        "note_id": note.get("id"),
        "note_title": note.get("title"),
        "selected_paper_id": (paper or {}).get("id"),
        "selected_paper_title": (paper or {}).get("title"),
        "resolution": resolution or {},
        "cache_dir": (cache or {}).get("cache_dir"),
        "mineru_md": manifest.get("mineru_md"),
        "pdf": manifest.get("pdf"),
    }


def build_paper_summary(note: dict, paper: dict | None, manifest: dict, evidence: dict) -> dict[str, Any]:
    metadata = evidence.get("metadata") or {}
    sections = parse_markdown_sections(metadata.get("abstract") or "")
    return {
        "title": metadata.get("title") or (paper or {}).get("title") or note.get("title"),
        "paper_id": metadata.get("paper_id") or manifest.get("paper_id"),
        "authors": metadata.get("authors") or [],
        "year": metadata.get("year") or manifest.get("year"),
        "venue": metadata.get("venue") or manifest.get("venue"),
        "source_url": metadata.get("paper_url") or manifest.get("source_url"),
        "paperquay_summary_sections": sections,
        "pdf": manifest.get("pdf"),
        "mineru_md": manifest.get("mineru_md"),
        "cache_dir": manifest.get("paperquay_cache_dir"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--note-id", required=True)
    parser.add_argument("--vault", default=str(DEFAULT_VAULT))
    args = parser.parse_args()

    vault = Path(args.vault)
    matcher = NoteMatcher(PAPERQUAY_ROOT)
    note = matcher.by_note_id(args.note_id)
    if not note:
        raise SystemExit(f"Note not found: {args.note_id}")

    library = LibraryReader(PAPERQUAY_ROOT)
    match = PaperMatcher(library).resolve_from_note_details(note)
    paper = match.get("paper")
    resolution = match.get("resolution") or {}
    cache = resolve_cache_bundle(paper) if paper else None

    title = (paper or {}).get("title") or note.get("title") or "Untitled Paper"
    paper_id = (paper or {}).get("id") or note.get("paper_id")
    note_markdown, original_path = export_original_note(note, title, vault, paper_id)
    manifest = build_manifest_like(note, paper, cache, resolution, vault)

    enhanced_path = formal_review_path(title, vault, paper_id=paper_id, note_id=note.get("id"))
    support_dir = enhanced_path.parent
    support_dir.mkdir(parents=True, exist_ok=True)

    mineru_md = manifest.get("mineru_md")
    evidence = build_paperquay_evidence_bundle(note, paper, cache, note_markdown) if mineru_md and Path(mineru_md).exists() else {}

    evidence_path = support_dir / "evidence_bundle.json"
    mapping_path = support_dir / "mapping_report.json"
    summary_path = support_dir / "paper_summary.json"
    prompt_path = support_dir / "writer_prompt.md"

    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    mapping_path.write_text(
        json.dumps(build_mapping_report(note, paper, cache, resolution, manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    summary_path.write_text(
        json.dumps(build_paper_summary(note, paper, manifest, evidence), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    prompt_path.write_text(build_review_prompt(note, paper, manifest, evidence), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "evidence-collected",
                "note_id": note["id"],
                "paper_id": (paper or {}).get("id"),
                "resolution": resolution,
                "cache_dir": (cache or {}).get("cache_dir"),
                "original_note_md": str(original_path),
                "evidence_bundle": str(evidence_path),
                "mapping_report": str(mapping_path),
                "paper_summary": str(summary_path),
                "writer_prompt": str(prompt_path),
                "target_output_path": str(enhanced_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
