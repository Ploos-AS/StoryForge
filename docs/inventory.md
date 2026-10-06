# Inventory

StoryForge IR v0 treats inventory as authoritative deterministic state. Declared `items` define valid item identifiers; `inventory` defines items held at game start.

Choices may require `has_item` or `lacks_item`. Effects may `take_item` or `drop_item`. Inventory is normalized to a sorted immutable tuple internally so `(scene, state)` remains hashable for the solver and dead-state analysis.

This layer deliberately models ownership, not UI verbs. Higher-level adventure actions such as take, use, give and combine can compile into these deterministic primitives while remaining analyzable.
