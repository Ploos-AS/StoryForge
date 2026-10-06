# Human approval artifacts

StoryForge approvals are portable review records bound to the exact Proposal that was reviewed.

A proposal fingerprint is SHA-256 over a canonical JSON representation of its role, summary, and operations. An approval records that fingerprint, an approved/rejected decision, reviewer identity, and an optional reviewer note.

The serialized `storyforge-approval` version 1 object is ordinary JSON. This allows future CLI, PWA, CI, or other interfaces to exchange approval decisions without making any interface authoritative over StoryForge itself.

If proposal content changes after review, its fingerprint changes and the old approval no longer matches. Approval therefore cannot silently transfer to a modified proposal.

M2.10 records review decisions but does not yet make approval a pipeline gate. That composition is intentionally left explicit for the next milestone.
