# Adventure actions

StoryForge actions are author-facing semantic sugar that lower to the deterministic IR primitives before runtime evaluation, solving, or dead-state analysis.

Supported in M1.3:

- `take`: requires the item to be absent, then adds it to inventory.
- `drop`: requires the item to be held, then removes it.
- `use`: requires the item to be held and applies declared deterministic effects.
- `combine`: requires two held items, consumes both, and creates a third item.

This design keeps one authoritative rules engine. Exporters, solvers and future parsers do not need independent implementations of puzzle semantics.

`give` is intentionally deferred until StoryForge models item ownership by characters. Treating give as drop would lose important narrative state.
