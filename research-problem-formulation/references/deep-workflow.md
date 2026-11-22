# Deep problem-formulation workflow

Use this reference only when the problem boundary is broad, prior work is contested, or an existing problem/RQ package is being revised.

## Semantic model

Distinguish:

- topic: the broad area;
- objective: the desired improvement;
- problem: an evidence-supported condition or limitation in a defined context;
- challenge: why the condition is hard to address or explain;
- method: a proposed way to address it;
- RQ: a question used to organize evaluation.

A valid problem identifies an affected object and condition and still makes sense after the proposed remedy is removed. It may describe a limitation, assumption mismatch, or unexplained phenomenon. Do not force a causal explanation when only the phenomenon is observed.

Useful reasoning forms include:

```text
Under condition C, system object S exhibits limitation L, causing consequence I.
Existing systems assume A; under condition C, behavior F remains important and unresolved.
Phenomenon P occurs in context C, but current understanding or mechanisms do not adequately explain or handle it.
```

These are diagnostics, not templates. Reject declarative disguises such as “research how to optimize X” or “we need the proposed X.”

## New-problem route

Start from the user's observation or intuition.

1. Record what is observed, what is inferred, and what is merely desired.
2. Localize the primary system object and operating boundary.
3. Build a targeted query portfolio around phenomenon, synonyms, conditions, consequences, closest techniques, limitations, and counterqueries.
4. Compare the closest work under equivalent object, assumptions, conditions, and metrics.
5. Test whether the candidate is real, material, unresolved, non-trivial, and measurable.
6. Present the strongest current formulation with evidence limits and the best counterexample.

## Revision route

Before revising, identify the authoritative current problem statement, scope, claims, challenges, RQs, and the items the user has reopened. Change only affected items. Do not rewrite challenges and RQs together unless both are in scope.

Recover the scientific object, intended outcomes and exclusions from the latest user reasoning. Identify which materials supply observations and which examples illustrate just one condition. Check that the problem statement still applies to the other intended settings. Present an unresolved choice only when it changes the framing.

When new evidence conflicts with a frozen item, show the conflict and smallest revision. Preserve the user's terminology and requested structure.

## Explain the nearest-work failure

Build the comparison from the search results. Follow the closest papers' references and later alternatives, check the decisive methods, evaluations and stated limitations, and include work that solves a candidate subproblem. Group by how the methods work. Give a direct competitor its own row whenever its capability changes the conclusion.

| 类别 | 相关工作文章 | 已解决的问题与优势 | 为什么仍不足以解决本文问题 |
| --- | --- | --- | --- |

Use an informative method name for each row. Order families by the question they can answer: same decision and goal, neighboring decision or component, then relevant foundations. Include simple compositions and solutions from other vocabularies if they could meet the same goal. Within a family attribute capabilities to the particular papers that demonstrate them. In the fourth column explain the missing input, assumption or unsupported decision and its consequence. For a background paper, explain which part it informs and which decision lies beyond its scope. If a result requires a new comparison, say precisely what is unknown after giving the substantive boundary. End with the gap that survives and investigate material coverage gaps.

For each consequential comparison, connect the work's real achievement to the mechanism or assumption it uses, the relevant target condition, and the resulting limitation. Cite the source location for established facts; label an inferred mismatch or proposed counterexample as such. A different objective, unimplemented feature or limited evaluation scope is not by itself a demonstrated failure.

- Insufficient: defining the literature gap as the absence of the implementation proposed by the team.
- Useful investigation: extract the closest method's inputs, objective, operating assumptions and evaluated conditions from the original source. Apply them to the user's specific decision. Identify what can already be decided and exactly which ambiguity persists.

Compare against the strongest simple composition as well as individual papers. If it already addresses the target condition, remove that gap. If a different condition creates a genuine problem, explain why that condition occurs and matters rather than adding artificial restrictions to defeat a competitor.

## Paper-facing answer and supporting record

Check the problem paragraph on its own. Remove any sentence describing what the team will investigate, build or return. What remains should explain the difficulty that exists in the current research setting and why it matters. Preserve that distinction when the user requests a shorter version.

For full formulations, use the three-answer format in the entrypoint. Present the opening as separate **背景：** and **问题：** paragraphs, one sentence each for the abstract-length version. Give motivation and the literature table the space their evidence needs.

Keep decisive evidence, inspection depth, unresolved hypotheses and invalidation conditions in the supporting explanation or the guide's evidence notes. Do not conceal them, but do not inject “this is only our claim” or instructions to the agent into manuscript prose. Preserve a qualification in the prose when omitting it would materially overstate the result. This is separation of presentation from proof, not permission to polish an unsupported gap into fact.

For a decision-sensitive motivation experiment, compare the available actions under the relevant conditions and measure the target outcome. If the interpretation depends on where the bottleneck is, check it independently, for example by selectively relieving the suspected bottleneck and measuring the end-to-end effect. A different action can win even when the same operation still limits performance. A mere change in the largest time share cannot establish either finding. Specify the observation that would show the extra information adds little. When shortening the answer, preserve which effects were measured, which were inferred and for which methods the evidence holds.

## Evidence stop rule

The search is sufficient for the current claim when the closest solution families and strongest counterevidence have been inspected and new queries no longer change the boundary. If access or coverage remains material, keep the result provisional and name the blind spot.

The final handoff should state the problem, importance, closest surviving gap, evidence status, and collapse condition without implying that a few papers prove novelty.
