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

from shared.obsidian.vault_paths import DEFAULT_VAULT, formal_reading_path
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

READING_QUESTIONS = [
    "What is the problem?",
    "Why it matters?",
    "Why existing works fail?",
    "What is the key idea?",
    "What is the design?",
    "What is the experimental plan?",
    "What is the takeaway?",
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


def clip_text(text: str, limit: int = 360) -> str:
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
    enhanced_path = formal_reading_path(title, vault, paper_id=paper_id, note_id=note.get("id"))
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
        "tags": ["paper-note", "paperquay-import", "reading-note"],
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


def summarize_entries(entries: list[dict[str, Any]], text_key: str, *, limit: int = 4, per_item: int = 200) -> str:
    parts: list[str] = []
    for item in entries[:limit]:
        label = section_label(item) if item.get("heading") else figure_label(item)
        body = clip_text(item.get(text_key) or item.get("caption") or item.get("snippet") or "", per_item)
        if body:
            parts.append(f"{label}，可用于说明：{body}")
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


def summarize_alignment(alignment: list[dict[str, Any]], limit: int = 4) -> str:
    parts: list[str] = []
    for item in alignment[:limit]:
        note_text = clip_text(item.get("note_text") or "", 90)
        section_hits = item.get("section_evidence") or []
        block_hits = item.get("block_evidence") or []
        evidence_bits: list[str] = []
        if section_hits:
            first = section_hits[0]
            evidence_bits.append(
                f"{section_label(first)}（可核对该理解是否对应正文主线）"
            )
        if block_hits:
            first_block = block_hits[0]
            evidence_bits.append(
                f"{normalize_text(first_block.get('anchor') or '相关块')}（可补局部描述或图表锚点）"
            )
        if note_text and evidence_bits:
            parts.append(f"笔记点“{note_text}”可回钩到{'；'.join(evidence_bits)}")
    return "；".join(parts)


def format_alignment_evidence(alignment: list[dict[str, Any]], limit: int = 4) -> list[str]:
    rows: list[str] = []
    for item in alignment[:limit]:
        note_text = clip_text(item.get("note_text") or "", 90)
        section_hits = item.get("section_evidence") or []
        if not note_text or not section_hits:
            continue
        rows.append(f"原笔记点“{note_text}”优先回看 `{section_label(section_hits[0])}`。")
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


def build_experiment_claim_checklist(evidence: dict[str, Any]) -> list[str]:
    main_figures = evidence.get("main_figures") or evidence.get("figure_index") or []
    checklist: list[str] = []
    for item in main_figures[:8]:
        label = figure_label(item)
        caption = clip_text(item.get("caption") or "", 120)
        checklist.append(f"`{label}`: 要说明它验证的 claim、比较对象、指标口径，以及结论边界。线索：{caption}")
    return checklist


def build_question_outline(evidence: dict[str, Any]) -> dict[str, str]:
    metadata = evidence.get("metadata") or {}
    sections = parse_markdown_sections(metadata.get("abstract") or "")
    method_sections = evidence.get("method_sections") or []
    experiment_sections = evidence.get("experiment_sections") or []
    related_sections = evidence.get("related_sections") or []
    gap_sections = evidence.get("gap_sections") or []
    method_blocks = evidence.get("method_blocks") or []
    experiment_blocks = evidence.get("experiment_blocks") or []
    figure_index = evidence.get("main_figures") or evidence.get("figure_index") or []
    note_alignment = evidence.get("note_alignment") or []

    design_evidence = format_labels(method_sections, limit=5)
    method_block_evidence = format_labels(method_blocks, limit=4)
    figure_evidence = format_labels(figure_index, limit=6)
    experiment_evidence = format_labels(experiment_sections, limit=5)
    experiment_block_evidence = format_labels(experiment_blocks, limit=5)
    related_evidence = format_labels(related_sections, limit=4)
    gap_evidence = format_labels(gap_sections, limit=4)
    alignment_evidence = summarize_alignment(note_alignment, limit=4)

    return {
        "What is the problem?": str(sections.get("Research Problem") or "").strip(),
        "Why it matters?": str(sections.get("Background") or "").strip(),
        "Why existing works fail?": (
            "这一问必须拆成两层来讲：第一层是自回归起草器与并行起草器各自的结构性代价，第二层是这些代价为什么会在系统层面变成真实瓶颈。"
            + (f" 可优先从这些正文段落组织论证：{related_evidence}。" if related_evidence else "")
            + " 需要明确区分“现象”“原因”“真正的问题本体”，不要把接受率下降、吞吐下降这些现象直接当成根因。"
            + (f" 如果原笔记已有对应观察，可先从这些笔记-证据对齐点展开：{alignment_evidence}。" if alignment_evidence else "")
        ).strip(),
        "What is the key idea?": str(sections.get("Approach") or "").strip(),
        "What is the design?": (
            "这一问要按完整执行链写，不要只列模块名。至少要讲清楚：方法要优化什么目标；输入、状态与输出是如何流动的；"
            "哪些模块负责生成/更新候选，哪些模块负责约束、筛选、调度或验证；各模块之间如何串起来；每个关键设计到底在补哪一层短板；"
            "默认方案为什么成立、替代方案为什么没有被选中；以及这套设计在真实系统里依赖哪些实现前提。"
            + (f" 可优先使用的方法 section 证据：{design_evidence}。" if design_evidence else "")
            + (f" 可补充的方法 block 证据：{method_block_evidence}。" if method_block_evidence else "")
            + (f" 若图表里有 architecture / workflow / overview / algorithm 图，优先利用这些图表：{figure_evidence}。" if figure_evidence else "")
            + " 需要像旧 paper-analyze 一样解释每一步为什么这样设计、带来什么收益、代价落在哪里，并让读者看完后能够复述完整方法流程。"
        ).strip(),
        "What is the experimental plan?": (
            "这一问不仅要列实验设置，还要说明每组实验各自在验证什么 claim。建议至少覆盖五层：基础设置公平性、离线主结果、机制分析、confidence/scheduler 诊断、线上系统验证。"
            + (f" 可先组织这些实验 section：{experiment_evidence}。" if experiment_evidence else "")
            + (f" 对应的实验 block 证据：{experiment_block_evidence}。" if experiment_block_evidence else "")
            + (f" 图表证据可从这里抽主线：{figure_evidence}。" if figure_evidence else "")
            + " 需要覆盖主要 figure/table，而不是只挑亮点结果。每一组结果都要交代指标口径、比较对象、能支持到什么结论、结论边界在哪里，并把正文里的关键图表逐个挂到对应 claim 上。"
        ).strip(),
        "What is the takeaway?": (
            str(sections.get("Takeaways") or sections.get("Conclusions") or "").strip()
            + (f" 同时可结合这些 limitation / gap 线索收紧结论边界：{gap_evidence}。" if gap_evidence else "")
        ).strip(),
    }


def build_reader_prompt(note: dict, paper: dict | None, manifest: dict, evidence: dict) -> str:
    title = (paper or {}).get("title") or note.get("title") or "Untitled Paper"
    outline = build_question_outline(evidence)
    method_sections = evidence.get("method_sections") or []
    experiment_sections = evidence.get("experiment_sections") or []
    related_sections = evidence.get("related_sections") or []
    gap_sections = evidence.get("gap_sections") or []
    note_alignment = evidence.get("note_alignment") or []
    main_figures = evidence.get("main_figures") or evidence.get("figure_index") or []

    lines = [
        build_frontmatter(note, paper, manifest),
        "",
        f"# {title}",
        "",
        "> 这是写给当前主模型的正式写作合同，而不是最终成品。脚本只负责收集证据，不负责调用任何额外模型。",
        "",
        "## 写作合同",
        "",
        "- 最终正式笔记必须以 `导师七问` 为主体结构，只保留 `你当前笔记的遗漏与纠偏` 作为额外主 section。",
        "- 不要生成 `综述五字段`、`人工阅读重点`、`分析框架图`、`一句话总结`、`资产分类判断 + 原因` 等旧字段。",
        "- `What is the design?` 和 `What is the experimental plan?` 是最重要的两问，必须写得最扎实、最像在给组会讲方法。",
        "- 这份阅读笔记借用系统顶会审稿人的严谨工作方式，但第一目标是校正和增强你的原笔记，而不是先攻击原文。默认先检查当前笔记理解是否真的被正文证据支撑，必要时再收紧作者 claim。",
        "- 最终输出必须沿用旧 `paper-analyze` 的风格下限：不是摘要式 bullet，而是证据充足、机制完整、能回答问题链条的中文长段解释。",
        "- 原笔记不要整段照搬进正式笔记。正确流程是：先理解原笔记，再去正文证据里核对、纠偏、补全，最后填回正式结构。",
        "- 所有判断都必须能回指到 `full.md` / `content_list_v2.json` 对应证据；如果证据不足，要明确写“当前正文证据不足以支持更强结论”。",
        "- `你当前笔记的遗漏与纠偏` 必须逐条指出原笔记里的遗漏、层级混淆、因果错置、术语不严谨、过强结论，并给出对应正文锚点。",
        "",
        "## 可用证据",
        "",
        f"- 原始导出笔记：`{manifest.get('paperquay_note_id')}` 对应目录下的 `original.md`",
        f"- 正文 Markdown：`{manifest.get('mineru_md') or '缺失'}`",
        f"- 结构化块：`{evidence.get('content_json_path') or '缺失'}`",
        f"- 图表索引数量：{len(evidence.get('figure_index') or [])}",
        f"- 笔记-正文对齐点数量：{len(evidence.get('note_alignment') or [])}",
        "",
        "## 证据工作台",
        "",
        "### 问题与相关工作线索",
    ]
    for bullet in format_evidence_list(related_sections, "snippet", limit=4, per_item=150):
        lines.append(f"- {bullet}")
    if not related_sections:
        lines.append("- 当前未抽到稳定的相关工作/动机段落，需要你自行回看正文主线。")
    lines.extend(
        [
            "",
            "### 方法与设计线索",
        ]
    )
    for bullet in format_evidence_list(method_sections, "snippet", limit=5, per_item=150):
        lines.append(f"- {bullet}")
    if not method_sections:
        lines.append("- 当前未抽到稳定的方法小节，请直接回看 `full.md` 中的方法主段。")
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
        lines.append("- 当前实验线索不足，请直接沿正文实验部分自建 claim-to-evidence 映射。")
    lines.extend(
        [
            "",
            "### 局限与结论边界线索",
        ]
    )
    for bullet in format_evidence_list(gap_sections, "snippet", limit=4, per_item=150):
        lines.append(f"- {bullet}")
    if not gap_sections:
        lines.append("- 当前未抽到稳定的局限/讨论段落，注意主动收紧结论边界。")
    lines.extend(
        [
            "",
            "### 原笔记回钩线索",
        ]
    )
    for bullet in format_alignment_evidence(note_alignment, limit=4):
        lines.append(f"- {bullet}")
    if not note_alignment:
        lines.append("- 当前没有稳定的笔记-正文对齐点，需要你直接从原笔记逐条回正文核对。")
    lines.extend(
        [
            "",
            "## 导师七问",
            "",
        ]
    )
    for idx, question in enumerate(READING_QUESTIONS, 1):
        hint = outline.get(question) or "请基于原笔记与正文证据完成该问，避免空泛摘要。"
        lines.extend(
            [
                f"### {idx}. {question}",
                f"写作提示：{hint}",
                "",
            ]
        )
    lines.extend(
        [
            "## 你当前笔记的遗漏与纠偏",
            "必须逐条输出，每条都包含四部分：`原笔记表述`、`问题类型`、`正文证据`、`修正后的更严谨表述`。",
            "重点检查：",
            "- 是否把问题现象误当成真正问题。",
            "- 是否把作者方法结果误说成原因。",
            "- 是否把论文没证明的东西说成已经成立。",
            "- 是否漏掉关键设计环节、关键实验边界、关键失败条件。",
            "",
            "## 成稿要求",
            "",
            "- 元数据直接用 frontmatter，不要再单独复制一遍“论文基本信息”。",
            "- 每一问都尽量回答“问题是什么、机制是什么、证据是什么、边界在哪里”。",
            "- 即使是阅读笔记，也要借用审稿人的严谨标准来校正原笔记：概念要严、证据要硬、结论要收紧、遗漏要补齐；但主目标始终是纠正你的理解，而不是先对论文发起攻击。",
            "- `What is the design?` 要让读者看完后能复述系统从输入到验证完成的执行路径。",
            "- `What is the experimental plan?` 要把主要图表和实验职责讲清楚，尤其是它们分别支撑哪个 claim。",
            "- 如果正文图表识别不全，必须诚实说明当前 Markdown 证据边界，不得自行脑补 Appendix 或缺失图。",
            "",
            "## 图表-Claim 覆盖清单",
            "",
        ]
    )
    for bullet in build_experiment_claim_checklist(evidence):
        lines.append(f"- {bullet}")
    if not main_figures:
        lines.append("- 当前没有可靠图表索引，实验计划部分必须显式说明这一证据边界。")
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

    enhanced_path = formal_reading_path(title, vault, paper_id=paper_id, note_id=note.get("id"))
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
    prompt_path.write_text(build_reader_prompt(note, paper, manifest, evidence), encoding="utf-8")

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
