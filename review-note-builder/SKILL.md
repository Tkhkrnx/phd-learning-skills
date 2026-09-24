---
name: review-note-builder
description: Build a PPT-ready paper-review analysis note, or turn its post-presentation revision into a formal reviewer report when explicitly invoked.
---

# Review Note Builder

This Skill has two user-driven stages. Stage 1 produces a paper-grounded analysis note that can directly support the user's presentation. After the user presents and incorporates discussion or teacher feedback into the deck and note, Stage 2 turns those updated materials into the formal reviewer report. Do not force a discussion or approval turn between stages; the user decides when to return for Stage 2.

## Sources and judgment

- Read the full relevant paper, pivotal figures/tables, and any appendix needed to verify a criticism before treating it as established. If the paper is unavailable, state the evidence limit and do not present a complete review as verified.
- Anchor the review's wording to the manuscript, not just its broad topic. Preserve the paper's objects, technical terms, causal direction, scope, and evidential qualifiers when paraphrasing; distinguish the authors' claims from the reviewer's interpretation. Check the final summary and every consequential strength or weakness against the cited passage before delivery.
- The user's latest conclusion, including a teacher-agreed recommendation, determines intended verdict and emphasis. In Stage 2, use the revised analysis and current PPT to recover the approved reasoning and presentation order; older notes are context. Independently test every factual claim against the manuscript. Keep a user judgment visible when the evidence does not yet settle it; do not convert it into a false factual assertion.
- Inspect PPT text, figures, and speaker notes. The notes may contain generic prompts or provisional reactions. Preserve source identity and separate confirmed issues, missing explanation, hypotheses needing a test, and optional improvements.
- For local files, `scripts/build_review_note.py --paper <paper.pdf> [--note <draft.md>] [--pptx <slides.pptx>]` inventories the source set without generating a note or review.

## Stage 1: presentation-ready analysis note

When the user asks to analyze a paper or prepare a review presentation, write one new analysis note using [five-question review guide](references/five-question-review.md). Follow its exact review sequence: problem definition, importance, existing work, key idea (including enough design detail to judge how it works), and experimental support. Do not make “design” a separate fifth review question. Put the experimental setup and slide-to-figure/table evidence map inside Question 5. Question 6 covers writing, terminology, and presentation details; finish with an overall assessment.

The review note must do more than explain the paper. Under each of Questions 1–5, state the reviewer's assessment of that dimension: what is clear or convincing, what remains problematic or unverified, and how that affects the paper's claims or evaluation. Question 6 must state concrete editorial/content findings. Do not force a flaw or revision request when the evidence supports the paper. For each consequential concern, provide judgment, manuscript evidence, effect on the conclusion or recommendation, and the smallest useful clarification or test. Keep the evidence map detailed enough to reproduce the supplied PPT's actual claims, while distinguishing the authors' motivation, measured results, and reviewer inference. If the PPT omits a material concern, add the review analysis rather than merely copying the deck.

When a supplied PPT is the user's final delivery, compare the note with its actual slide wording, explanation depth, and evidence. A structurally complete note that contains only headings or compressed summaries is not complete; it must let the user recover the same problem statement and argument at comparable depth. Preserve the user's slide narrative where sound, and correct only claims contradicted by the paper or important evidence.

These questions are a reasoning structure, not a quota of flaws. Explain what the paper does well. For each consequential concern, cite the exact manuscript location, state whether it is a false claim, an unclear explanation, an alternative explanation not isolated by the experiments, or an optional extension, explain its effect, and state the smallest useful clarification or test. Check whether the point is already addressed elsewhere. Do not write the formal reviewer report in Stage 1.

## Stage 2: formal reviewer report after the presentation

Use this stage when the user returns after presenting and provides the presentation PPT, the discussion or teacher conclusions, and the analysis note they have revised. Read [formal review guide](references/formal-review.md). Treat the latest post-discussion judgment as the intended review position and use the revised note/PPT to recover its reasoning; check factual claims against the paper and reconcile substantive conflicts explicitly. If discussion changes the problem framing or severity, revise the connected argument consistently instead of appending a correction to stale wording. Produce the formal reviewer report as the deliverable. Follow the venue's exact fields and rating scale when supplied; otherwise use Summary and High Level Discussion, Strengths, Weaknesses, Comments for Rebuttal, Detailed Comments for Authors, and Overall Recommendation. Add reproducibility only when material. Do not add confidential committee comments unless requested or required. Do not regenerate the analysis note unless asked.

If the user explicitly asks for a formal report before the presentation-stage materials exist, follow that request but identify which post-presentation inputs are absent and do not invent their conclusions. Never silently treat an old PPT or unedited analysis draft as the user's latest post-discussion view.

For Stage 1, run `shared/obsidian/note_quality.py --kind review-analysis --path <analysis-note> --expected-title <title>`, then inspect it against the paper, PPT, and supplied user conclusions. For Stage 2, run `shared/obsidian/note_quality.py --kind review --path <formal-review> --expected-title <title> --companion <updated-analysis-note>`. The validator checks structure and verdict consistency, not semantic agreement. In either stage, preserve source files and existing reviews, and return only the deliverable(s) appropriate to that stage.

Ordinary requests to review a paper do not activate this explicit-only Skill.
