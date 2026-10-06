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


@dataclass(frozen=True)
class AuthoringRole:
    name: str
    constraints: tuple[str, ...]

    def request(self, story: dict, instruction: str) -> AuthoringRequest:
        if not instruction.strip():
            raise ProposalError(f"{self.name} instruction must not be empty")
        return AuthoringRequest(
            role=self.name,
            instruction=instruction,
            context=story,
            constraints=self.constraints,
        )

    def propose(self, provider: AuthoringProvider, story: dict, instruction: str) -> Proposal:
        proposal = provider.generate(self.request(story, instruction))
        if proposal.role != self.name:
            raise ProposalError(
                f"{self.name} provider returned role {proposal.role!r}"
            )
        validate_proposal(proposal)
        return proposal


WRITER = AuthoringRole(
    name="writer",
    constraints=(
        "Return only explicit add/replace proposal operations.",
        "Preserve existing machine IDs unless the instruction explicitly requires a new object.",
        "Do not invent runtime state outside the StoryForge IR.",
        "Keep deterministic gameplay logic in structured IR, not prose.",
    ),
)

DIALOGUE_EDITOR = AuthoringRole(
    name="dialogue-editor",
    constraints=(
        "Return only explicit add/replace proposal operations.",
        "Preserve speaker identity, scene logic, choice IDs, conditions, and effects.",
        "Change gameplay logic only when the instruction explicitly requests it.",
        "Keep dialogue consistent with character state and established story context.",
        "Do not encode deterministic gameplay state in prose.",
    ),
)

PUZZLE_DESIGNER = AuthoringRole(
    name="puzzle-designer",
    constraints=(
        "Return only explicit add/replace proposal operations.",
        "Express puzzle state, requirements, and effects in deterministic StoryForge IR.",
        "Do not rely on prose or model inference for puzzle correctness.",
        "Preserve at least one reachable ending.",
        "Do not introduce dead ends, softlocks, or inventory deadlocks.",
    ),
)


def writer_request(story: dict, instruction: str) -> AuthoringRequest:
    return WRITER.request(story, instruction)


def propose_with_writer(provider: AuthoringProvider, story: dict, instruction: str) -> Proposal:
    return WRITER.propose(provider, story, instruction)


def dialogue_request(story: dict, instruction: str) -> AuthoringRequest:
    return DIALOGUE_EDITOR.request(story, instruction)


def propose_with_dialogue_editor(
    provider: AuthoringProvider, story: dict, instruction: str
) -> Proposal:
    return DIALOGUE_EDITOR.propose(provider, story, instruction)


def puzzle_request(story: dict, instruction: str) -> AuthoringRequest:
    return PUZZLE_DESIGNER.request(story, instruction)


def propose_with_puzzle_designer(
    provider: AuthoringProvider, story: dict, instruction: str
) -> Proposal:
    return PUZZLE_DESIGNER.propose(provider, story, instruction)
