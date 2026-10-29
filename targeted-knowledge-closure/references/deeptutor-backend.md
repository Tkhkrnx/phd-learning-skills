# DeepTutor backend

DeepTutor is an independent application, not a Markdown skill. This skill adapts its material-grounded tutoring, prerequisite paths, solving/practice, notebooks, research learning, and durable progress. Actual RAG, immersive audio/video, living books, and app-wide memory require the upstream runtime and matching modules.

## Local integration

The local tool checkout is `C:/Users/peng/Documents/PHR/Intellistream/study_tools/DeepTutor`. Its isolated runtime environment is `.venv`; private runtime data belongs in the sibling `DeepTutor-home`, not in the source checkout or this skill package. The portable alternative is `DEEPTUTOR_HOME` set to a user-selected runtime directory.

Use the installed executable's `--help`, `doctor`, and `module list` to inspect actual capabilities. The normal upstream flow is `deeptutor init --home <runtime-home>` then `deeptutor start --home <runtime-home>`; confirm available flags from installed help before use. Do not start a web service, copy Codex/Claude credentials, choose a paid provider, or upload the vault merely to answer a teaching question.

For requested app use, initialize the provider through the upstream interactive configuration without exposing keys. Configure only the selected knowledge source. Linking an entire vault or enabling write-back requires explicit scope; begin with the relevant exported materials/read-only source where possible. Prefer the existing MinerU installation over duplicating a heavyweight parser. Missing embedding/search/media models must be reported as missing, not bypassed with fabricated results.

## Capability routing

| Need | Route |
| --- | --- |
| Explain a paper section, derive a formula, guide practice | Current agent + inspected source; no backend required |
| Persistent path, exercise bank, errors, resume | Skill session helper + requested Obsidian learning folder |
| Multi-document indexed retrieval | Configured DeepTutor Knowledge module; verify citations against originals |
| Editable chapter/course book | DeepTutor Books module; review generated content and preserve source locators |
| Interactive notebook / immersive reading | DeepTutor Notebook / Reading modules; distinguish app notes from canonical vault notes |
| Audio overview / video lessons | Matching modules, media/model configuration, and requested cost/privacy scope |
| Research assistant / visualization / solve workspace | Installed Research / Visualize / Solve modules or available current tools; report what actually ran |

Keep one owner for each progress record. Export an app session into Obsidian only on request, compare existing notes, and never silently overwrite either copy. Do not advertise an installed module as an end-to-end tested provider workflow.

Source: <https://github.com/HKUDS/DeepTutor> (Apache-2.0). Integration is selective and does not claim parity with the complete application.
