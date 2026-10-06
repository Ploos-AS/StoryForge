# Persisted editorial runs

StoryForge editorial results can be serialized as `storyforge-editorial-run` version 1 JSON.

A run records the current candidate story, whether the pipeline halted, each completed stage, its Proposal, whether it was applied, and any gate result. Every stored Proposal includes the same canonical SHA-256 fingerprint used by human approvals.

`load_editorial_run` validates the format/version, basic structure, reconstructs each Proposal, and recomputes its fingerprint. A modified proposal therefore fails loading instead of silently inheriting prior review evidence.

M2.12 deliberately persists completed run state without yet implementing automatic continuation. This gives CLI, CI artifacts, or a future PWA a stable pause/export/import boundary. Resume semantics can be added on top while still requiring fresh gate/approval validation for whatever stage is about to execute.
