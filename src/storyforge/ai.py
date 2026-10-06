from copy import deepcopy
from dataclasses import dataclass
from typing import Protocol


class ProposalError(ValueError):
    pass


@dataclass(frozen=True)
class Proposal:
    role: str
    summary: str
    operations: tuple[dict, ...]


class Provider(Protocol):
    def propose(self, *, role: str, story: dict, instruction: str) -> Proposal:
        ...


def validate_proposal(proposal: Proposal) -> None:
    if not proposal.role.strip():
        raise ProposalError("proposal role must not be empty")
    if not proposal.summary.strip():
        raise ProposalError("proposal summary must not be empty")
    for operation in proposal.operations:
        if not isinstance(operation, dict) or set(operation) != {"op", "path", "value"}:
            raise ProposalError(f"invalid proposal operation: {operation!r}")
        if operation["op"] not in {"add", "replace"}:
            raise ProposalError(f"unsupported proposal operation: {operation['op']!r}")
        path = operation["path"]
        if not isinstance(path, list) or not path or not all(isinstance(p, str) for p in path):
            raise ProposalError(f"invalid proposal path: {path!r}")


def apply_proposal(story: dict, proposal: Proposal) -> dict:
    validate_proposal(proposal)
    result = deepcopy(story)
    for operation in proposal.operations:
        target = result
        path = operation["path"]
        for key in path[:-1]:
            if key not in target or not isinstance(target[key], dict):
                raise ProposalError(f"proposal path does not exist: {path!r}")
            target = target[key]
        key = path[-1]
        if operation["op"] == "replace" and key not in target:
            raise ProposalError(f"cannot replace missing path: {path!r}")
        target[key] = deepcopy(operation["value"])
    return result
