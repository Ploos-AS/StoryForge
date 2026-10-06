from .ai import Proposal
from .approval import proposal_fingerprint
from .editorial import EditorialResult, GateResult, StageResult


RUN_FORMAT = "storyforge-editorial-run"
RUN_VERSION = 1


class EditorialRunError(ValueError):
    pass


def dump_editorial_result(result: EditorialResult) -> dict:
    return {
        "format": RUN_FORMAT,
        "version": RUN_VERSION,
        "halted": result.halted,
        "story": result.story,
        "stages": [
            {
                "stage": item.stage,
                "proposal": {
                    "role": item.proposal.role,
                    "summary": item.proposal.summary,
                    "operations": list(item.proposal.operations),
                    "fingerprint": proposal_fingerprint(item.proposal),
                },
                "applied": item.applied,
                "gate": (
                    {"accepted": item.gate.accepted, "reason": item.gate.reason}
                    if item.gate is not None
                    else None
                ),
            }
            for item in result.stages
        ],
    }


def restore_editorial_result(data: dict) -> EditorialResult:
    if data.get("format") != RUN_FORMAT:
        raise EditorialRunError("unsupported editorial run format")
    if data.get("version") != RUN_VERSION:
        raise EditorialRunError("unsupported editorial run version")
    if not isinstance(data.get("story"), dict):
        raise EditorialRunError("editorial run story must be an object")
    if not isinstance(data.get("stages"), list):
        raise EditorialRunError("editorial run stages must be a list")
    if not isinstance(data.get("halted"), bool):
        raise EditorialRunError("editorial run halted must be boolean")

    stages = []
    for stage in data["stages"]:
        if not isinstance(stage, dict):
            raise EditorialRunError("editorial run stage must be an object")
        proposal_data = stage.get("proposal")
        if not isinstance(proposal_data, dict):
            raise EditorialRunError("editorial run proposal must be an object")
        try:
            proposal = Proposal(
                role=proposal_data["role"],
                summary=proposal_data["summary"],
                operations=tuple(proposal_data["operations"]),
            )
        except (KeyError, TypeError) as exc:
            raise EditorialRunError("invalid editorial run proposal") from exc
        if proposal_data.get("fingerprint") != proposal_fingerprint(proposal):
            raise EditorialRunError("editorial run proposal fingerprint mismatch")

        gate_data = stage.get("gate")
        if gate_data is None:
            gate = None
        elif (
            isinstance(gate_data, dict)
            and isinstance(gate_data.get("accepted"), bool)
            and isinstance(gate_data.get("reason"), str)
        ):
            gate = GateResult(gate_data["accepted"], gate_data["reason"])
        else:
            raise EditorialRunError("invalid editorial run gate")

        if not isinstance(stage.get("stage"), str):
            raise EditorialRunError("editorial run stage name must be a string")
        if not isinstance(stage.get("applied"), bool):
            raise EditorialRunError("editorial run applied must be boolean")
        stages.append(StageResult(stage["stage"], proposal, stage["applied"], gate))

    return EditorialResult(data["story"], tuple(stages), data["halted"])


def load_editorial_run(data: dict) -> dict:
    restore_editorial_result(data)
    return data
