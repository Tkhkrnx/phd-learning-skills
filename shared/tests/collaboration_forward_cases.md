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
