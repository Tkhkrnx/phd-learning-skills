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

Search same-field work first, then adjacent systems and structurally similar distant fields when they add a different causal lever. Repositories, docs, issues, benchmarks, and engineering articles establish implementation facts; they do not independently prove academic novelty.

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
