# StoryForge IR v0

IR v0 deliberately establishes a small stable core before puzzles, conditions, effects and asset manifests.

Required root keys are `storyforge: "0"`, `start`, `scenes`, and `endings`. Core named collections are `characters`, `locations`, `items`, and `variables`.

A scene contains prose in `text` and choices. Each choice contains `text` and exactly one transition: `goto` to another scene or `ending` to a declared ending.

The IR is engine-, implementation-language- and AI-provider-independent. YAML is the canonical human-authored representation for M0.
