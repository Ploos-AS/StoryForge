# Puzzle Designer

Puzzle Designer is an AI authoring role whose output is treated as an untrusted candidate until the deterministic StoryForge core qualifies it.

The role requires puzzle state, requirements, effects, inventory interactions, and progression to remain structured IR. After a Proposal is applied to a copy of the story, StoryForge runs normal semantic validation, the solver, and dead-state analysis.

A candidate is accepted only when validation succeeds, every declared ending remains solver-reachable, and no reachable dead-end or softlocked state is found within the configured state-space limit. Hitting the state-space limit is inconclusive and therefore fails qualification rather than silently accepting the proposal.

This makes AI creativity subordinate to mechanically testable game logic.
