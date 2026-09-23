# Seven-question speaking and evidence guide

Use these questions to build an explanation the user can present and defend. Adapt the amount of space to the paper and the supplied PPT; do not force equal-length sections.

1. **What is the problem?** State the top-level condition or limitation in a sentence. Then add the scenario, affected object, observable consequence, and boundary. Keep a cause or proposed fix out of the problem sentence unless the evidence requires it. DSpark's draft quality and verification waste are two causes of the broader failure to turn parallel drafting into serving gain, not automatically two separate research problems.
2. **Why it matters?** Explain why the condition affects the actual target workload, system, or user. Evidence may be a measurement, concrete case, or sound causal argument. Do not substitute the new method's speedup for the problem motivation.
3. **Why existing works fail?** Group the nearest approaches by the distinction that matters, state what each already solves, then identify the remaining mismatch with this paper's target. Do not present mere difference as failure or omit a strong nearby alternative.
4. **What is the key idea?** Show which obstacle the insight addresses and why it could work, with assumptions and the simplest useful contrast.
5. **What is the design?** Start with the whole execution path. Explain each component's input, action, output, owner, and interaction with the next component. Include equations only when their variables clarify a decision. Distinguish the proposed algorithm from the deployed engineering approximation.
6. **What is the experimental plan?** First state setup, metrics, and fair baselines. For each pivotal figure or table give: question, compared conditions, observation, supported claim, and evidence boundary. Organize by research claim when that helps a listener; do not merely recite figure numbers or overlook a pivotal result.
7. **What is the takeaway?** State what the evidence supports, the scope where it supports it, and one transferable insight. Keep hypotheses and future directions distinct from demonstrated findings.

Present a short answer before its technical explanation. When the user's later correction changes the abstraction level, revise the whole causal story rather than appending a correction paragraph while leaving the original framing intact. When no user note exists, do not manufacture a correction section. When the note is partial, fill its gaps from the paper without treating the blank sections as mistaken claims.
