# Provider configuration

`storyforge-providers` version 1 is the provider-neutral configuration boundary for AI-backed authoring.

A configuration contains named provider definitions and a separate role-to-provider mapping. This allows different roles to use different local or remote models without changing StoryForge's authoring or editorial pipeline.

Example:

```yaml
format: storyforge-providers
version: 1
providers:
  writer-local:
    kind: ollama-compatible
    model: writer-model
    endpoint: http://localhost:11434
  review-cloud:
    kind: openai-compatible
    model: review-model
    api_key_env: REVIEW_API_KEY
roles:
  writer: writer-local
  playtester: review-cloud
```

Secrets are never stored inline. The fields `api_key`, `token`, `secret`, and `password` are rejected. `api_key_env` names an environment variable whose value can be resolved by a future provider adapter at runtime.

M2.16 defines and validates configuration only. It deliberately does not implement network clients or assume a specific vendor API.
