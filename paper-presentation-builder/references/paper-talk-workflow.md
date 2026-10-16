# Build a paper talk from a source and a slide contract

## Inputs and preservation

Use the template selected by the entrypoint's precedence, including the packaged default when no template or existing work was supplied. A PPT supplied only as content is not automatically a style override. When the default is selected, follow [default-template usage](default-template.md): it is a full reference deck with old paper content to replace, not an empty deck or a fixed slide-count contract.

Inspect the paper and the supplied note/deck. The user's latest discussion judgment sets emphasis and intended review position, while the paper checks factual claims. A partial note or an old-paper template can contain gaps or stale material. Classify source pages as protected completed work, editable current work, or old content to replace. Do not infer that every existing page is finished or that every page may be redesigned.

Keep a private working map with original/output display-page numbers, slide role, author section/figure/algorithm, content to retain/replace, and the expected explanation. Use display order from the presentation relationships, not a file name such as `slide10.xml`. If splitting inserts pages, update the map while retaining the logical question numbering and ownership of subexperiments.

Preserve the supplied template's title positions, text hierarchy, bullet or arrow style, fonts, colors, logos and repeated elements. Use existing page layouts for the appropriate role. Required tables/charts and new explanatory text should remain editable. Reuse source paper figures with legible labels; do not replace scientific evidence with decorative or generated imagery.

## The content on each kind of page

**Background and problem.** Use the abstract's background and unmet need, with introduction context. State the research problem declaratively. Keep the technical cause and proposed design in their proper later roles.

**Motivation.** Summarize the authors' motivating explanation and measurements. Explain how subfigures relate, what is measured, and the consequence. Retain necessary terms and units. Do not assign one motivation to each panel unless the authors actually do so.

**Prior work.** Prefer the authors' categories and the user's comparison layout. The common columns are 类别、代表方法、优势、核心缺陷. Verify that each row describes its own approach; do not copy a generic advantage across unrelated methods. A different scope or complementary contribution must not become a fabricated defect.

**Overview.** Introduce the system's major responsibilities and relationships, tied to the authors' insights. A flow or input example may clarify those relationships when supported, but a list of insights is not automatically a chronological execution trace.

**Design.** Keep the authors' abstraction/design hierarchy and section order. Put each design under the problem or goal it addresses. Explain the source figures and algorithms at that point: actors, state, operations, dependencies, scheduling decisions, data movement and outputs where relevant. Do not merely list module names or replace an algorithm with a vague paragraph. Use local annotations or concise steps that make its important branches and relation to other algorithms understandable.

**Experimental setup.** Give one compact orientation: models/hardware, datasets/application workloads, baselines, configurations, metrics/protocol. Put detailed parameters beside their experiment. Do not mix scale, deployment method, workload and dataset into one list labelled workloads.

**Results.** Follow the authors' experimental order or the user's already chosen question hierarchy. Keep the question heading when one experiment is spread across several pages. For each result, show its comparison, key observation and supported conclusion. Include reported text-only results when central to the requested talk; label their source and do not fabricate an original figure or an isolated component attribution.

**Review findings or conclusion.** Include only the scope requested by the user. Review concerns belong to the corresponding analysis, with evidence and severity; a reading talk does not automatically acquire reviewer criticism. Preserve a teacher/user recommendation as their judgment and keep factual support consistent.

## Compression, explanation and page changes

Slide text should supply enough substance for the user to explain the key points without reading speaker notes. Keep technical nouns but explain their role and causal connection. Avoid both bare labels and complete spoken scripts. Notes are optional only when requested or established by the source contract; detailed explanation is not a reason to hide the essential content there.

A request to clarify a dense page does not authorize changes throughout the deck. Where a split is requested, split that content while preserving the overall hierarchy and surrounding pages. A figure explicitly required on one page stays together. When page count is fixed, improve selection and local wording first; do not silently add pages or shrink body text until it is unreadable. Raise a specific layout conflict only when it cannot be resolved within the given contract.

Questions raised during discussion reveal what needs explanation. Answer them in chat when asked, and incorporate the supported clarification into the existing source-led section when editing is requested. Do not title new slides after those questions unless they also match the authors' structure or the user requests that format. Distinguish an author's original question from an editorial paraphrase in the private source map.

## Source locations and notes

Maintain paper section/page/keyword mappings in the private working map, even when the user asks for no visible chapter/figure citations and no notes. These are independently checkable requirements: clean presentation pages still need source-grounded content. If source attribution is requested, provide the exact mapping and say whether a title/layout was editorial. Do not describe a generated title or illustration as the author's original material.

## Final verification

Treat an accepted user deck as a quality reference, not just a theme. Before delivery, compare the actual generated pages against these content criteria:

| Page role | The audience must be able to explain |
| --- | --- |
| Problem and motivation | The unmet condition, why it matters, and how the source evidence establishes the loss; problem, cause and solution remain distinct. |
| Overview | What enters the system, what each main part does, how those parts connect, and which author insight justifies the arrangement. |
| Design or algorithm | Which challenge is addressed, the important states and decisions in source order, how execution proceeds and why it can continue correctly. |
| Memory or data movement | What each region holds, what moves in each direction, when it moves, and how that enables the mechanism; figure labels alone are insufficient. |
| Experimental result | The comparison and conditions, the decisive observation, its supported interpretation and any qualification that changes the conclusion. |

Read the slide's actual words together with the figure. If the essential explanation is absent, depends on hidden notes, contradicts the source, or is substantially thinner than the accepted reference, revise before delivery. Compression may remove repetition but must retain the causal links. A complete source map, attractive layout or passing validator does not compensate for missing explanation. Keep paper-specific mechanisms and page counts out of the reusable acceptance rule.

Read slide titles in order, then the body and images together. Check the whole sequence against the source map, including algorithms, text-only results and parent experiment questions. Inspect rendered changed slides at presentation size. Compare protected pages with their mapped output pages and check for stale template text/images. Review inherited master/footer elements when making global changes.

For local files, the structural checker supports:

```powershell
python paper-presentation-builder/scripts/audit_deck.py --deck result.pptx --source original.pptx --preserve 1:1 --preserve 10:14 --expected-count 20 --no-notes --forbid-text OldPaperName --require-text "问题二"
```

Numbers in `--preserve SOURCE:OUTPUT` are one-based display-page numbers. This is an example of options, not a fixed paper layout. The checker normalizes XML serialization, then compares the slide XML and direct dependencies such as images and layouts. A difference requires inspection; even a shared automatic date field can change a layout. The checker cannot prove full template fidelity, source interpretation, image legibility, or a successful native PowerPoint open. Complete the presentation tool's own export/package checks and visual review as applicable, then deliver one clearly identified final deck.
