# Continuity Editor

StoryForge separates continuity into deterministic facts and narrative review.

`continuity_issues(story)` checks machine-provable consistency such as character-state references, item ownership, player/NPC ownership conflicts, inventory references, and scene location references. These checks do not use AI.

The Continuity Editor AI role handles the softer layer: characterization, lore, chronology expressed in prose, tone, and contradictions that cannot be proven from structured state alone. Its constraints treat machine-readable facts as authoritative, forbid silent machine-ID renames, and require uncertainty to be surfaced rather than invented away.

AI proposals remain reviewable and are never automatically applied.
