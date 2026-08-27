# Research Evidence Acquisition Protocol

This reference is mandatory for `research-problem-formulation` and `research-method-design`. It governs evidence acquisition before a problem or method is frozen. Search is agent labor; scientific commitment remains collaborative.

## Non-Negotiable Invariant

Do not make a strong claim that a problem is real, important, unresolved, or method-worthy before searching for evidence capable of overturning that claim. An initial framing may guide search, but it stays provisional.

Broad intake does not mean a literature dump. Search widely, inspect decisive sources, then show the user the small set of evidence that changes the boundary or decision.

If search is unavailable, primary sources cannot be inspected, or a material query family remains uncovered, disclose that limitation and do not freeze novelty, unresolved-status, or method-superiority claims.

## Two Evidence Modes

### Problem-boundary evidence

Search to determine whether the proposed phenomenon and gap survive. Cover:

- the phenomenon, system object, operating condition, consequence, and metric under their common synonyms;
- seminal work, current best work, surveys or benchmarks that map the area, and the closest solution families;
- counterqueries such as already solved, equivalent capability, negative result, limitation, failure case, and easier neighboring conditions;
- backward and forward citation chains from the closest work when tools permit;
- evidence that weakens the motivation, collapses the boundary, or reclassifies the work as routine engineering.

Use surveys to map vocabulary and neighborhoods, not as sole proof of novelty. Use primary papers, official proceedings, artifacts, and measured system evidence for decisive claims.

### Mechanism-inspiration evidence

Search for causal levers, not only papers sharing the application label. First express the root challenge as a structural signature:

```text
actor/object + state or resource + constraint + observable signal + controllable lever
+ decision granularity + reversibility + cost + failure mode
```

Then search several lanes:

1. the same problem and field;
2. adjacent systems, architecture, networking, databases, operating systems, control, optimization, and programming-language work;
3. distant fields that share the structural signature, without assuming their terminology or implementation transfers;
4. repositories, official documentation, issues, pull requests, benchmarks, engineering articles, and technical blogs that reveal implemented mechanisms or failed attempts;
5. negative evidence showing why an attractive mechanism fails under the target constraints.

Cross-domain observation is a hypothesis source, not design proof. For every borrowed idea, record the transferable principle, original assumptions, target-system mapping, carrier, cost model, and the condition that breaks the analogy.

## Query Portfolio

Before searching, form a small portfolio rather than one oversized query. Include as applicable:

- direct phenomenon or mechanism terms;
- synonyms and older terminology;
- object-condition-metric combinations;
- closest known technique and competitor families;
- failure, limitation, overhead, counterexample, and negative-result terms;
- structural-signature queries that omit the target application name;
- exact-title, author, citation, or artifact follow-ups from strong seeds.

`topic-paper-finder` may supply the academic candidate pool in `problem-boundary` or `mechanism-inspiration` mode. When a research collaboration skill is already active, use it as an internal evidence backend rather than starting a second user-facing skill lifecycle or interaction protocol. It does not replace opening decisive primary sources. Non-paper evidence requires the available web, repository, documentation, and code-search tools.

## Evidence Ledger

Maintain a compact internal ledger during the run:

| Field | Required content |
|---|---|
| query family | what boundary or mechanism the query tests |
| source and role | primary proof, map, implementation fact, lead, or counterevidence |
| supported claim | the exact claim the source supports |
| strongest threat | how it could solve, weaken, or invalidate the candidate |
| unresolved gap | what remains unknown after inspection |

Keep evidence, inference, and hypothesis separate. A blog or repository can establish an implementation fact or reveal a lead; it normally cannot alone establish academic novelty. A paper title or search snippet is not evidence that its full method or assumptions match.

## Coverage and Stop Rule

Do not stop because an arbitrary paper count was reached. Stop a search round when one of these holds:

- decisive counterevidence collapses or materially redirects the candidate;
- new queries and citation follow-ups mostly repeat already-covered solution families and assumptions;
- the closest-work set, strongest counterevidence, and material source gaps are stable enough for the next user exchange;
- further search is blocked, in which case the blocked coverage and resulting uncertainty are explicit.

Never claim to have found "all papers." State the searched query families, source types, time/venue limits if any, and remaining blind spots. Reopen search whenever the user changes the problem object, condition, metric, root challenge, or mechanism family.

## Collaboration Boundary

The agent should perform query expansion, retrieval, source triage, and evidence organization. The user should not be asked to guess discoverable facts. The agent then presents the decisive evidence and asks the user to challenge the boundary, causal interpretation, assumption mapping, or trade-off. Search completeness alone does not satisfy the meaningful-exchange gate.
