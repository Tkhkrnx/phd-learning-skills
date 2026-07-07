# PhD Learning Skills

Personal Codex skill repository for research, engineering, and learning workflows during PhD work.

This repository is designed for personal long-term use rather than public marketplace polish. The core goal is:

- improve task throughput with an agent
- preserve and grow independent problem formulation, design judgment, and transfer ability

## Skill Set

- `targeted-knowledge-closure`
  - close one blocking knowledge gap with recall, correction, transfer, and independent restatement
- `engineering-task-decomposition`
  - turn an unclear engineering request into evidence-grounded boundaries, options, decisions, and a first execution slice
- `research-problem-formulation`
  - turn a vague research intuition into a defendable problem definition with evidence and failure hypotheses
- `research-method-design`
  - turn a stable research problem into mechanism candidates, failure modes, and a minimal validation plan

## Shared Design Rules

All skills in this repository follow the same operating rules:

- user-first draft before agent expansion
- one agent role per round
- explicit user decision records
- fixed artifact schemas
- explicit stop rules
- agent-off completion checks
- evidence-grounded engineering claims

See [AGENT_COLLABORATION_SKILL_BLUEPRINT.md](C:/Users/peng/Documents/PHR/Intellistream/projects/phd-learning-skills/AGENT_COLLABORATION_SKILL_BLUEPRINT.md) for the full design specification.

## Repository Layout

```text
phd-learning-skills/
├── AGENT_COLLABORATION_SKILL_BLUEPRINT.md
├── README.md
├── shared/
│   ├── references/
│   ├── scripts/
│   └── tests/
├── targeted-knowledge-closure/
├── engineering-task-decomposition/
├── research-problem-formulation/
└── research-method-design/
```

## Validation Approach

This repository treats skill quality as an engineering problem.

Each skill should be checked for:

- low-friction entry
- artifact completeness
- role discipline
- evidence grounding where relevant
- decision ownership
- agent-off transfer

Shared test cases live under `shared/tests/`.

## Personal Usage Notes

- This repo is meant to stay private unless intentionally cleaned for public release.
- The defaults are optimized for repeated personal use in Codex rather than broad discoverability.
- The shared references and tests are intentionally explicit so future revisions can be checked instead of guessed.
