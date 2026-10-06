# Approval gates

M2.11 connects portable human approval artifacts to editorial policy.

`approval_gate(approval)` accepts only when the approval fingerprint matches the exact Proposal and the recorded decision is `approved`. A rejection or any post-review proposal change fails closed.

`all_gates(...)` composes independent gates with AND semantics. Gates run in order and the first rejection stops evaluation. This allows a project to express policies such as:

`all_gates(puzzle_solver_gate, approval_gate(editor_approval))`

The Puzzle Designer proposal must then pass deterministic solver/softlock qualification and match an explicit human approval before an `apply=True` editorial stage may progress.

Policy remains outside providers and authoring roles. AI proposes; deterministic checks qualify; humans approve; the pipeline enforces.
