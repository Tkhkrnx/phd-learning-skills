# Paper explanation and presentation regression cases

These cases were derived from the conversation [用 reading-note-builder 生成论文笔记](codex://threads/01a11747-074a-7581-8014-d1042de233ad). They are behavioral evaluation cases, not proof that a new model invocation has passed them. The cited paper details belong to the BatchGen example; do not turn its architecture or fixed page count into requirements for other papers.

## Note and review-analysis cases

| Observed failure | Expected behavior on a fresh task |
| --- | --- |
| The problem section starts with metrics and implementation causes before the unmet need. | Establish the abstract's background and declarative problem, using the introduction for context. Explain importance and prior-work limitations in their own roles. |
| Three motivation panels become three independent motives. | Read the caption and surrounding text. In BatchGen, distinguish the structure in 2a, its batching consequence in 2b, and the separate long-tail issue in 2c. |
| Batch size versus execution time is described as a direct GPU-utilization measurement. | Identify measured variables, derived throughput, and the authors' separate utilization statement. Do not fabricate a utilization percentage from that plot. |
| Prior-work categories drift away from the paper, and unrelated rows repeat the same advantages. | Start with the authors' categories and verify each row's representatives, strengths, and remaining mismatch independently. Preserve complementary work as complementary. |
| An overview becomes a long scheduler trace, or numbered insights become temporal steps. | Explain the major responsibilities and relationships, and use insights as the reasons for the architecture. Put execution details in their source-led design section. |
| “A sequence is a coroutine” becomes a false one-to-one identity for every diagram block; async/return is treated as automatic state saving. | Check the abstraction and pseudocode together with the prose. Distinguish the sequence state object, coroutine execution steps, wrapper installation, actual execution, retained data and scheduler control. Mark omitted implementation. |
| Design headings list components and figures without the authors' questions/challenges. | Preserve the authors' layered problem/design organization. Explain each relevant figure and algorithm inside its corresponding goal, in source order. |
| An algorithm or a text-only experiment disappears because it has no separate result image. | Keep a source-to-output map that includes algorithms and body-text results. Explain the algorithm's key branches and retain the reported text result with its original scope. |
| Workload, dataset, deployment scale and baseline are mixed in experimental setup. | Use a compact setup split into models/hardware, datasets/application workloads, baselines, configuration and metrics. Move detailed parameters beside the relevant experiment. |

Use the same reconstruction quality for review analysis, but retain its five review judgments plus writing/details. A faithful explanation alone does not satisfy the review's judgment/evidence/impact/minimal-improvement requirement.

## Presentation cases

1. Request: complete only the unfinished pages using the supplied deck. Identify protected display pages and stale template pages, use the current source rather than historical page numbers, preserve the template and output a new file.
2. Request: “正文要有重点，我讲这些重点大家就能理解。” Use concise technical points with enough causal explanation; do not produce a verbatim speech or hide the mechanism in notes.
3. Request: explain a confusing subfigure in chat. Answer from the source without editing the deck unless editing was also requested. A discussion question does not become a new slide title by default.
4. Request: split a specific dense page, then later keep Figure 7 together. Apply the latest page-specific constraint, preserve the parent section order and titles, and update the display-page map. Do not expand the whole deck into a new question-led outline.
5. Request: no visible source numbering and no notes. Keep exact provenance in private working materials, remove the requested presentation elements, and preserve source-faithful content.
6. Request: “问题二怎么丢了？” Detect and restore the parent experiment question, with RSA and rollout remaining subordinate rather than silently renumbering them as separate questions.

## What was actually verified during this change

- All 39 returned turns (38 containing user messages) from the referenced thread were inspected, including the initial note, iterative corrections, PPT completion and the final provenance question.
- `tests/test_paper_presentation_contract.py` exercises actual ZIP/XML fixtures: display order, changed linked media, notes and stale text, a missing parent heading, invalid preservation mappings and benign XML reserialization.
- The thread's existing 20-page `structure-fixed` PPT passed explicit count, empty notes, stale-paper text and parent-question checks. This is historical-artifact structural validation, not a newly authored PPT or a new behavioral run.
- Comparing six protected pages with the earlier `completed` deck flagged direct layout dependencies. Inspection found equivalent slide XML and an automatic shared-layout date change from 2026/10/15 to 2026/10/16. The check correctly requires inspection; it does not establish a conceptual or visual flaw by itself.
- A same-agent, three-page authoring exercise was subsequently run from the source paper and the accepted BatchGen deck: overview, outer scheduling algorithm, and memory model. New editable explanatory text was authored through the current presentation runtime, while the source headers, scientific images, layouts and theme were retained. The source text used for checking was the architecture discussion on PDF page 5 and design/algorithm/memory discussion on pages 8–9.
- The first render exposed cramped mixed-language wrapping. It was revised and rendered again. All three final pages were visually inspected against the reference and source, including the algorithm's refill/long-tail conditions, yield boundary and DP/TP distinction, and parameter/KV transfer directions. The finalizer reported three slides, no package findings, no geometry findings and no warnings. The final rendered images matched the inspected repaired drafts. The static contract checker passed count, notes, stale-paper text and required-title checks.
- The local example is `outputs/batchgen-skill-check/BatchGen-quality-sample.pptx`; private build/validation files stay under `work/batchgen-skill-check/`. These ignored example files are not published with the Skill. This is a representative same-paper content/render exercise, not an independent model forward-run or a whole new-paper evaluation.

For broader behavioral testing, provide a different paper plus a partial deck to a fresh model under the new Skill. Inspect the actual note/deck against the source and user contract. A static contract validator cannot replace that check, and this three-page sample does not establish uniform quality across other papers.
