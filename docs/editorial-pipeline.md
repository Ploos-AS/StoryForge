# Editorial pipeline

StoryForge can compose specialized authoring roles into an explicit editorial pipeline without introducing an autonomous agent loop.

Each `EditorialStage` has a name, an `AuthoringRole`, an instruction, and an explicit `apply` flag. The configured provider produces a normal reviewable Proposal. When `apply` is false, the proposal is recorded but the working story is unchanged. When it is true, the proposal is applied copy-on-write and the resulting candidate becomes context for later stages.

Providers are selected by role name, so different roles may use different cloud or local models. Missing providers fail explicitly.

The pipeline does not bypass role validation, proposal validation, solver qualification, continuity checks, or human review policy. It is orchestration, not a second authority over StoryForge IR.

A future project-level workflow can use this primitive to arrange stages such as Writer, Dialogue Editor, Puzzle Designer, Continuity Editor, Game Designer, Asset Spec Generator, and Playtester while choosing which boundaries require approval or deterministic qualification.
