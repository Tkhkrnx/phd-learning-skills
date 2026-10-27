# Deep method-design workflow

Use this reference when several mechanism families, cross-domain ideas, or implementation carriers must be compared.

## 1. Root challenge

Explain how the nearest methods fail under the agreed conditions, then derive the causal obstacle. A challenge is not a symptom, module name, or restated feature. Separate a fundamental constraint from an incidental implementation defect.

## 2. Candidate principles

For each serious candidate, record:

- source and original problem;
- transferable principle;
- assumptions and available signals;
- target-system mapping and feasible carrier;
- control granularity and reversibility;
- latency, memory, complexity, transition, and maintenance costs;
- the condition under which the analogy breaks.

Use either entry route, according to the request:

- **Problem-led:** derive a structural obstacle from the agreed problem and closest failures, then search same-field, adjacent and distant principles that address it.
- **Principle-led:** when the user seeks inspiration, understand a source-domain problem and mechanism first, then locate a naturally occurring analogous condition in the target research direction. Establish its importance and nearest-work boundary before promoting it to a research problem or a settled method.

Same-field work calibrates prior capability; it is not an endless prerequisite that crowds out the requested cross-domain exploration. For a useful transfer, show the source problem and why its mechanism works, a concrete target example, assumptions that survive or break, and the target design decision changed by that reasoning. If deleting the source-domain label leaves an unchanged proposal, the analogy has not yet contributed a design.

Repositories, docs, issues, benchmarks, and engineering articles establish implementation facts; they do not independently prove academic novelty. If the user asks to understand a collection of principles, deliver that explanation rather than forcing every principle into a mature paper topic.

## 3. Fact gate

Inspect the target hardware, runtime, code path, state ownership, and control scope. State what can change per request, batch, epoch, deployment, or not at all. Reject a mechanism whose carrier cannot produce the claimed effective behavior.

## 4. Alternatives and assumptions

Expose the assumptions the causal path actually needs. Construct the strongest lower-cost or standard alternative and compare it only on dimensions relevant to the claimed gain. A more elaborate method is not preferred without discriminating benefit.

## 5. Kill criterion

Choose a measurement that separates mechanism failure from implementation noise. Define the evidence unit, denominator, baseline, controlled variable, outcome, and result that would abandon or fundamentally revise the method.

## 6. Synthesis and first experiment

Combine only compatible elements. Check shared state, interfaces, resource costs, and competing actions; one element may address several challenges. Prefer the smallest experiment that distinguishes the causal claim from the simpler explanation.

For data reuse or measurement work, inspect raw fields and collection code, missingness, confounding, and generalization limits. A logged proxy is not automatically the claimed quantity. For runtime mechanisms, distinguish selected, applied, effective, and measured outcomes.

Finish with the integrated causal chain, alternative, costs, kill criterion, first experiment, and the residual uncertainty most likely to change the design.

## Search progress and constructive revision

After a search round, identify what evidence changed the problem, mechanism or ranking. A larger bibliography, more rejected topics or peer agreement is not by itself progress toward a usable method. If searches repeat known objections, consolidate and change the structural query or derivation rather than running the same search loop. This ends a search round, not an explicitly requested continuing investigation.

When a close method appears, distinguish full coverage, a supported residual condition, and an opportunity requiring a different mechanism. Explain the best defensible adaptation or why it fails; do not fabricate a gap to satisfy a topic count. Keep a small implementation optimization labeled as such instead of inflating it into a new architecture. Simple mechanisms remain valuable when their problem, insight and evidence justify them.
