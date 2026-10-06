# Dead-state analysis

`storyforge analyze` explores every reachable `(scene, state)` pair and builds a directed state graph. It then works backwards from every state that can directly reach an ending.

Any reachable state outside that reverse-reachable set cannot finish the game:

- `dead-end`: no non-ending transition is available and no ending can be reached.
- `softlock`: transitions remain available, but every continuation is trapped away from all endings.

This is stronger than checking that at least one solution exists. A game may have a valid walkthrough and still contain a branch that permanently destroys the player's ability to finish.

The analysis is deterministic and intended as a CI gate for authored and AI-generated puzzles.
