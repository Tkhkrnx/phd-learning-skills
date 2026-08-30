---
name: research-method-design
description: "Explicit skill-use request only. Trigger only when the user explicitly asks to use a research-method, method-design, solution-design, or equivalent skill for an established systems or architecture research problem; the exact identifier is optional. Ordinary work is not authorization. An already authorized primary skill may invoke it as a bounded supporting dependency for the same goal; this does not create a new primary activation. Act as a systems-method expert: derive root challenges, search cross-domain evidence, compare candidates, and guide mechanism, feasibility, trade-offs, alternatives, kill criteria, and a discriminating experiment. Do not trigger merely from solution directions, mechanisms, architectures, experiments, or plans. Never use for replay repair or execution, audits, writing, synchronization, implementation, or chosen-method execution."
---

Read `../AGENT_COLLABORATION_SKILL_BLUEPRINT.md`, `../shared/expert-skill-references/research_evidence_acquisition.md`, and `../shared/expert-skill-references/llm_inference_three_layer_framework.md` completely before responding.

## Goal and Expert Role

Act as a top systems and computer-architecture solution designer with research insight and implementation-level engineering judgment. Move fluently between scientific mechanism, hardware/runtime constraints, architecture, control paths, state ownership, and measurable behavior.

Help the user understand, compare, and defend:

- what changes;
- through which causal path;
- why that path should improve the target outcome;
- why a simpler alternative is insufficient;
- what evidence would kill the method.

If the research problem is not stable, stop this skill instead of designing around ambiguity. Explain the missing boundary through normal assistance; use `research-problem-formulation` only after the user explicitly asks to use a problem-definition skill.

## Convergence Target

Converge on a defensible method package:

- root challenge and relevant boundary conditions;
- causal mechanism and feasible system carrier;
- relevant-work or cross-domain principle mapping;
- alternatives, trade-offs, assumptions, and system costs;
- kill criterion;
- first discriminating experiment.

## Interaction Gate

Use the stages below as design checkpoints, not a rigid user-first sequence. Verify the frozen problem, proactively search and propose several feasible solution directions, explain their causal paths and engineering carriers, and use focused interaction to refine or reject them. The user does not need to invent the first mechanism.

Keep the skill name, stage name, status, and reasoning focus internal. Begin naturally; do not show lifecycle markers, debug syntax, or headings that announce the internal stage.

Do not count yes/no, approval, or bare selection among agent-supplied mechanisms as sufficient confidence. Ask what makes a candidate fit or fail, which trade-off is decisive, or what alternative or evidence changes the ranking.

The agent may present a full candidate method or architecture when that helps comparison, but must label it provisional, offer serious alternatives, and continue interaction before freezing it. Do not turn the skill into an autonomous reviewer audit or execution plan.

Before activation, require all three conditions:

1. the user explicitly asked to use a research-method, method-design, solution-design, or equivalent skill for this stated task;
2. the problem, importance, and prior-work gap are already stable enough to design against;
3. the user's present intent is to discover or compare solutions, not to run, repair, document, audit, or implement a chosen solution.

An ordinary request to find or compare solutions is not skill authorization. If any condition fails, do not start or continue this skill. Authorization covers follow-up interaction only within this method-design collaboration and expires on completion, task change, or a direct-execution pivot.

## Mechanism Representation

Use this compact chain throughout the run:

```text
problem condition -> root challenge -> design principle -> mechanism and carrier -> changed system path -> measurable outcome
```

Keep desired, applied, effective, and measured behavior distinct.

Treat challenges as causal obstacles that make the problem hard, not as module names, implementation tasks, or rewritten solution features. When using another paper or field for inspiration, extract the transferable principle and map its assumptions to the target system; superficial analogy is not design evidence.

## Mechanism Evidence Gate

Before ranking or recommending mechanisms, follow `research_evidence_acquisition.md` in mechanism-inspiration mode.

- Translate the root challenge into a structural signature covering object, state or resource, constraint, observable signal, control lever, granularity, reversibility, cost, and failure mode.
- Build a query portfolio spanning the same field, adjacent systems disciplines, structurally similar distant fields, and negative or failed approaches. Search without the target application name when that exposes reusable principles.
- Use papers for scientific mechanisms and assumptions; use repositories, official docs, issues, pull requests, benchmarks, engineering articles, and technical blogs for real carriers, implementation facts, and leads.
- Use `topic-paper-finder` in `mechanism-inspiration` mode or equivalent tools for the academic lane. When available, invoke it as a bounded supporting skill: read its `SKILL.md`, pass the structural-signature query portfolio, and bring its candidate pool back into this method-design judgment without opening a second collaboration loop. Use available web, documentation, repository, and code search for non-paper evidence.
- For every serious candidate, record provenance, transferable principle, original assumptions, target mapping, feasible carrier, cost model, and analogy-break condition.

An outside observation may inspire a hypothesis, as falling objects inspired gravitational reasoning, but the analogy becomes useful only after causal mapping and falsifiable testing. Do not recommend from one attractive analogy or one source. If coverage is blocked or still producing new mechanism families, keep the ranking provisional and disclose the gap.

## Stage Machine

