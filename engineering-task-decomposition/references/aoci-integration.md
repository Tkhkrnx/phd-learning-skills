# Optional AOCI-CODE

Local tool home: `C:/Users/peng/Documents/PHR/Intellistream/study_tools/AOCI-CODE`; the release executable belongs in `bin/aoci.exe`. Use that stable absolute path, not whichever binary happens to be on PATH.

AOCI maintains a model-authored, Git-versioned map of responsibilities, relationships, public interfaces, and constraints. It is not a parser that can infer all semantics automatically, and its index is not source-code authority. Installation alone does not create a useful project index.

For an existing configured project, inspect alignment/source version and use the relevant entries to choose source files. Resolve consequential claims against actual code and tests. Update affected index entries only after the code change is verified. Do not load a whole large index for a trivial isolated task when relevant entries suffice unless that project's explicit protocol requires it.

For new adoption, first choose one repository and inspect its dirty state and instructions. Preview the release's current `init --help` and project changes. Do not run `init` globally or inject MCP into all clients/projects. A new MCP registration may require a new session. Run `doctor` and `scan`; build the semantic index through the actual connected MCP tools, never by fabricating placeholder entries.

Trial acceptance: initial build coverage and cost; resume after interruption; one code change detected and updated; branch/worktree change detected; stale entries not silently trusted. No percentage of model confidence proves code understanding. Index build or bulk source transmission must stay within the user's chosen scope.

Upstream: <https://github.com/aoci-spec/aoci-code>. License: FSL-1.1-MIT; preserve release licensing. Archive checksum verification does not authenticate the checksum publisher; report the verification level actually completed.
