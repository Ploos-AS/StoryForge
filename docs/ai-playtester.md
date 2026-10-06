# AI Playtester

The Playtester is an adversarial AI review role, not an alternative game runtime.

A model may suggest unusual strategies or action-ID sequences and may report suspected usability, narrative, pacing, or gameplay problems. Runtime snapshots and currently available action IDs are authoritative; the model must not invent hidden state, unavailable actions, or successful outcomes.

`execute_plan(story, action_ids)` runs a proposed plan through the existing deterministic `HeadlessRuntime`. It records snapshots before and after every attempted action and stops on an ending or runtime error. The resulting trace is reproducible evidence that can be attached to a playtest finding.

This creates a useful division of labour: AI searches creatively for suspicious behaviour; StoryForge determines what actually happens.
