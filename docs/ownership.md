# Character ownership

M1.4 extends deterministic state with item ownership by characters. Player-held items remain in `_inventory`; NPC-held items are stored canonically as item-to-character ownership pairs.

The `give` action requires the player to hold an item, removes it from player inventory, and assigns it to the target character. `owned_by` requirements let later choices depend on that transfer. Taking an item transfers it back to the player and clears character ownership.

Because ownership is canonical and hashable, the existing solver and dead-state analysis explore ownership puzzles without a separate rules engine.
