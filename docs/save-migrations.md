# Save migrations

M1.15 adds explicit, declarative migration of bound StoryForge saves between story versions.

A migration is an ordered version edge with `from`, `to`, and deterministic operations. Supported operations initially cover scene and ending renames, variable rename/set/drop, item renames, and character renames. Item ownership and character ownership references are updated when relevant.

Migrations contain data only: no Python snippets, eval, callbacks, or arbitrary scripting. Multiple migration edges can be chained, for example `1.0.0 -> 1.1.0 -> 1.2.0`. Missing paths, cycles, duplicate source versions, cross-story migration, invalid destinations, and destructive rename collisions fail explicitly.

Migration transforms a copy of the save JSON. The result is then loaded through the normal save loader, so current story/version and scene/ending validation remain authoritative.
