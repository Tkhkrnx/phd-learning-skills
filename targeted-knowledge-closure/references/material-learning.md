# Material-grounded learning

## Choose the learning unit

Use the requested concept, chapter, skill, or research task as the unit. Inspect the supplied sources before planning; if none exist, locate authoritative materials before attributing claims. A small question needs a small explanation, not a generated textbook.

For a course/chapter, show the destination and a prerequisite graph: concept ID, prerequisite IDs, expected usable action, and source locator. Prior knowledge is a working hypothesis until the user's reasoning supports it. Offer a diagnostic only where it changes the path. Distinguish unknown, practicing, demonstrated-in-this-case, and needing review; do not invent a mastery percentage.

## Teach from sources

- A paper supplies claims, methods, assumptions, and experimental evidence; a textbook supplies definitions and derivations; code supplies actual implementation behavior. Track which is being used.
- Reuse available MinerU extraction or local parsed notes when they match the source version. For an equation, table, or visual mechanism inspect the relevant original page. Record unread or inaccessible sections rather than claiming complete coverage.
- For multiple sources, align terminology and conditions explicitly, retain disagreements, and select the source appropriate to the question. A retrieved passage is a candidate, not proof of an entire argument.
- Explain definitions, mechanism, worked example, boundary/counterexample, and application only as needed. For a process retain actor, state before/after, operation, and order. For a derivation keep assumptions and intermediate transformations visible.

## Solve and practice

Separate solving a supplied problem from teaching the method. If guidance is requested, expose the next useful hint, then a substep or worked example if stuck, then a nearby task with reduced hints. If a full answer is requested, provide it directly; do not force a Socratic interview.

Create exercises with concept ID, source locator, prompt, answer/rationale, and a plausible near-miss or transfer target. Keep answers separate from the question when the learner is practicing. Assess the actual submitted response, explaining the decisive mismatch: prerequisite gap, object/state confusion, algebra, invalid assumption, implementation, or transfer error. Revisit the dependency that caused the error instead of restarting the entire lesson.

Do not record an agent's sample answer as a user attempt. Correctness of one item does not establish general mastery. A new-context application is stronger evidence than repeating the explanation. Review dates are local suggestions, not scheduled reminders; creating an automation requires a separate user request.

## Durable sessions and learning guides

Only persist when the user asks to keep progress/notes, requests a durable course, or explicitly provides a destination. Existing Obsidian notes remain the primary learning library. Use one session state alongside the learning guide, not a second conflicting mastery database.

`scripts/learning_session.py` supports `init`, `plan`, `exercise`, `attempt`, `status`, and `export`. Run `--help` and the matching subcommand's help for inputs. A plan JSON contains `concepts: [{id, title, prerequisites, source}]`. An exercise JSON contains `id, concept, prompt, answer, source`. `source` is a human-checkable page/section/code locator; judgments remain the tutor's responsibility.

The state records source fingerprints, goals, dependency graph, exercise bank, actual attempts, feedback, error type, and optional review date. `status` reports changed/missing materials and due reviews; `export` creates a readable guide/progress record without overwriting an existing file. Do not interpret file hashes, structural validity, or recorded assessments as independent pedagogical validation.

On resume: inspect state and requested scope, check changed sources, read the last unresolved attempt, and continue from the relevant prerequisite or next application. Revalidate only affected concepts after a source update; retain the prior evidence and label it stale. Do not silently replace historical attempts.

For a requested chapter-style guide, organize around the dependency path with source links, concise explanation, examples, exercises, and open questions. Add diagrams or small executable examples when they materially explain the relation. Use the current environment's visualization/code tools, disclose execution results, and never claim a diagram or simulation was run merely because code was written.
