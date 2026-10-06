# Restoring editorial runs

M2.14 closes the persistence loop by reconstructing a typed `EditorialResult` from `storyforge-editorial-run` version 1 JSON.

`restore_editorial_result` validates the run format/version, candidate story, halted state, every stage, apply status, gate evidence, and every Proposal fingerprint. It reconstructs `Proposal`, `GateResult`, `StageResult`, and `EditorialResult` objects.

The restored result can be passed directly to `resume_editorial_pipeline`. Earlier provider calls are therefore not replayed after a process restart or artifact transfer.

This establishes the core boundary required for CI artifact, disk, CLI, or future PWA workflows:

run -> serialize -> process exits -> load -> verify -> restore -> resume.
