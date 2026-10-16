# Explain a paper from its evidence

Use this reference when producing a reading note, review analysis, or paper presentation. It governs explanation quality, not Skill activation or a new research-method search. The user's requested format and latest correction remain authoritative; factual wording must remain supported by the paper.

## Establish the argument before shortening it

- Problem: use the abstract's background and unmet need, expanded by the introduction and checked against the full paper. State the condition before its cause or solution. Preserve terms such as achievable performance versus a proven theoretical upper bound.
- Importance: use application consequences, cited context, and motivation measurements. Explain the loss and why it matters before the detailed mechanism. A method's improvement is not itself motivation evidence.
- Prior work: start with the authors' related-work categories and their actual strengths. Distinguish remaining limitations, different objectives, and complementary work. Additional interpretation must not masquerade as the authors' classification.
- Idea and design: preserve the authors' hierarchy of questions, challenges, design goals, and mechanisms. An abstraction layer and a runtime layer may have different challenges. Follow that structure rather than manufacturing one flat list.

Before drafting, keep a small working map of **source section/paragraph -> problem or goal -> design or evidence -> destination in the note/deck**. It is a working aid, not an extra user deliverable unless requested. Include text-only experiments and algorithms as well as images. Use it to check completeness after revisions.

## Choose the right explanation for the evidence

**Overview.** Explain the system object, major responsibilities, information/control relationships, and why the arrangement addresses the problem. Use the authors' insights to justify those choices. Do not turn numbered insights into invented chronological steps, or drown the overview in the scheduler's later implementation details.

**Mechanism or process.** Identify who acts, on which object, from which state, under what condition, and with what next state. Explain arrows, queues, ownership, memory regions, and transfer directions where they affect understanding. Preserve distinctions such as one request versus a batch, an object's lifetime versus its execution steps, logical state versus physical storage, and parameter loading versus KV offloading. Avoid a simplified one-to-one analogy when the source defines a richer relationship.

**Code or algorithm.** Read the actual figure/pseudocode together with the relevant prose. Explain inputs/outputs, variable units, branch conditions, loop order, and how a helper algorithm relates to the outer algorithm. Distinguish installing a wrapper, creating a coroutine, executing a module, retaining state, and handing back control when those are different operations. A placeholder comment does not implement the omitted logic. Label explanatory pseudocode or a worked example as editorial, and do not assert undocumented field semantics.

**Measurements.** Read the axes, units, scales, legend, annotations, table groups, baseline and footnotes before explaining a result. Distinguish what is plotted, what follows from an explicit calculation, what the authors infer elsewhere, and what was not measured. For example, batch size and execution time can support a throughput calculation; they do not directly measure GPU utilization. An arrow may mark a working range rather than a performance curve. A combined optimization's gain cannot be attributed to one component without evidence.

**Experimental setup.** Separate models/hardware, datasets/application workloads, baselines, configurations/deployment scales, and metrics/protocol. A workload is not a GPU count, and a deployment comparison is not a dataset. Provide a compact overview for one slide, with experiment-specific parameters adjacent to their results; do not expand the overview into every configuration in the paper.

## Make the explanation usable

Explain the original account in accessible professional language, keeping the technical nouns needed to recognize the source. A short purpose/conclusion pair is an index, not an explanation of a difficult figure. Expand a dense subfigure or algorithm enough to let the reader explain what happens and why; avoid exhaustive prose for a simple plot.

For note headings, an author's explicit question or a faithful summary of their design goal can help connect the argument. For slide headings, preserve the supplied hierarchy and prefer the authors' section subjects unless the user has chosen a question-based structure. Questions asked during discussion diagnose missing explanation; they do not automatically become new sections or slides.

Keep necessary qualifications next to the claim they change. Collect other editorial issues in the note's writing/details section. Do not interrupt every explanatory paragraph with an unrelated audit warning.

## Re-read after a correction

When a user finds a wrong concept or missing explanation, update the affected paragraph, table row, linked overview, mechanism description, experiment interpretation, and takeaway wherever they depend on it. A correction appended at the end does not repair contradictory earlier prose.

Check related-work rows independently, reconcile the source map with the actual output, and read the explanation as a listener would. Structural validators cannot establish that an algorithm is explained, a chart is interpreted correctly, or the argument can be retold.

When the user supplies an accepted note or talk as the quality reference, compare the generated explanation itself with that reference: can the reader recover the problem, the authors' challenge/design hierarchy, the essential algorithm or data flow, and why each result supports its conclusion at comparable depth? Rework missing causal links rather than declaring success because all headings and figure labels are present. Preserve that standard while adapting the amount of detail to each new paper and the requested scope.
