from dataclasses import dataclass
from typing import Protocol

from .ai import Proposal, ProposalError, validate_proposal


@dataclass(frozen=True)
class AuthoringRequest:
    role: str
    instruction: str
    context: dict
    constraints: tuple[str, ...]


class AuthoringProvider(Protocol):
    def generate(self, request: AuthoringRequest) -> Proposal:
        ...


WRITER_CONSTRAINTS = (
    "Return only explicit add/replace proposal operations.",
    "Preserve existing machine IDs unless the instruction explicitly requires a new object.",
    "Do not invent runtime state outside the StoryForge IR.",
    "Keep deterministic gameplay logic in structured IR, not prose.",
)


def writer_request(story: dict, instruction: str) -> AuthoringRequest:
    if not instruction.strip():
        raise ProposalError("writer instruction must not be empty")
    return AuthoringRequest(
        role="writer",
        instruction=instruction,
        context=story,
        constraints=WRITER_CONSTRAINTS,
    )


def propose_with_writer(provider: AuthoringProvider, story: dict, instruction: str) -> Proposal:
    proposal = provider.generate(writer_request(story, instruction))
    if proposal.role != "writer":
        raise ProposalError(f"writer provider returned role {proposal.role!r}")
    validate_proposal(proposal)
    return proposal
