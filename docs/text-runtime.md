# Deterministic text runtime

M1.8 adds a small runtime directly on StoryForge IR. `Session` owns the current scene and canonical deterministic state, exposes only currently available choices, applies the same lowered action/effect semantics as the solver, and reports endings.

Run a story interactively with `storyforge play STORY`.

The runtime intentionally accepts structured choice selection rather than free-form AI output. A future natural-language or LLM parser may map player text to a choice/action, but it will not own or mutate authoritative game state. This keeps terminal, web, PWA, and AI-assisted front ends consistent with validation and solving.
