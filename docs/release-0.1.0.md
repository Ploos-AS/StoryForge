# StoryForge 0.1.0 release candidate

Release 0.1.0 is the first integrated StoryForge toolchain candidate.

Before creating `v0.1.0`:

- CI passes on the release commit.
- OCI build and runtime qualification pass.
- Release-contract workflow passes.
- `storyforge --version` reports `0.1.0`.
- Lighthouse validates, solves and analyzes in the installed OCI image.
- No API keys, generated stories, proprietary assets, or provider credentials are stored in the image.
- Human-approval workflows preserve proposal fingerprints and resume without replaying the blocked provider call.
- The Git tag is exactly `v0.1.0`.

The tag workflow then publishes matching multi-architecture OCI version tags through the existing OCI workflow.

0.1.0 is intentionally pre-1.0. The IR and persisted editorial formats are versioned, but compatibility policy can still evolve while StoryForge gains additional exporters, genre extensions, stronger artifact provenance, and production provider hardening.
