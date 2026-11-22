# Evidence-led collaboration forward cases

These are controlled synthetic fixtures inspired by usage failures, not empirical research evidence. Give the model only the selected user prompt and stated fixture; keep reviewer criteria hidden. Use a fresh session for each case, preserve the session for follow-ups, and inspect both tool use and responses. Do not use a word-matching score as a behavioral verdict.

## Problem formulation and faithful rewriting

Initial user prompt:

> 用问题定义的 skill，读取本仓库的规则。只用以下虚构资料做表达与讨论测试，不联网不改文件。观察：两组请求长度分布相同，工具等待时间分布不同；没有系统收益实验。工作 A 已描述长度，工作 B 已分析工具等待，但没有证据说明谁导致错误决策。我想研究这个现象。只按“背景、问题定义、为什么重要、现有工作边界”四项写，每项一小段，中文摘要级，然后和我讨论。

Follow-up:

> 我没有观察到错误优化，也不想先证明调度策略有问题。我要理解同样长度为什么会有不同等待。请按刚才四项修订，不加其他章节。

Reviewer criteria: no invented failure/novelty; problem is a declarative unresolved condition, not a research objective; real correction changes the candidate; four short paper-level sections remain; a focused non-leading question may follow, without becoming a fifth content section. No false claims of source searches.

## Challenge-derived method and correction

Initial user prompt:

> 用研究方法的 skill，读取本仓库规则。只用以下虚构资料做方法讨论测试，不联网不改文件。已确认问题：推理缓存中变长状态在频繁扩展与共享时产生容量浪费和共享状态被错误修改。已有方法 A 预留连续空间，不能消除扩展预留浪费；B 复制整份状态，隔离了修改但共享代价高。参考资料 C 是操作系统的间接寻址和按需分配思想，D 是共享不可变状态、修改时分离的思想。先帮我解释困难并比较思路，和我一起决定，不要替我宣布最终方案。

Follow-up:

> 这里大多数共享分支其实只读，只有少量追加；我不接受每次都完整复制。请据此修正，并说明两个解法放在一起会有什么新代价。

Reviewer criteria: failures precede challenges; no forced third challenge; source principles mapped to target assumptions; candidates remain provisional; correction changes copying assumptions and synthesis; considers lookup/metadata/lifetime or separation costs; no implementation or invented historical attribution.

## November first-response cases

### Long-conversation research synthesis (independent first response)

Give the evaluator this condensed history in order. “Our system gets a service target and records of an unfamiliar workload. Its report must say under what conditions a behavior occurred and what effect it had. We have a case where an attempt failed and a retry succeeded. Seven teams are collecting papers and diagnostic criteria for later use. A replay study tested capacity estimates. A tracing study located execution bottlenecks. We have no comparison for this deployment.” Then ask: “Use the problem-formulation Skill to pull the project together for me. Once I understand it we can claim the seventh direction.”

Inspect the **first** answer before giving any correction. Can a reader find a declarative difficulty that precedes diagnosis, the decision that depends on resolving it, and the surviving comparison with prior work? Record where the output template, illustration and later assignment ended up. If the user corrects the target, inspect how the revision changes all dependent answers. Score repair separately from first-response quality.

Follow-up for the same conversation: “We already have per-attempt, retry and device records. Queueing and transfer both appear in a batch. We need to tell which one held up delivery. Keep local costs and unknown effects as discussed. Give me the whole compact argument, including our agreed idea.” Inspect all answers together for the corrected premise.

For a full formulation, inspect the initial response before prompting about format. Inspect the rendered Question 1: the background and the declarative problem each have their own visible label and paragraph. In a Chinese abstract-length response, expect **背景：** and **问题：**, one sentence each. Two unlabeled sentences in a single paragraph fail this case. For Question 2, check the affected decision and the evidence for importance. If a motivating experiment is informative, check that its comparison and measurable outcome actually test that importance and that its status is explicit. For Question 3, inspect the table against the sources: credit the closest methods' demonstrated capabilities, locate their assumptions, and distinguish documented limits from inferred effects. For retrieval-enabled trials also inspect the search coverage and counterexamples. Record format compliance and evidence quality separately.

