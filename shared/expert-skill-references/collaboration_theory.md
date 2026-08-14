# Theory Rationale for Expert Collaboration Skills

This reference supports maintainers of the four expert collaboration skills. Normal skill execution should use `AGENT_COLLABORATION_SKILL_BLUEPRINT.md` and should not load this file.

## Cognitive Apprenticeship

Experts model, scaffold, coach, and gradually fade support. The agent should reveal the structure of a judgment, then return ownership of that judgment to the user.

Reference: Collins, Brown, and Newman, 1989.

## Scaffolding and Cognitive Load

Support should match the user's current ability. Prematurely asking an unfamiliar user to produce a complete structure overloads working memory; providing the complete answer removes the learning opportunity. The operational compromise is a minimal scaffold followed by one answerable judgment.

References: Wood, Bruner, and Ross, 1976; Sweller, 1988 and later cognitive-load work.

## Worked Examples, Generation, and Retrieval

A small worked example helps when no mental model exists. Independent generation and retrieval become valuable after that model exists. This motivates the sequence: orient, ask for a small restatement, correct one mismatch, then transfer.

References: Sweller and Cooper, 1985; Slamecka and Graf, 1978; Roediger and Karpicke, 2006.

## Falsification and Mechanism Reasoning

Research problems and methods become defensible through contrast, causal mechanism, simpler alternatives, and evidence that could overturn the claim. The user must participate in these judgments because they define the scientific commitment.

## Situated Cognition and Evidence-Based Diagnosis

Engineering judgment depends on actual code, interfaces, configuration, logs, and runtime behavior. The agent should gather that evidence; the user should reason about design boundaries and trade-offs rather than perform clerical search.

## Why a Hard Interaction Gate Is Necessary

Natural-language goals such as "guide the user" are too weak when the surrounding agent is optimized to finish tasks autonomously. A low-freedom transition rule—one stage, one open-ended question that exposes the user's reasoning, then stop—prevents superficial compliance and protects the collaboration objective. Yes/no answers and bare choices are not evidence that the reasoning process occurred.
