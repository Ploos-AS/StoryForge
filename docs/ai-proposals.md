# AI proposals

StoryForge treats generative AI as an authoring assistant, never as authoritative runtime state.

A provider implements a small provider-neutral interface and returns a `Proposal` containing a role, human-readable summary, and explicit patch operations. M2.0 initially permits only `add` and `replace`; deletion is intentionally excluded until review semantics are designed.

Applying a proposal is a separate explicit operation. It deep-copies the story, validates every patch operation, and returns the candidate story without mutating the source IR. Normal StoryForge schema and semantic validation can then qualify the candidate before it is accepted.

This boundary is intended for future writer, dialogue editor, puzzle designer, continuity editor, game designer, asset-spec generator, and AI playtester providers. Provider adapters may use cloud or local models without changing the deterministic StoryForge core.
