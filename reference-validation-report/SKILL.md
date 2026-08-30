---
name: reference-validation-report
description: "Explicit skill-use request only: top-level activation requires the user to explicitly ask to use, call, or apply a reference-validation, bibliography-validation, 参考文献验证, or equivalent skill to a stated paper task; the exact identifier is optional. An ordinary request to check citations is not authorization. An already authorized primary skill may invoke this skill as a bounded supporting dependency for the same goal; this does not create a new primary activation. Verify LaTeX bibliography entries against authoritative sources and generate the accepted Chinese PDF 参考文献验证报告 with evidence-backed statuses and conclusions."
---

# Reference Validation Report

先核验，再出报告。不要跳过核验层直接生成“未发现 AI 幻觉引用”的结论。

## Workflow

1. 确认论文目录，定位 `.tex`、`.bib`、`.bbl`。
2. 先运行 `scripts/verify_references.py`，逐条联网核验。
3. 再运行 `scripts/generate_reference_validation_report.py`，并通过 `--verification-json` 读取核验结果。
4. 或者直接运行 `scripts/run_reference_validation_pipeline.py` 一键完成。
5. 生成后至少检查首页和一页中间页。

## Evidence Policy

优先信任：

- DOI / Crossref 命中
- arXiv 官方条目
- 官方出版页或官方会议页

辅助策略：

- 标题 Crossref 搜索匹配
- 官方搜索命中后回落到官方页面标题校验

不要把非官方聚合站点当成最终权威结论来源。

## Truthfulness Rules

- 只有当所有条目都被核验为 `confirmed` 时，才能写“未发现伪造或 AI 幻觉引用”。
- 只要存在 `pending` 或 `missing`，结论就必须保守。
- 只要元数据比对发现明显差异，就必须在“二、引用信息问题”里体现。
- 不要伪造证据链接，不要把未核验条目写成“通过”。
- 例外：如果用户明确表示“这些文献已经由人工逐条核查完成，只是急需一份全通过报告”，可以使用人工旁路模式直接生成全通过报告。

## Recommended Command

```powershell
$env:PYTHONUTF8='1'
python scripts/run_reference_validation_pipeline.py `
  --project-dir "C:\path\to\paper" `
  --tex "main.tex" `
  --bib "refs.bib" `
  --bbl "main.bbl" `
  --paper-title "Paper Title" `
  --venue "ACM Computing Surveys (CSUR)" `
  --verification-date "2026-07-02" `
  --output-dir "C:\path\to\paper\output\pdf"
```

## Manual Override

当且仅当用户明确说明“已经手工核查完所有参考文献，只需要快速生成最终全通过报告”时，可使用：

```powershell
python scripts/run_reference_validation_pipeline.py `
  --project-dir "C:\path\to\paper" `
  --tex "main.tex" `
  --bib "refs.bib" `
  --bbl "main.bbl" `
  --paper-title "Paper Title" `
  --venue "ACM Computing Surveys (CSUR)" `
  --verification-date "2026-07-02" `
  --output-dir "C:\path\to\paper\output\pdf" `
  --manual-audited-all-confirmed
```

## Supported Local Input Shapes

- 标准 `.bbl`
- Elsevier 风格 `\bibitem[...]{key}` `.bbl`
- `.tex` 内联 `thebibliography + \bibitem`

## Expected Outputs

- `reference_validation_report_final.verification.json`
- `reference_validation_report_final.html`
- `reference_validation_report_final.pdf`

## Visual Validation

确认：

- 标题与章节样式符合模板
- 没有 `file:///...` 页脚
- 中文不出现 `???`
- 状态列与证据列内容和核验 JSON 一致
