# OpenAI-compatible provider

M2.17 adds the first concrete StoryForge authoring provider adapter.

`OpenAICompatibleProvider` converts an `AuthoringRequest` into a chat-completions-shaped JSON request and requires the model response to contain only a JSON StoryForge Proposal: `role`, `summary`, and `operations`.

The adapter does not own HTTP. A transport callable is injected, keeping network concerns separate and making the provider contract deterministic in tests. Authentication is an optional bearer token supplied at runtime; provider configuration remains responsible for naming the environment variable, not storing the secret.

Returned data is parsed into the same `Proposal` type used by every authoring role and passes normal proposal validation before it can reach editorial gates.

This is an interoperability adapter, not a dependency on a particular vendor SDK. A compatible local or remote endpoint may implement the same request/response surface.
