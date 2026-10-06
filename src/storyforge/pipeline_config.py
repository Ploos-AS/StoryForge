from dataclasses import dataclass

from .authoring import (
    ASSET_SPEC_GENERATOR,
    CONTINUITY_EDITOR,
    DIALOGUE_EDITOR,
    GAME_DESIGNER,
    PLAYTESTER,
    PUZZLE_DESIGNER,
    WRITER,
)
from .editorial import EditorialStage, GateResult
from .gates import all_gates, puzzle_solver_gate


PIPELINE_FORMAT = "storyforge-pipeline"
PIPELINE_VERSION = 1


class PipelineConfigError(ValueError):
    pass


ROLES = {
    role.name: role
    for role in (
        WRITER,
        DIALOGUE_EDITOR,
        PUZZLE_DESIGNER,
        CONTINUITY_EDITOR,
        GAME_DESIGNER,
        ASSET_SPEC_GENERATOR,
        PLAYTESTER,
    )
}


@dataclass(frozen=True)
class PipelineConfig:
    stages: tuple[EditorialStage, ...]


def approval_required_gate(story, proposal):
    return GateResult(False, "human approval required")


def _load_gate(raw, stage_name):
    if raw is None:
        return None
    names = raw if isinstance(raw, list) else [raw]
    if not names or not all(isinstance(name, str) for name in names):
        raise PipelineConfigError(f"stage {stage_name!r} gate must be a string or non-empty list")
    gates = []
    for name in names:
        if name == "puzzle-solver":
            gates.append(puzzle_solver_gate)
        elif name == "human-approval":
            gates.append(approval_required_gate)
        else:
            raise PipelineConfigError(f"stage {stage_name!r} has unknown gate {name!r}")
    return gates[0] if len(gates) == 1 else all_gates(*gates)


def load_pipeline_config(data: dict) -> PipelineConfig:
    if data.get("format") != PIPELINE_FORMAT:
        raise PipelineConfigError("unsupported pipeline format")
    if data.get("version") != PIPELINE_VERSION:
        raise PipelineConfigError("unsupported pipeline version")
    raw_stages = data.get("stages")
    if not isinstance(raw_stages, list) or not raw_stages:
        raise PipelineConfigError("stages must be a non-empty list")

    stages = []
    names = set()
    for index, raw in enumerate(raw_stages):
        if not isinstance(raw, dict):
            raise PipelineConfigError(f"stage {index} must be an object")
        name = raw.get("name")
        role_name = raw.get("role")
        instruction = raw.get("instruction")
        apply = raw.get("apply", False)
        if not isinstance(name, str) or not name:
            raise PipelineConfigError(f"stage {index} name must be non-empty")
        if name in names:
            raise PipelineConfigError(f"duplicate stage name {name!r}")
        if role_name not in ROLES:
            raise PipelineConfigError(f"stage {name!r} has unknown role {role_name!r}")
        if not isinstance(instruction, str) or not instruction.strip():
            raise PipelineConfigError(f"stage {name!r} instruction must be non-empty")
        if not isinstance(apply, bool):
            raise PipelineConfigError(f"stage {name!r} apply must be boolean")

        gate = _load_gate(raw.get("gate"), name)

        unknown = set(raw) - {"name", "role", "instruction", "apply", "gate"}
        if unknown:
            raise PipelineConfigError(
                f"stage {name!r} has unsupported fields: {', '.join(sorted(unknown))}"
            )

        stages.append(EditorialStage(name, ROLES[role_name], instruction, apply, gate))
        names.add(name)

    return PipelineConfig(tuple(stages))
