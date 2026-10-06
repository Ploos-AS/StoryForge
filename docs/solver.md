# Solver

StoryForge's solver explores the finite `(scene, state)` space using breadth-first search. It only follows choices whose requirements are satisfied and applies the same deterministic effects used by runtime tooling.

For every reachable ending, the solver records the first path found. Because BFS is used, this is a shortest walkthrough in number of choices. The search also reports declared endings for which no valid state path exists.

```sh
storyforge solve examples/lighthouse/story.yaml
```

The solver is intentionally independent of AI. Future AI puzzle generation can therefore be accepted or rejected using reproducible mechanical evidence.

## M1 limitations

IR v0 currently allows numeric increments without bounds. Authors should keep state finite; a future validator will detect or cap unbounded state spaces.
