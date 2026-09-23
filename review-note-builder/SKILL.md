---
name: review-note-builder
description: Produce a five-question analysis note and formal paper review when the user explicitly invokes this Skill.
---

# Review Note Builder

Produce two separate, consistent artifacts from a rigorous and fair reading of the actual paper: a five-question analysis note for the user, and a submission-ready review with strengths and weaknesses. A Markdown draft and presentation are optional.

## Sources and judgment

- Read the full relevant paper, pivotal figures/tables, and any appendix needed to verify a criticism before treating it as established. If the paper is unavailable, produce only a clearly limited review draft.
- The user's latest conclusion, including a teacher-agreed recommendation, has highest priority for the intended verdict and emphasis. A review PPT comes next, then an older Markdown note. Independently test every factual claim against the manuscript. Keep a user judgment visible when the evidence does not yet settle it; do not convert it into a false factual assertion.
- Inspect PPT text, figures, and speaker notes. The notes may contain generic prompts or provisional reactions. Preserve source identity and separate confirmed issues, missing explanation, hypotheses needing a test, and optional improvements.
- For local files, `scripts/build_review_note.py --paper <paper.pdf> [--note <draft.md>] [--pptx <slides.pptx>]` inventories the source set without generating the review.

## Analysis note

Write the first deliverable using [five-question review guide](references/five-question-review.md): whether the problem is clear, why it matters, whether existing work leaves the claimed gap, whether the key idea and design make sense, and whether experiments support the claims. Add a writing/details section and a concise overall judgment. These are checks, not five required weaknesses. Explain what the paper already does well. A method that combines known elements may still have value; assess the novelty and added capability of the integration precisely.

For each consequential criticism, verify the manuscript location, state the exact claim or missing information, explain its effect on the paper's conclusion, and request the smallest clarification, comparison, or experiment that would resolve it. Check whether an apparently missing item is already covered elsewhere. Review writing and presentation details separately, including inconsistent terminology, contradictory tables, unclear prose, citation or formatting errors. Keep minor details separate from acceptance-driving concerns.

## Formal review

Translate the verified judgments into the original review workflow described in [formal review guide](references/formal-review.md). The second deliverable uses the requested venue form when supplied; otherwise write Summary and High Level Discussion, Strengths, Weaknesses, Comments for Rebuttal, Detailed Comments for Authors, and Overall Recommendation. Add reproducibility when material. Scores and confidential committee comments appear only when requested or required. This is a real reviewer report, not the five-question note under different headings.

Before delivery, compare the two artifacts finding by finding: the same paper claim, evidence, severity, proposed correction, and final recommendation must agree. The formal review may omit exploratory or low-impact notes, but cannot strengthen a tentative concern into a proven flaw or introduce a new acceptance-driving weakness without returning to the analysis. Preserve source files and existing reviews. Return **both** files in the conversation.

Run `shared/obsidian/note_quality.py --kind review-analysis --path <analysis-note> --expected-title <title>`, then `--kind review --path <formal-review> --expected-title <title> --companion <analysis-note>`. Read both outputs against the paper, PPT, and latest user conclusion; the validator checks structure and matching verdict only, not semantic agreement.

Ordinary requests to review a paper do not activate this explicit-only Skill.
