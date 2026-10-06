from dataclasses import dataclass

from .ai import Proposal, apply_proposal
from .authoring import AuthoringProvider, AuthoringRole


@dataclass(frozen=True)
class EditorialStage:
    name: str
    role: AuthoringRole
    instruction: str
    apply: bool = False


@dataclass(frozen=True)
class StageResult:
    stage: str
    proposal: Proposal
    applied: bool


@dataclass(frozen=True)
class EditorialResult:
    story: dict
    stages: tuple[StageResult, ...]


def run_editorial_pipeline(
    story: dict,
    stages: list[EditorialStage],
    providers: dict[str, AuthoringProvider],
) -> EditorialResult:
    current = story
    results = []
    for stage in stages:
        if stage.role.name not in providers:
            raise ValueError(f"no provider configured for role {stage.role.name!r}")
        proposal = stage.role.propose(
            providers[stage.role.name], current, stage.instruction
        )
        if stage.apply:
            current = apply_proposal(current, proposal)
        results.append(StageResult(stage.name, proposal, stage.apply))
    return EditorialResult(current, tuple(results))
