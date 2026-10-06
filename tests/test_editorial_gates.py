from storyforge.ai import Proposal
from storyforge.authoring import PUZZLE_DESIGNER
from storyforge.editorial import EditorialStage, GateResult, run_editorial_pipeline
from storyforge.gates import puzzle_solver_gate


BASE = {
    "storyforge": "0",
    "start": "start",
    "scenes": {
        "start": {
            "text": "Door.",
            "choices": [{"id": "finish", "text": "Finish", "ending": "done"}],
        }
    },
    "endings": {"done": {"text": "Done."}},
}


class Provider:
    def __init__(self, proposal):
        self.proposal = proposal

    def generate(self, request):
        return self.proposal


def test_rejected_gate_halts_without_applying():
    proposal = Proposal(
        role="puzzle-designer",
        summary="Add impossible ending",
        operations=(
            {"op": "add", "path": ["endings", "impossible"], "value": {"text": "No."}},
        ),
    )
    result = run_editorial_pipeline(
        BASE,
        [EditorialStage("puzzle", PUZZLE_DESIGNER, "Add ending", True, puzzle_solver_gate)],
        {"puzzle-designer": Provider(proposal)},
    )
    assert result.halted
    assert not result.stages[0].applied
    assert result.stages[0].gate is not None
    assert not result.stages[0].gate.accepted
    assert "impossible" not in result.story["endings"]


def test_accepted_gate_allows_apply():
    proposal = Proposal(
        role="puzzle-designer",
        summary="Improve room prose",
        operations=(
            {"op": "replace", "path": ["scenes", "start", "text"], "value": "Heavy door."},
        ),
    )
    result = run_editorial_pipeline(
        BASE,
        [EditorialStage("puzzle", PUZZLE_DESIGNER, "Improve", True, puzzle_solver_gate)],
        {"puzzle-designer": Provider(proposal)},
    )
    assert not result.halted
    assert result.stages[0].applied
    assert result.stages[0].gate == GateResult(True)
    assert result.story["scenes"]["start"]["text"] == "Heavy door."
