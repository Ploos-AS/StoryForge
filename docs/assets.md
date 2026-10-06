# Asset specifications

StoryForge describes assets but does not require a particular generator.

The Asset Spec Generator AI role can propose entries under the story's `assets` mapping. Each asset has a stable ID, semantic kind and description, plus optional target and technical constraints. Binary asset data does not belong in StoryForge IR.

`asset_manifest(story)` exports a deterministic, provider-neutral `storyforge-assets` version 1 manifest. External tools can consume this contract to generate, locate, convert, or validate assets.

This allows integrations such as RetroAsset without making StoryForge depend on RetroAsset. A project can instead use hand-drawn art, Blender, conventional asset pipelines, another AI provider, or target-specific converters while retaining the same StoryForge contract.

Target constraints are intentionally separate from semantic description so one conceptual asset can be produced differently for Amiga OCS, C64, web, modern desktop, or future targets.
