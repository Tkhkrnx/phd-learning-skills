# PhD Learning Skills

这是一个面向个人博士学习工作流的 skill 仓库，聚焦 5 个长期保留的能力：

- `weekly-paper-radar`
- `topic-paper-finder`
- `vault-note-finder`
- `reading-note-builder`
- `review-note-builder`

仓库目标不是重建旧的 PDF 入库流水线，而是把以下链路稳定下来：

1. 搜论文
2. 下载能直接获取的 PDF 到 PaperQuay
3. 在 PaperQuay 阅读、标注、写原始笔记
4. 基于 PaperQuay 笔记和 MinerU 正文缓存，生成正式的 Obsidian 阅读/审稿笔记

## Dependency

本仓库默认依赖 [PaperQuay](https://github.com/WangQrkkk/PaperQuay) 作为论文阅读、标注和正文缓存来源。

主要输入层包括：

- `paperquay-notes.sqlite`
- `paperquay-library.sqlite`
- `.mineru-cache/document-*/full.md`
- `.mineru-cache/document-*/content_list_v2.json`

本仓库不再负责旧式 `paper-ingest` / `paper-translate` 资产流水线。

## Skills

### `weekly-paper-radar`

- 面向近 3 年论文做每周雷达搜索
- 覆盖 3 个固定研究方向：
  - `State-Aware Orchestration and Resource Governance`
  - `Hardware-Aware Memory Management and Semantic Consistency`
  - `State-Reuse Inference for Long Contexts and MoE`
- 先查官方会议页面，再走聚合源恢复链路
- 产出机器可读候选池，最终推荐由调用 skill 的主模型在对话里直接给出

### `topic-paper-finder`

- 把用户的模糊需求收敛成关键词、venue、年份窗口
- 搜索目标论文并可选下载 PDF 到 PaperQuay
- 自动结合 `vault-note-finder` 做重复抑制
- 返回结构化 JSON，由主模型直接在对话里总结结果

### `vault-note-finder`

- 在 Obsidian vault 内搜索已有阅读笔记、审稿笔记和相关草稿
- 优先把正式 Reading / Review Notes 排到前面
- 用于避免重复推荐、重复入库、重复增强

### `reading-note-builder`

- 从 PaperQuay 阅读笔记出发，映射到对应论文和 MinerU 正文缓存
- 导出 `original.md`、`evidence_bundle.json`、`paper_summary.json`、`mapping_report.json`、`writer_prompt.md`
- 由当前执行 skill 的主模型完成正式 `enhanced.md`
- 输出结构以导师七问为主，并显式补出“你当前笔记的遗漏与纠偏”

### `review-note-builder`

- 从 PaperQuay 审稿笔记出发，先完成内部七问式增强理解，再转成正式 review 结构
- 所有关键批评都必须可回指到正文 Markdown 证据
- 默认站在系统顶会 reviewer 视角，严格、细致、证据优先

## Search Stack

搜索相关 skill 共用同一套 discovery / ranking / download 底座：

- 优先官方会议或出版方页面
- 官方源不足时，再回退到聚合源
- 当前聚合恢复链路为：`Semantic Scholar -> arXiv -> DBLP -> OpenAlex`
- 每个候选结果都结合 `vault-note-finder` 做重复检测
- 下载结果、限流恢复、PDF 缺失原因都会结构化写进 JSON

当前边界：

- 某些 publisher / DOI 页面仍可能返回 `403` 或登录限制
- 外部聚合源仍可能出现 `429`
- skill 会尽量恢复，但不会把“凑够数量”和“结果质量足够好”混为一谈

## Output Contract

`weekly-paper-radar` 和 `topic-paper-finder` 都遵循同一个约定：

- 脚本只负责产出结构化 JSON
- 最终推荐或搜索结论由 Codex/Claude 在对话里直接告诉用户
- 回答时应显式总结：
  - 成功下载了哪些 PDF
  - 实际写入的 PaperQuay 目录是什么
  - 哪些论文仍需用户手动补链

## Quickstart

具体命令见 [QUICKSTART.md](./QUICKSTART.md)。
