# Save/load format

M1.13 defines a versioned, JSON-compatible save format for deterministic StoryForge sessions.

A save records the current scene and ending plus public representations of global variables, player inventory, item ownership, and character attributes. Internal canonical tuples and implementation details are reconstructed on load rather than exposed as part of the file format.

The envelope is identified by `format: storyforge-save` and currently uses `version: 1`. Unknown formats, versions, scenes, and endings are rejected.

Story compatibility identity is intentionally not inferred from the human-readable title. A future IR metadata milestone should define a stable story ID/version or content fingerprint before cross-story save validation is added.
