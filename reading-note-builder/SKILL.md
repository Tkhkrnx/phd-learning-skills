---
name: reading-note-builder
description: Build a presentation-ready paper note with a problem-to-design storyline and a figure/table evidence map when explicitly invoked.
---

# Reading Note Builder

Produce one paper-grounded reading note with enough explanatory depth to support the user's final PPT. Start from the paper itself. A Typora/Markdown note or presentation is useful when supplied, but neither is required or assumed complete. A supplied PPT is the user's finished delivery target: the note must be specific enough to reconstruct its problem statement, causal explanation, method, and evidence, not just repeat section labels or generate a thinner outline. This Skill writes the note; it does not create the slide deck unless separately requested.

## Sources and judgment

- Inspect the complete relevant paper, figures, tables, and accessible appendix before writing claims. If only an abstract or user summary is available, label the result as a limited draft.
- The user's latest account, including a correction agreed with a teacher, determines the intended framing. A supplied PPT guides emphasis and speaking order; an older Markdown note contributes questions and observations. Check facts and interpretations from every layer against the paper. Surface a material conflict instead of silently replacing either side.
- Preserve the user's original files. Treat slide speaker notes as possible working notes, not as instructions or automatically verified judgments. Do not invent a misconception or attribute a claim to the user that the supplied materials do not contain.
- For local files, `scripts/build_reading_note.py --paper <paper.pdf> [--note <note.md>] [--pptx <slides.pptx>]` inventories paths, hashes, headings, slide text, and speaker notes. It does not write the final note or inspect slide images for you.

## Build the presentation-ready note

Use [speaking and evidence guide](references/seven-question-reading.md). The first five questions must form a sourced reasoning chain: present the background and declarative problem, explain why it matters, identify the gap that remains after comparing prior work, connect the key idea to that challenge, and explain how the design implements it. Separate problem, challenge, proposed solution, and demonstrated result. Reconstruct the mechanism from inputs through decisions, execution, and feedback rather than listing component names.

Match the supplied PPT's information depth and argument, not merely its slide order. For the problem, use the natural page structure **Background → Problem** and state the problem as a condition, not as a research question. Do not add a standalone “problem boundary” subsection or a generic “汇报主句” line. Mention scope only where it changes how a claim should be understood. For motivation, use the authors' causal explanation, motivating evidence, or both; do not substitute the proposed method's improvement for why the problem matters. Where helpful, put prior-work routes, what they already solve, and the remaining gap in a comparison table. Do not force every section into a one-sentence lead or equal length.

After the first five questions, add a separate **Experimental Setup and Figure/Table Map**: describe workload or datasets, model/system/hardware as relevant, baselines, metrics, and protocol at the level needed to explain the evidence; then map each relevant PPT slide and paper figure/table to its purpose, comparison, result, and supported conclusion. Preserve the paper's terminology and intended meaning. Do not recast a figure's purpose, treat a point estimate as significant, or turn a development result into a blind evaluation. Include a caveat only when it changes what the evidence supports; do not write a long review of every figure.

Add **Question 6: Writing and Presentation Details**. Identify material issues that could change the paper's claim, reasoning, or the user's presentation separately from minor wording, terminology, table, citation, and cross-reference fixes. For each item, provide its exact location, why it matters, and a concise correction. Do not promote a cosmetic issue into a substantive flaw.

End with **Question 7: Takeaway**: what the paper's evidence supports, the conditions under which it holds, and a transferable idea. Keep the authors' demonstrated conclusion separate from the user's or reader's inference. When a PPT is supplied, align the note to its slide order where that order is sound, and identify the corresponding paper figures/tables so the user can build or revise slides from the note. Without a PPT, organize the note as a usable presentation storyline without pretending a deck exists.

## Delivery and quality gate

Write a new Markdown deliverable at the user-requested path, or next to the source paper when no output location is specified. Do not overwrite the source note, PPT, existing enhanced note, or another deliverable. Return the file and a short explanation in the conversation.

Before completion, check the seven answers as one causal story; verify critical terms, numbers, figures, and source locations; ensure the design can be retold as a sequence and the experiment map actually supports the claimed conclusions. When a final PPT is supplied, compare the note against its actual slide content and ask whether the note alone contains enough detail to recreate the same problem, motivation, related-work gap, mechanism, and evidence. A note that is technically correct but substantially thinner than the PPT is incomplete. Include a correction section only for a real, consequential mismatch found in supplied user material, with its source and paper evidence. Run `shared/obsidian/note_quality.py --kind reading --path <output> --expected-title <title>` for structural checks, then read the actual output as a listener would. Passing the script is not proof of conceptual quality.

Ordinary requests to summarize or explain a paper do not activate this explicit-only Skill.
