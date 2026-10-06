# Headless JSON runtime

M1.12 adds a transport-independent facade around the deterministic StoryForge runtime.

`HeadlessRuntime.snapshot()` returns only JSON-compatible values. While playing it exposes the current scene text and currently available actions with stable IDs, display text, and authored command affordances. When an ending is reached it returns an ending object and no actions.

`HeadlessRuntime.execute(choice_id)` executes a currently available action by stable ID and returns the next snapshot. Invalid or unavailable IDs return a structured error rather than mutating state.

The contract deliberately contains no HTTP, WebSocket, framework, persistence, or authentication assumptions. Those belong in adapters around this core. This makes the same runtime suitable for a PWA, web service, native desktop client, automated playtester, retro client, or an AI interpreter.
