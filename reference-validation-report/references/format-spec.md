# Format Spec

Use this report format.

## Page Style

- Chinese report title: `参考文献验证报告`
- Font feel: `Microsoft YaHei`, `微软雅黑`, `PingFang SC`, `Noto Sans CJK SC`, sans-serif fallback
- White background
- No browser URL footer
- Vector/text PDF, not image-based assembly

## Header Block

Place these lines below the title:

- `论文: ...`
- `提交期刊: ...`
- `验证时间: YYYY-MM-DD`
- `验证工具: AI 自动参考文献完整性检测（main.tex + refs.bib）`

## Sections

Use exactly these three section titles:

- `一、验证摘要`
- `二、引用信息问题`
- `三、逐条验证结果`

Each section title uses:

- a medium-gray left bar block
- bold Chinese heading
- generous vertical spacing

## Summary Table

Two columns:

- `项目`
- `数量`

Rows:

- `引用总数`
- `通过（已确认存在）`
- `存疑`
- `未找到（疑似伪造）`

Conclusion line:

- If all verified and real: `结论：本文所有 N 篇参考文献均为真实存在的学术文献，未发现伪造或 AI 幻觉引用。`
- If metadata is clean: `未发现文献真实但著录存在明显错误的情况。`

## Per-reference Table

Columns:

- `#`
- `文献`
- `状态`
- `证据`

Row content rules:

- `#` uses bracketed numbering like `[1]`
- `文献` should be a bibliography-like sentence extracted from `.bbl`
- `状态` uses colored badge plus Chinese word:
  - green `√ 通过`
  - orange `! 存疑`
  - red `× 未找到`
- `证据` is short:
  - `已确认`
  - `待复核`
  - `未找到`

## Text Cleaning Rules

When converting `.bbl` entries to row text:

- unwrap `\emph{...}`, `\textit{...}`, `\url{...}`, `\showarticletitle{...}`, `\showURL{...}`
- unwrap `\bibinfo{...}{...}`
- remove `\newblock`
- convert `~` to spaces
- convert `\&` to `&`
- remove outer braces unless needed for visible text
- collapse repeated whitespace
- remove obvious duplicated title fragments when the same title appears twice in a row

## PDF Generation

Prefer local HTML plus Chrome headless printing:

- `chrome.exe --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=... file:///...html`

If Chrome is unavailable, stop and report the blocker instead of silently producing a lower-quality substitute.
