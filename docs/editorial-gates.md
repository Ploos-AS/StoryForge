# Editorial gates

Editorial stages may attach an explicit qualification gate. A gate receives the current story and the validated Proposal and returns a `GateResult`.

Gates are fail-closed. If a gate rejects a proposal, the proposal and rejection reason remain in the pipeline result as review evidence, the candidate is not applied, later stages are not run, and the pipeline reports `halted=True`.

M2.9 includes `puzzle_solver_gate`, which delegates to the existing deterministic Puzzle Designer qualification. A puzzle proposal therefore must pass semantic validation, ending reachability, and dead-state/softlock analysis before an applied stage can modify the working candidate.

An `apply=True` stage with a gate still requires both conditions: explicit application policy and successful qualification. Gates do not make AI authoritative; they restrict when AI proposals are allowed to progress.
