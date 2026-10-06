from dataclasses import dataclass
from typing import Callable

from .ai import Proposal, apply_proposal
from .authoring import AuthoringProvider, AuthoringRole


@dataclass(frozen=True)
class GateResult:
    accepted: bool
    reason: str = ""


Gate = Callable[[dict, Proposal], GateResult]


@dataclass(frozen=True)
class EditorialStage:
    name: str
    role: AuthoringRole
    instruction: str
    apply: bool = False
    gate: Gate | None = None


@dataclass(frozen=True)
class StageResult:
    stage: str
    proposal: Proposal
    applied: bool
    gate: GateResult | None = None


@dataclass(frozen=True)
class EditorialResult:
    story: dict
    stages: tuple[StageResult, ...]
    halted: bool = False


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

        gate_result = stage.gate(current, proposal) if stage.gate else None
        if gate_result is not None and not gate_result.accepted:
            results.append(StageResult(stage.name, proposal, False, gate_result))
            return EditorialResult(current, tuple(results), halted=True)

        if stage.apply:
            current = apply_proposal(current, proposal)
        results.append(StageResult(stage.name, proposal, stage.apply, gate_result))

    return EditorialResult(current, tuple(results), halted=False)
