# Provider runtime resolution

M2.18 connects `storyforge-providers` configuration to concrete authoring provider instances.

`build_providers` validates provider kinds and endpoints, resolves any `api_key_env` reference from the runtime environment, and constructs provider adapters. Missing required secrets fail before a provider can be used.

`resolve_role_providers` then maps authoring role names to the configured instances. Multiple roles mapped to the same named provider share that instance.

The first runtime supports `openai-compatible` and `ollama-compatible` kinds through the same injected transport contract. StoryForge still owns no vendor SDK and stores no secret values in project configuration.

This is the final configuration-to-runtime bridge needed before a CLI command can load a story, load provider configuration, build role providers, and execute an editorial pipeline.
