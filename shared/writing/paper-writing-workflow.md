# Shared paper writing and revision

Keep the systems/HPC skill as the primary entrypoint. Choose the stages needed by the user's task, not a mandatory research pipeline for every paragraph.

## Contribution and section logic

Recover the current manuscript version, verified results, target passage, intended contribution, and user's terminology. A substantial rewrite starts with the argument: phenomenon -> importance -> closest work's actual capabilities/assumptions -> concrete limitation and consequence -> contribution -> supporting result. A contribution may be a mechanism, method, analysis, or empirical finding; do not force a new system narrative.

Maintain a claim-evidence map only at the granularity needed: claim and scope, manuscript location, source/result locator, what was actually inspected/run, and outstanding gap. Engineering tests, real runs, scoring, attribution, and scientific conclusions are different evidence. Compare closest work fairly before naming a difference. If evidence is missing, narrow or label the claim rather than polishing it into a fact.

## Citation support

Bibliographic identity and claim support are separate checks. Use `reference-validation-report` to verify identity/metadata when needed, and `nature-academic-search` to discover a missing source. A real DOI does not show that the cited paper supports this sentence.

For a decisive claim, inspect the original passage/figure/table and record the citation key, exact locator, condition, and relation: supports, partially supports, contradicts, or not inspected. Check population/workload, hardware, precision, budget, metric, and causal versus correlational wording. Read the context around a quote, not only a retrieval hit. Do not silently replace a citation with a merely topically similar paper.

## Humanizer pass

Use the user's writing sample and venue style first. Remove staged importance, stock transitions, empty contrasts, repeated closers, forced triads, promotional adjectives, and excessive formulaic headings when they add no information. Rebuild a paragraph around its actual point rather than swapping a blacklist of words. Preserve natural technical terms and deliberate contrasts; do not randomize prose to imitate humanity.

Edit prose only unless more was requested. Preserve facts, numbers, conditions, equations, code, commands, citation keys, links, labels, and epistemic strength. In a manuscript, return the requested final passage or patch, not chat scaffolding or an unsolicited before/after essay. This is writing improvement, not an AI-detector evasion guarantee.

## Non-defensive, evidence-bounded prose

State the supported positive claim directly. Remove repeated apologies and disclaimers that add no scope, mechanism, or evidence. Replace vague hedging with its real condition or uncertainty. Place a methodological limitation where the reader needs it; keep it in the abstract/result sentence if omitting it would mislead there.

Never suppress adverse results, overhead, failed cases, strong baselines, or meaningful validity limits. Do not change the question, metric, comparison, or workload to make the contribution look better. Reject advice to only report wins or weaken inconvenient comparisons. Stronger writing comes from evidence and precision, not stronger certainty.

## Reviewer response and resumable revision

For a revision task, create or update the project's existing response/revision matrix; avoid a parallel tracking system. Track review ID and verbatim concern, interpretation, action, manuscript location, evidence/test/result, status, and unresolved disagreement. Distinguish proposed, changed, verified, and deferred. A proposed experiment is not a completed revision. Retain review IDs across drafts.

Use `revision_tracker.py` for deterministic path/locator/status checks if a machine-readable matrix is useful. Its check cannot assess whether the scientific response is adequate. Re-read the revised context, check facts/citations/conditions against the prior version, and verify the linked evidence before calling a row verified. A user's final assessment remains theirs; do not silently change their review judgment.

Run `python shared/writing/revision_tracker.py --input revision.json --project-root <paper-dir>`. The JSON shape is `{"revisions": [{"id": "R1.2", "concern": "original review concern", "action": "specific response", "status": "proposed"}]}`. Changed/verified rows add `locations: [{path, line, anchor}]`; verified rows also add `verification` and `evidence: [{path, line, anchor}]`. Paths are relative to the project root, lines are one-based, and anchors must match that line. Deferred rows add `reason`. These are traceability checks, not automatic claim-support judgments.

On resume, recover the current draft and unresolved matrix rows, not an obsolete outline. Stop unnecessary full-pipeline approvals; ask only when contribution/scope/interpretation materially depends on the user's decision.

## Sources and adaptation boundary

Independently written integration informed by [Humanizer](https://github.com/blader/humanizer) (MIT), [Kiterlin anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing), and [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) (CC BY-NC 4.0). No upstream prompts/code are vendored here. The selective integration does not install their plugins, import their multi-agent/approval machinery, or claim a calibrated scientific reviewer.
