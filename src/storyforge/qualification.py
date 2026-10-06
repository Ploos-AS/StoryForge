from dataclasses import dataclass

from .ai import Proposal, apply_proposal
from .analysis import dead_states
from .limits import DEFAULT_MAX_STATES, StateSpaceLimitError
from .solver import solve
from .validator import validate_story


@dataclass(frozen=True)
class Qualification:
    accepted: bool
    errors: tuple[str, ...]
    solved_endings: tuple[str, ...]
    dead_states: int


def qualify_puzzle_proposal(
    story: dict, proposal: Proposal, max_states: int = DEFAULT_MAX_STATES
) -> Qualification:
    candidate = apply_proposal(story, proposal)
    errors = tuple(validate_story(candidate))
    if errors:
        return Qualification(False, errors, (), 0)

    try:
        solutions = solve(candidate, max_states=max_states)
        dead = dead_states(candidate, max_states=max_states)
    except StateSpaceLimitError as exc:
        return Qualification(False, (str(exc),), (), 0)

    solved = tuple(sorted(solutions))
    expected = set(candidate.get("endings", {}))
    missing = sorted(expected - set(solved))
    qualification_errors = []
    if missing:
        qualification_errors.append(
            "unreachable endings: " + ", ".join(missing)
        )
    if dead:
        qualification_errors.append(
            f"reachable dead/softlocked states: {len(dead)}"
        )

    return Qualification(
        not qualification_errors,
        tuple(qualification_errors),
        solved,
        len(dead),
    )
