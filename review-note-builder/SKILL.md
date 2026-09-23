---
name: review-note-builder
description: Produce a formal, evidence-backed paper review when the user explicitly invokes this Skill.
---

# Review Note Builder

Deliver a rigorous and fair review of the actual paper. A Markdown draft and presentation are optional. When supplied, they reveal the user's priorities; they do not replace checking the manuscript.

## Sources and judgment

- Read the full relevant paper, pivotal figures/tables, and any appendix needed to verify a criticism before treating it as established. If the paper is unavailable, produce only a clearly limited review draft.
- The user's latest conclusion, including a teacher-agreed recommendation, has highest priority for the intended verdict and emphasis. A review PPT comes next, then an older Markdown note. Independently test every factual claim against the manuscript. Keep a user judgment visible when the evidence does not yet settle it; do not convert it into a false factual assertion.
- Inspect PPT text, figures, and speaker notes. The notes may contain generic prompts or provisional reactions. Preserve source identity and separate confirmed issues, missing explanation, hypotheses needing a test, and optional improvements.
- For local files, `scripts/build_review_note.py --paper <paper.pdf> [--note <draft.md>] [--pptx <slides.pptx>]` inventories the source set without generating the review.

## Review reasoning

Use [five-question review guide](references/five-question-review.md): whether the problem is clear, why it matters, whether existing work leaves the claimed gap, whether the key idea and design make sense, and whether experiments support the claims. These are checks, not five required weaknesses. Explain what the paper already does well. A method that combines known elements may still have value; assess the novelty and added capability of the integration precisely.

For each consequential criticism, verify the manuscript location, state the exact claim or missing information, explain its effect on the paper's conclusion, and request the smallest clarification, comparison, or experiment that would resolve it. Check whether an apparently missing item is already covered elsewhere. Review writing and presentation details separately, including inconsistent terminology, contradictory tables, unclear prose, citation or formatting errors. Keep minor details separate from acceptance-driving concerns.

## Formal deliverable

Write a new Markdown review, in the requested language and venue format when provided. Otherwise use five numbered assessments, a writing/details section, and an overall recommendation with confidence. Lead each assessment with a clear judgment and concise evidence. Do not expose internal seven-question notes, invented user misconceptions, or a private correction ledger in the submission-ready review. Include confidential committee comments or numerical scores only when requested or required by the venue form.

Preserve the source files and existing reviews. Return the formal review file and its main judgment in the conversation. Run `shared/obsidian/note_quality.py --kind review --path <output> --expected-title <title>`, then inspect the real prose against the paper, user PPT, and latest user conclusion. A structural pass alone cannot establish review quality.

Ordinary requests to review a paper do not activate this explicit-only Skill.
