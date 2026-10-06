# Editorial run CLI

M2.21 connects the serialized StoryForge inputs to an executable editorial workflow.

```
storyforge run story.yaml \
  --pipeline pipeline.yaml \
  --providers providers.yaml \
  -o run.json
```

The command validates the story, loads `storyforge-pipeline` and `storyforge-providers`, resolves configured role providers and runtime secrets, executes the editorial pipeline, and persists a `storyforge-editorial-run` artifact.

Exit status is 0 when all configured stages finish and 3 when a gate halts the workflow. A halted run is still written so the exact proposal and gate evidence remain available for review.

The default network transport is a small Python standard-library JSON POST implementation. Provider adapters remain separate from HTTP and can still be tested with injected transports.

A `human-approval` gate therefore gives a practical pause boundary: run -> proposal -> persisted artifact -> review. Applying the approved halted proposal and continuing without replay is the next resume-layer milestone.
