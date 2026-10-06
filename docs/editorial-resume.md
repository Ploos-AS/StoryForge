# Resuming editorial pipelines

`resume_editorial_pipeline` continues an existing `EditorialResult` from the first stage that has not already produced a result.

Completed stages are never replayed. This matters for AI providers: resuming a saved workflow must not silently regenerate earlier proposals or consume a second model response for work that was already reviewed.

Before continuation, StoryForge checks that every completed stage name matches the corresponding prefix of the supplied pipeline definition. A mismatch fails instead of attaching old review history to a different workflow.

The saved candidate story becomes the starting story for the remaining stages. Newly completed results are appended to the existing stage history.

Persisted JSON loading and reconstruction of a full `EditorialResult` remain separate concerns; M2.13 defines the core no-replay resume semantics that CLI/PWA orchestration can build on.
