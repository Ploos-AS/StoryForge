# Writer role

The Writer is the first StoryForge AI authoring role. It converts a human instruction plus the current story IR into a provider-neutral `AuthoringRequest`.

The request carries four explicit fields: role, instruction, story context, and deterministic authoring constraints. A provider returns a normal StoryForge `Proposal`; the Writer boundary verifies that the returned role is correct and that every patch operation satisfies the M2.0 proposal contract.

The Writer is intentionally not a model adapter. OpenAI, local/Ollama-compatible models, or other providers can implement the same `generate(request)` protocol. This keeps prompts and transport concerns outside the deterministic StoryForge core.

M2.1 does not automatically apply proposals. Review and explicit application remain separate steps.
