# State-space limits

StoryForge explores deterministic state graphs for solving and dead-state analysis. Numeric counters or relationship attributes can create an unbounded graph when a loop changes state on every pass.

M1.6 therefore limits exploration to 10,000 distinct `(scene, state)` nodes by default. `solve()` and `build_state_graph()` raise `StateSpaceLimitError` when the bound is reached. The CLI reports this as `LIMIT` with exit code 4 instead of hanging.

Use `storyforge solve STORY --max-states N` or `storyforge analyze STORY --max-states N` to tune the bound for larger projects. Reaching the limit means analysis is inconclusive, not that the story is invalid or unsolvable.
