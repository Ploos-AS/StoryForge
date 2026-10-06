# Game Designer

The Game Designer role reviews pacing, choice structure, progression, and player agency while keeping gameplay state in deterministic StoryForge IR.

M2.5 also adds provider-independent design metrics. StoryForge measures scene count, ending count, total choices, branching scenes, average choices per scene, and structural shortest distances to reachable endings. These values are evidence for review, not quality scores: more choices or branches are not automatically better.

The current ending-distance metric is structural and deliberately does not replace the state-aware solver. Puzzle correctness and softlock detection remain the responsibility of deterministic solver/analysis qualification.

Game Designer proposals remain reviewable and are never automatically applied.
