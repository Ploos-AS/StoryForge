# Editorial pipeline configuration

M2.19 defines `storyforge-pipeline` version 1, a serializable definition of the editorial stages that a CLI or automation runner can execute.

Example:

```yaml
format: storyforge-pipeline
version: 1
stages:
  - name: draft
    role: writer
    instruction: Improve the opening while preserving deterministic logic.
    apply: true
  - name: continuity
    role: continuity-editor
    instruction: Check the revised story against established facts.
    apply: false
```

Role names are resolved through a closed registry of StoryForge's built-in authoring roles. Unknown roles, duplicate stage names, empty instructions, non-boolean apply values, and unknown stage fields fail closed.

Version 1 intentionally does not serialize Python gate callables. Gate policy needs its own declarative contract so that human approval and deterministic qualification can be reconstructed safely across process boundaries.

This pipeline format, together with `storyforge-providers`, gives a future `storyforge run` command reproducible inputs instead of hard-coded CLI behavior.
