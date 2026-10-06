# StoryForge IR v0

IR v0 deliberately establishes a small stable core before puzzles, conditions, effects and asset manifests.

Required root keys are `storyforge: "0"`, `start`, `scenes`, and `endings`. Core named collections are `characters`, `locations`, `items`, and `variables`.

A scene contains prose in `text` and choices. Each choice contains `text` and exactly one transition: `goto` to another scene or `ending` to a declared ending.

The IR is engine-, implementation-language- and AI-provider-independent. YAML is the canonical human-authored representation for M0.

## State, conditions and effects

`variables` defines the initial authoritative game state. Values may be
booleans, numbers or strings.

Choices may contain `requires`, an array of equality conditions. A choice is
available only when all requirements match current state.

Choices may also contain `effects`. M0.2 defines three deterministic
operations: `set`, `increment`, and `decrement`. Effects may only reference
declared variables.

This intentionally small state language is solver-friendly and does not embed
arbitrary code in the IR.
