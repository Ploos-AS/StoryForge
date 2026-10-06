from .ai import Proposal
from .editorial import GateResult
from .qualification import qualify_puzzle_proposal


def puzzle_solver_gate(story: dict, proposal: Proposal) -> GateResult:
    result = qualify_puzzle_proposal(story, proposal)
    if result.accepted:
        return GateResult(True)
    return GateResult(False, "; ".join(result.errors))
