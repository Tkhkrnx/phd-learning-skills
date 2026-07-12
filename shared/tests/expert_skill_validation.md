# Expert Skill Validation

This file records practical validation cases for the four expert-facing skills.

The redesign target is no longer just “better expert workflow”.

It is:

- expert–apprentice collaboration

So validation must test two things at once:

1. did the task progress
2. did the user participate in a meaningful piece of expert reasoning

## What failure now means

The redesign fails if the interaction still does any of the following:

- overloads the user with artifacts instead of guiding thinking
- asks the user to pre-structure what they cannot yet understand
- behaves like a generic assistant instead of the right expert
- solves the problem for the user without transferring the reasoning

## Case 1: `research-problem-formulation`

Input style:

- a vague intuition about agent workloads and AI-native systems

Expected expert behavior:

- identify candidate problem framings
- classify the problem into the LLM inference layer framework
- bring in only the most dangerous adjacent work

Expected apprentice interaction:

- the user should be asked small boundary questions they can attempt
- the user should participate in at least one layer judgment or boundary distinction
- the agent should supplement, not fully replace, the user's problem-sharpening move

Pass criteria:

- the skill no longer depends on front-stage artifact maintenance
- the interaction centers on:
  - problem definition
  - importance
  - failure gap
- the user is visibly involved in narrowing the problem

## Case 2: `research-method-design`

Input style:

- a research problem plus a rough method hunch

Expected expert behavior:

- compress the hunch into a mechanism hypothesis
- force a simpler alternative
- expose assumptions
- require a systems cost view
- require a kill criterion

Expected apprentice interaction:

- the user should be asked to explain why the mechanism creates value
- if the answer is vague, the agent should narrow the question rather than invent the whole mechanism immediately
- the user should defend why the simpler alternative is insufficient

Pass criteria:

- the interaction does not collapse into agent-only brainstorming
- the user participates in mechanism defense
- the final output includes a kill criterion and a first validating experiment

## Case 3: `engineering-task-decomposition`

Input style:

- a raw natural-language engineering requirement

Expected expert behavior:

- translate the requirement into system terms
- generate a codebase familiarization plan
- recover the relevant architecture slice
- compare implementation paths with engineering trade-offs

Expected apprentice interaction:

- the user should be asked small system-reading questions they can attempt
- if the user does not know, the agent should point to likely files, modules, or symbols
- the interaction should train architecture recovery before implementation design

Pass criteria:

- the skill does not jump directly to a polished solution
- the user participates in recovering the structure of the system
- the final recommendation includes a first execution slice rather than only a big plan

## Case 4: `targeted-knowledge-closure`

Input style:

- one blocking concept the user does not understand

Expected expert behavior:

- diagnose the user's current mental model
- shrink concept grain if needed
- explain first
- translate terminology into system meaning
- correct the key misconception

Expected apprentice interaction:

- the user should not be asked for a strong explanation before enough scaffold exists
- after explanation, the user should restate a small part in their own words
- then the user should place the concept back into the current research or engineering context

Pass criteria:

- the interaction follows:
  - diagnosis
  - explanation
  - correction
  - transfer
- the user moves from recognition to at least one small transfer step

## Residual risk check

Even with the redesign, the active model may still:

- overexplain instead of asking the next answerable question
- skip the apprentice part and finish the reasoning alone
- skip evidence gathering in engineering tasks
- choose adjacent work too broadly in research framing

Mitigations now present in the skill texts:

- explicit expert profile
- explicit core competencies
- explicit guided interaction strategy
- explicit learning objective
- explicit completion tests requiring user-side reasoning

## Real-user scenario spot checks

### Spot check A: vague research intuition

User-style input:

- “我觉得 agent workload 和 AI-native system 这里有问题，但我说不清。”

What should now happen:

- the agent should help the user clarify the phenomenon
- then ask whether the issue is closer to request, state, or execution
- then use adjacent work to sharpen the boundary
- then co-construct the problem statement

### Spot check B: concept-only learning request

User-style input:

- “帮我学 unified memory，我不懂。”

What should now happen:

- the agent should first diagnose the likely concept grain
- then explain
- then translate the term into system meaning
- then ask for one small restatement
- then one transfer back into the current task

### Spot check C: raw engineering requirement

User-style input:

- “要把这个服务加上请求级缓存，但我不知道项目该从哪看。”

What should now happen:

- the agent should first drive architecture recovery
- ask small system-reading questions
- point to files or symbols if needed
- only then compare implementation paths

### Spot check D: rough method hunch

User-style input:

- “问题我大概知道了，我想做一个 state-aware runtime 优化，但我不知道怎么变成方法。”

What should now happen:

- the agent should first ask where the gain comes from
- then pressure the mechanism
- then compare with a simpler alternative
- then define a kill criterion and first validating experiment
