# Architecture

StoryForge is an AI-assisted toolchain for narrative games. AI produces structured source material; it is not authoritative over game state.

The deterministic core loads StoryForge IR, validates it, applies deterministic analysis/transforms, and exports it to target engines/runtimes. AI providers, RetroAsset and game engines are adapters around that core. A valid project must remain buildable without an AI API key.

Initial profiles: visual-novel, point-and-click, text-adventure.
