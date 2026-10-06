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


def resume_editorial_pipeline(
    previous: EditorialResult,
    stages: list[EditorialStage],
    providers: dict[str, AuthoringProvider],
) -> EditorialResult:
    completed = len(previous.stages)
    if completed > len(stages):
        raise ValueError("previous run has more stages than pipeline definition")

    for index, result in enumerate(previous.stages):
        if result.stage != stages[index].name:
            raise ValueError(
                f"pipeline stage mismatch at {index}: "
                f"{result.stage!r} != {stages[index].name!r}"
            )

    prefix = previous.stages
    current = previous.story
    next_index = completed

    if previous.halted:
        if not previous.stages:
            raise ValueError("halted run has no blocked stage")
        blocked_index = completed - 1
        blocked = previous.stages[-1]
        stage = stages[blocked_index]
        if stage.gate is None:
            raise ValueError("halted stage has no gate")
        gate_result = stage.gate(current, blocked.proposal)
        retried = StageResult(stage.name, blocked.proposal, False, gate_result)
        prefix = previous.stages[:-1] + (retried,)
        if not gate_result.accepted:
            return EditorialResult(current, prefix, halted=True)
        if stage.apply:
            current = apply_proposal(current, blocked.proposal)
            prefix = previous.stages[:-1] + (
                StageResult(stage.name, blocked.proposal, True, gate_result),
            )
        next_index = blocked_index + 1

    continued = run_editorial_pipeline(current, stages[next_index:], providers)
    return EditorialResult(
        continued.story,
        prefix + continued.stages,
        halted=continued.halted,
    )
