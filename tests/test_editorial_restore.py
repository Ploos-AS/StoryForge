import json

from storyforge.ai import Proposal
from storyforge.authoring import DIALOGUE_EDITOR, WRITER
from storyforge.editorial import (
    EditorialResult,
    EditorialStage,
    GateResult,
    StageResult,
    resume_editorial_pipeline,
)
from storyforge.editorial_run import dump_editorial_result, restore_editorial_result


class Provider:
    def __init__(self):
        self.calls = 0

    def generate(self, request):
        self.calls += 1
        return Proposal(
            role=request.role,
            summary="Polish",
            operations=(
                {"op": "replace", "path": ["scenes", "start", "text"], "value": "Polished"},
            ),
        )


def test_json_restore_reconstructs_typed_result():
    proposal = Proposal("writer", "Draft", ())
    original = EditorialResult(
        {"scenes": {"start": {"text": "Draft"}}},
        (StageResult("draft", proposal, False, GateResult(True, "checked")),),
        halted=True,
    )
    data = json.loads(json.dumps(dump_editorial_result(original)))
    restored = restore_editorial_result(data)
    assert isinstance(restored, EditorialResult)
    assert isinstance(restored.stages[0], StageResult)
    assert isinstance(restored.stages[0].proposal, Proposal)
    assert restored.stages[0].gate == GateResult(True, "checked")
    assert restored.halted


def test_restored_result_can_resume_without_replay():
    proposal = Proposal(
        "writer",
        "Draft",
        ({"op": "replace", "path": ["scenes", "start", "text"], "value": "Draft"},),
    )
    saved = EditorialResult(
        {"scenes": {"start": {"text": "Draft"}}},
        (StageResult("draft", proposal, True, None),),
        halted=False,
    )
    restored = restore_editorial_result(
        json.loads(json.dumps(dump_editorial_result(saved)))
    )
    provider = Provider()
    pipeline = [
        EditorialStage("draft", WRITER, "Draft", apply=True),
        EditorialStage("polish", DIALOGUE_EDITOR, "Polish", apply=True),
    ]
    result = resume_editorial_pipeline(
        restored, pipeline, {"dialogue-editor": provider}
    )
    assert provider.calls == 1
    assert result.story["scenes"]["start"]["text"] == "Polished"
    assert [stage.stage for stage in result.stages] == ["draft", "polish"]
