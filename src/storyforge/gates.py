from collections.abc import Iterable

from .ai import Proposal
from .approval import Approval, approval_matches
from .editorial import Gate, GateResult
from .qualification import qualify_puzzle_proposal


def puzzle_solver_gate(story: dict, proposal: Proposal) -> GateResult:
    result = qualify_puzzle_proposal(story, proposal)
    if result.accepted:
        return GateResult(True)
    return GateResult(False, "; ".join(result.errors))


def approval_gate(approval: Approval) -> Gate:
    def gate(story: dict, proposal: Proposal) -> GateResult:
        if not approval_matches(approval, proposal):
            return GateResult(False, "approval does not match proposal")
        if approval.decision != "approved":
            return GateResult(False, f"proposal is {approval.decision}")
        return GateResult(True)

    return gate


def all_gates(*gates: Gate) -> Gate:
    def combined(story: dict, proposal: Proposal) -> GateResult:
        for gate in gates:
            result = gate(story, proposal)
            if not result.accepted:
                return result
        return GateResult(True)

    return combined
