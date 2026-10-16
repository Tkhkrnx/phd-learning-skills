---
name: paper-presentation-builder
description: Create or revise a paper-reading or review presentation from the paper and optional notes or template when explicitly invoked.
---

# Paper Presentation Builder

Produce the requested paper-talk PPT with concise explanatory points, source-faithful figures and conclusions, and the user's presentation structure. Inputs may include a paper, reading/review analysis, a partly completed deck, and discussion corrections. A note is useful but not required. A formal reviewer report remains a separate review deliverable.

## Establish the slide contract

Read [paper-talk workflow](references/paper-talk-workflow.md) and [source-grounded explanation](../shared/expert-skill-references/paper_explanation.md). Inspect the supplied deck's actual slides before editing. Record which pages are finished, which contain old template content, the title/problem numbering and order, slide dimensions, repeated elements, and any slide-count, notes, citation, or figure-splitting instructions. Infer these from the supplied request and files; ask only if a consequential ambiguity remains.

Use the user's latest framing and corrections, while checking facts against the paper. Preserve finished pages and edit the requested remainder in a new file. Keep an original-to-output page map if pages move. A request to explain a figure is read-only unless the user also requests changes.

## Build the talk

1. Map the paper's problem, motivation, closest-work gap, idea, design and evidence onto the agreed deck. Follow the author's hierarchy inside these sections and the user's chosen overall order. Verify the paper's supporting prose, figures, algorithms and body-text results.
2. Put the explanatory essentials on the slide: what the figure or algorithm does, the relevant comparison or state change, and why it matters. Use compact technical points with causal links, not unexplained noun lists or a narration script. The user should be able to explain the slide without hidden speaker notes.
3. Keep the original problem/challenge and experiment-question hierarchy. Clarifications from chat repair the corresponding explanation; they do not automatically become new question slides, a new storyline, or permission to expand the deck. Split only where consistent with the user's page/figure contract; otherwise edit the local explanation or identify the space conflict.
4. Use the available presentation-authoring capability as a bounded implementation dependency. In Codex, load the current Presentations Skill and its relevant authoring/template/finalization references when available. Resolve its installed location at runtime; do not hardcode a plugin version or copy its implementation into this Skill. On other clients use their available PPT tools with equivalent editing and verification. Report any material limitation.

## Verify and deliver

Inspect final rendered slides, including every changed slide and any slide affected by a master/layout change. Check source accuracy, protected pages, title/problem numbering, ordering, old-paper residue, figure completeness, font/size consistency, clipping, editable required content, notes and citations. A package check or successful export alone is insufficient.

For local PPTX, `scripts/audit_deck.py` checks selected structural contracts and can compare declared protected pages with a source deck. Run it where those checks apply; it neither renders nor judges explanation quality. Keep provenance and build records in the working directory unless requested. Source locations can remain there when the user requests clean slides and no notes; do not silently put them back on the slide or in notes.

Return the verified PPT at the requested path, or a new clearly named deliverable beside the input deck when unspecified. Do not overwrite the source deck. State limitations that affect its use. This Skill does not authorize publication, messaging, or a change to the research/review verdict.
