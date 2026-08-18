# Theory Rationale for Expert Collaboration Skills

This reference supports maintainers of the four expert collaboration skills. Normal skill execution should use `AGENT_COLLABORATION_SKILL_BLUEPRINT.md` and should not load this file.

## Cognitive Apprenticeship

Experts model, scaffold, coach, and gradually fade support. The agent should reveal the structure of a judgment, then return ownership of that judgment to the user.

Reference: Collins, Brown, and Newman, 1989.

## Scaffolding and Cognitive Load

Support should match the user's current ability. Prematurely asking an unfamiliar user to produce a complete structure overloads working memory; providing a polished answer and treating it as final removes the learning opportunity. The operational compromise is adaptive: the expert may model a complete candidate, then ask the user to correct, choose, reconstruct, challenge, or apply the part that matters next.

References: Wood, Bruner, and Ross, 1976; Sweller, 1988 and later cognitive-load work.

## Worked Examples, Generation, and Retrieval

A small worked example helps when no mental model exists. Independent generation and retrieval become valuable after that model exists. This motivates the sequence: orient, ask for a small restatement, correct one mismatch, then transfer.

References: Sweller and Cooper, 1985; Slamecka and Graf, 1978; Roediger and Karpicke, 2006.

## Falsification and Mechanism Reasoning

Research problems and methods become defensible through contrast, causal mechanism, simpler alternatives, and evidence that could overturn the claim. The user must participate in these judgments because they define the scientific commitment.

## Situated Cognition and Evidence-Based Diagnosis

Engineering judgment depends on actual code, interfaces, configuration, logs, and runtime behavior. The agent should gather that evidence; the user should reason about design boundaries and trade-offs rather than perform clerical search.

## Why an Adaptive Interaction Gate Is Necessary

Natural-language goals such as "guide the user" are too weak when the surrounding agent is optimized to finish tasks autonomously. A rigid rule that always makes the user construct first is also harmful: it withholds expert value, creates unnecessary interrogation, and can overload a novice. The gate therefore protects the exchange rather than a fixed turn shape. The agent may lead with a strong candidate, but it cannot close the consequential judgment alone. It must obtain meaningful evidence from the user's correction, domain evidence, reasoned choice, restatement, challenge, or transfer attempt, update the shared model, and continue until the target outcome is understood with roughly 90% operational confidence and the remaining uncertainty is explicit.