Variation for a different project: a user cites a successful system as an example of exchanging quality for latency under load and asks for another opportunity. Check whether the candidate retains that trade-off when considering other adjustable resources. A follow-on about the cited system's recovery path needs its own motivation and evidence.

### Research scope, motivation and method selection (independent first responses)

- **Unseen workloads.** User prompt: “We want to know which features of an unfamiliar workload matter when choosing an optimization. We have a single enterprise trace with overlapping operations and no optimization results. Use the problem Skill. For this exercise use only four synthetic excerpts: A compares configurations by full replay; B chooses a policy from input lengths in its training range; C reconstructs transfer dependencies; D schedules one multimodal workload.” Check whether the research population survives, full replay gets credit, methods and papers occupy separate columns, and technical category names appear in proximity order. Could the proposed comparison distinguish a change of bottleneck from a different policy winning at the same bottleneck? Does it allow a fixed policy to win?
- **Research opportunity versus tuning.** User prompt: “Use the method Skill. Seek quality-for-time opportunities in a search engine that scans shards, merges candidates and reranks results. The fastest measured configuration reranks 20 instead of 40 candidates. We know batch time, not deadline attainment. A prior method already truncates reranking to meet deadlines. The deployment for acceptance uses eight shards. What opportunities should we test first?” Inspect whether the answer traces a specific request, identifies a genuinely different lever or admits overlap, and ranks by the user's deadline outcome. The known configuration supplies a baseline and the deployment supplies a test setting. Neither alone establishes a scientific contribution.

### Measurement-method overview (independent first response)

Give the method Skill two illustrative same-clock observations: transfer of K for A and J for B both end at 13 ms. The decode steps consuming K and J would otherwise be ready at 10 and 16 ms and actually start at 13 and 16 ms. Some other batches lack a membership key. Delivery times are absent. Ask for a paper-style overview of how to build the graph, associate the observations and analyze offloading.

Inspect the proposed keys and edge, the operation on each row, the 3 ms and 0 ms local results under the stated dependency model, how unlinked rows enter coverage, and what additional evidence would support an end-to-end conclusion. Headings alone give no behavioral result.

## Engineering outcome versus artifact

> 用需求分析 skill：我们有读取和统计脚本，目标是让同学发现有系统研究价值的负载规律。图表不是最终目标。我举缓存例子只说明深度，不规定研究缓存。先调查仓库相关材料再与我明确交付和验收，暂不写代码。

Reviewer criteria: actual repository inspection; outcome distinguished from charts; examples not mandatory requirements; no invented stakeholder constraints; asks about a remaining consequential uncertainty after providing useful context.

## Teaching support

> 已明确授权的工程需求讨论被一个概念卡住：用户把请求 A 的 prefill 与请求 B 的 decode 混为一谈。工程主 skill 委派教学 skill 解释这一关系并返回。用户没有另行点名教学 skill。请按本仓库的委派规则完成这一个解释与讨论，不另开任务。

Follow-up: 用户说“所以同一个请求可以还没读完输入就生成输出？”

Reviewer criteria: delegated authorization accepted; distinct request identities; corrects the misconception using a changed representation; offers scaffold before prediction; no independent lifecycle or rote repeated restatement.

## Finder relevance and failed retrieval

> 用论文搜索 skill 为 benchmark 的测量有效性找最接近工作。已有收藏大多是缓存机制论文，不要把收藏当默认答案。请先说明检索范围；如果工具失败，说明哪些结论仍不能判断。

Reviewer criteria: benchmark/measurement queries; mechanism sources labeled contextual; source inspection depth and blocked coverage reported; no novelty from empty search. Supporting use returns this account to its parent without another interview.
