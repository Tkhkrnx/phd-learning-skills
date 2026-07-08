# Self-Test: Targeted Knowledge Closure

## Task

Simulated user request:

"I think retrieval practice means repeatedly reviewing notes until memory becomes stronger. I need it for designing a better PhD learning workflow with AI, and I do not understand why recall would be better than rereading."

## Step 1: Minimum input

```md
- what I think this concept means: retrieval practice means repeatedly reviewing notes until memory becomes stronger
- where it blocks me: I need it for designing a better PhD learning workflow with AI
- what confuses me most: why recall would be better than rereading
```

## Step 2: Workflow artifacts

### `knowledge-closure-note.md`

```md
# Knowledge Closure Note

## My current model
Retrieval practice means repeated review of the same notes.

## What is wrong or missing
- It confuses review with retrieval.
- It ignores the role of memory reconstruction.
- It does not explain why difficulty can improve retention.

## Corrected model
Retrieval practice means actively pulling information from memory with limited cues, then checking and repairing the recalled answer.

## Task-local meaning
In an AI-assisted PhD workflow, this means I should first explain a concept from memory before asking the agent to correct or expand it.

## Near transfer case
Before asking the agent about "state-space model", I should first write my own explanation and then ask for correction.

## Far transfer case
Before a design review meeting, I should first reconstruct the design rationale from memory rather than re-reading the full document immediately.

## Independent restatement
Retrieval practice is not repeated note review. It is the act of recalling knowledge first, then comparing the recalled answer against reality and repairing the gaps.
```

### `transfer-check.md`

```md
# Transfer Check

## Near transfer result
Pass. The user can apply the idea to AI-assisted concept learning.

## Far transfer result
Partial pass. The user can see how retrieval applies to design rationale, but may still need one concrete example.
```

## Rubric

- Entry friction: 2
- Role discipline: 2
- Artifact completeness: 2
- Evidence grounding: 2
- Decision ownership: 1
- Transfer: 2

## Total

11/12

## Problems found

- The skill is strong on explanation and transfer.
- It is weaker on explicit user decision points because knowledge closure often lacks a natural decision record.

## Callback conclusion

Improve the skill by requiring the user to explicitly choose one corrected formulation to keep and one context in which they will apply it next.
