# Character state and relationships

M1.5 adds generic deterministic attributes to characters. A story may initialize attributes such as `met`, `trust`, `hostile`, `romance`, `route`, or domain-specific values without StoryForge hardcoding each narrative concept.

Choice requirements can compare a character attribute for equality. Effects can set, increment, or decrement attributes. State is normalized into sorted tuples, so character relationships remain part of the same hashable state explored by the solver and dead-state analyzer.

`met` is a convention rather than a special runtime primitive. This keeps the IR useful across visual novels, point-and-click adventures, text adventures, and future narrative RPG profiles.
