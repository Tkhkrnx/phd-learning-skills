# Workflow

## 1. Weekly Discovery

`weekly-paper-radar` 负责例行搜索。它围绕两个固定研究方向展开：

- `State-Centric Runtime Design`
- `Hardware-Conscious Execution`

每个方向都会进一步拆成多个子方向，用短查询逐条搜索，而不是把 topic、subtopic、venue 一次性拼成一个长 query。

搜索顺序是：

1. 官方会议 / 出版源页面
2. 聚合源兜底
3. vault 去重
4. 可选 PDF 下载

## 2. Focused Search

`topic-paper-finder` 负责临时专题搜索。

它的预期用法不是要求用户一开始就给出完全精确的字段，而是先把模糊需求压成这些条件：

- 主题 / 问题
- 可能子方向
- 关键词
- venue 或 venue tier
- 年份范围
- 是否想顺手下载 PDF

然后走与 `weekly-paper-radar` 相同的 discovery 底座。

## 3. Reading In PaperQuay

发现到的论文先进入 PaperQuay 阅读。

正式输入层不是旧 Obsidian 资产目录，而是：

- `paperquay-notes.sqlite`
- `paperquay-library.sqlite`
- `.mineru-cache/document-xxxx/full.md`
- `.mineru-cache/document-xxxx/content_list_v2.json`

## 4. Formal Note Building

`reading-note-builder` 和 `review-note-builder` 会把：

- PaperQuay 原始笔记
- 论文正文缓存
- 映射诊断信息

重新收束成证据包，再由当前运行 skill 的主模型完成正式写作。

其中：

- 阅读笔记强调“先校正你的原笔记，再补导师七问空缺”。
- 审稿笔记强调“先完成七问式增强理解，再转成严格 review 结构”。
- 两者都要求结论能回指正文证据。

## 5. Vault Search

`vault-note-finder` 是搜索流程的重复抑制层。

它的目标不是简单全文检索，而是优先返回 `Research/Papers/<short-name>/Reading/enhanced.md` 与 `Review/enhanced.md`，再返回需要保留的 `Support/original.md`。`writer_prompt.md`、evidence JSON 和日志位于 Vault 外的工作目录，不参与知识库搜索。