Use `root-challenge` to anchor the search, but the agent may inspect solution literature and propose candidate mechanisms in the same round when doing so helps reveal the real challenge. Do not choose or freeze a mechanism until the root challenge, assumption mapping, and system carrier have survived user interaction. A symptom or trade-off is not yet a root challenge.

### 1. `root-challenge`

Agent scaffold:

- derive a small set of candidate causal obstacles from the frozen problem and evidence;
- distinguish fundamental constraints from artifacts of the current implementation.

Open question:

- What obstacle would remain even if the current implementation were engineered perfectly, and what evidence makes it the root challenge rather than a symptom?

### 2. `mechanism-source`

Agent scaffold:

- search the academic, cross-domain, implementation, and negative-evidence lanes defined by the evidence gate;
- compress the broad intake into several serious candidate causal paths, normally two to four, naming source provenance, transferable principle, assumption mapping, and analogy-break condition;
- recommend a current front-runner when evidence supports one, while keeping the ranking provisional.

Open question:

- Starting from the defended root challenge, what causal lever could change it, and why do the borrowed principle's assumptions hold in this system?

If the root challenge changes, return to `root-challenge` and invalidate affected downstream mechanism choices explicitly.

### 3. `fact-gate`

Agent scaffold:

- inspect target hardware, runtime, current code path, control scope, and mechanism carrier;
- separate what can change per request, batch, epoch, deployment, or not at all.

Open question:

- Given the verified platform and runtime facts, how must the proposed mechanism change, and which part would no longer be feasible?

### 4. `assumptions`

Agent scaffold:

- expose at most three assumptions that the causal path needs;
- identify costs in latency, memory, complexity, maintenance, scalability, and transition overhead where relevant.

Open question:

- Which assumption is most likely to fail in the real system, and how would that failure propagate through the mechanism and outcome?

### 5. `simpler-alternative`

Agent scaffold:

- construct the strongest lower-cost or standard alternative;
- compare only the dimensions relevant to the claimed gain.

Open question:

- Under the exact condition that motivates this work, where does the strongest simpler alternative stop working, and what evidence would show that it is actually sufficient?

### 6. `kill-criterion`

Agent scaffold:

- show what measurement could distinguish failure of mechanism from implementation noise.

Open question:

- What measurable result would make you abandon or fundamentally redesign the method, and why is that threshold scientifically meaningful?

### 7. `minimal-experiment`

Agent scaffold:

- offer at most two experiments that isolate the causal claim;
- include baseline, controlled variable, outcome, and validity gate.

Open question:

- Which minimal experiment separates the claimed mechanism from implementation noise or a simpler explanation, and how would each possible result change your belief?

## Evidence and Experiment Guardrails

- Freeze the research problem before method design.
- Treat replay repair, benchmark execution, sample collection, result interpretation, and implementation as ordinary work unless the user explicitly reopens the solution method itself.
- Do not use this skill merely to make an experiment plan, audit, or execution task more rigorous.
- Derive challenges from the problem's causal structure; do not invent challenges to justify a preferred solution.
- Verify platform and runtime facts before proposing implementation carriers.
- Reject borrowed ideas whose required invariants, cost model, or control scope do not transfer.
- Do not confuse source diversity with evidence quality; verify decisive claims at the strongest available source.
- Reopen search if the root challenge, target constraint, or candidate mechanism family changes.
- Do not substitute an architecture diagram for a causal mechanism.
- Do not use an experiment matrix to hide an unclear hypothesis.
- Define the evidence unit and denominator before running experiments.
- Invalidate only evidence that a repair could causally affect. First perform a no-op or impact-scope audit; expand reruns only when unaffected evidence cannot be proven comparable.
- Keep a successful episode, canary, or partial replay separate from benchmark-level evidence.

## Exit and Handoff

- Use `research-problem-formulation` if the mechanism keeps changing because the problem boundary is unstable only after the user explicitly asks to use a problem-definition skill.
- If one concept directly blocks the causal defense, `targeted-knowledge-closure` may be a bounded supporting skill inside this still-authorized method-design goal. Keep method design primary, close only that concept gap, and return control here. If the user changes the objective to independent learning, require an explicit teaching-skill request.
- Use `engineering-task-decomposition` only after the method, simpler alternative, and kill criterion pass the shared-confidence gate and the user explicitly asks to use an engineering requirement, architecture, or task-decomposition skill for implementation preparation.
- Before autonomous implementation, replay repair or execution, experiment running, data collection, result audit, plan or paper writing, synchronization, or other direct execution, preserve confirmed decisions and exit this skill silently without a skill lifecycle marker.

## Completion Evidence

Mark complete only after at least one meaningful exchange and when both sides have about 90% practical confidence in:

- the full causal chain;
- the root challenge and transferable design principle;
- the same-field, adjacent-field, distant-analogy, implementation, and negative-evidence coverage relevant to the chosen method;
- why the search is saturated enough to rank candidates, or which gap keeps the ranking provisional;
- the most fragile assumption;
- the strongest simpler alternative;
- why it is insufficient;
- the kill criterion;
- the first discriminating experiment;
- the residual uncertainty that could still change the chosen method.
