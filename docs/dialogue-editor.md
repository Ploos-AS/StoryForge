# Dialogue Editor role

The Dialogue Editor uses the shared `AuthoringRole` infrastructure introduced in M2.2. Writer and Dialogue Editor now share request construction, provider invocation, role verification, and proposal validation.

Dialogue Editor constraints protect gameplay semantics by default: speaker identity, scene logic, choice IDs, conditions, and effects should remain stable unless the human instruction explicitly asks to change gameplay. Dialogue must remain consistent with known character state and story context, while deterministic state stays in structured IR rather than prose.

Like every StoryForge AI role, Dialogue Editor returns a reviewable Proposal and never applies it automatically.
