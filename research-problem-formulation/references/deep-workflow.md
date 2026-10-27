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

Recover the current research objects, intended outcomes and exclusions from the latest user reasoning. Distinguish research materials from the scientific object: production requests and several workload families do not imply an Agent-only question. Neither a familiar example nor an older guide may silently narrow a newly reopened scope. Preserve distinct objectives when compressing too: a prefill example must not displace a separate fidelity question. Present a focused unresolved choice only when it can change the framing; do not turn this check into a questionnaire.

When new evidence conflicts with a frozen item, show the conflict and smallest revision. Preserve the user's terminology and requested structure.

## Explain the nearest-work failure

For each consequential comparison, connect the work's real achievement to the mechanism or assumption it uses, the relevant target condition, and the resulting limitation. Cite the source location for established facts; label an inferred mismatch or proposed counterexample as such. A different objective, unimplemented feature or limited evaluation scope is not by itself a demonstrated failure.

- Insufficient: “Prior work does not provide our integrated benchmark generator.” This defines the gap by the proposed solution.
- Useful investigation: a generator preserves request statistics, while the candidate target concerns execution-dependent pressure. Inspect what the generator actually represents and validates, then identify a concrete condition under which that representation would omit a relevant effect. Until that condition and its consequence are supported, it is a hypothesis to test, not a verified deficiency of the named work.

Compare against the strongest simple composition as well as individual papers. If it already addresses the target condition, remove that gap. If a different condition creates a genuine problem, explain why that condition occurs and matters rather than adding artificial restrictions to defeat a competitor.

## Paper-facing answer and supporting record

Use the requested length and language. For abstract-style output, background and problem should read as opening manuscript sentences, not a research checklist. Answer importance and existing-work failure in their own roles; avoid repeating all three answers in the problem sentence.

Keep decisive evidence, inspection depth, unresolved hypotheses and invalidation conditions in the supporting explanation or the guide's evidence notes. Do not conceal them, but do not inject “this is only our claim” or instructions to the agent into manuscript prose. Preserve a qualification in the prose when omitting it would materially overstate the result. This is separation of presentation from proof, not permission to polish an unsupported gap into fact.

For example, if “a parameter change could affect several stages” is only a proposed counterexample, compressing it to “generated loads distort real bottlenecks” adds an unmeasured conclusion. Describe the specific unresolved control or fidelity relation instead, retaining “may” or an equivalent scoped formulation where necessary. A causal claim established only for one cited method cannot silently become a failure of the whole field in the abstract.

## Evidence stop rule

The search is sufficient for the current claim when the closest solution families and strongest counterevidence have been inspected and new queries no longer change the boundary. If access or coverage remains material, keep the result provisional and name the blind spot.

The final handoff should state the problem, importance, closest surviving gap, evidence status, and collapse condition without implying that a few papers prove novelty.
