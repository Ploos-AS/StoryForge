import pytest

from storyforge.ai import Proposal
from storyforge.authoring import DIALOGUE_EDITOR, WRITER
from storyforge.editorial import (
    EditorialStage,
    resume_editorial_pipeline,
    run_editorial_pipeline,
)


class CountingProvider:
    def __init__(self):
        self.calls = []

    def generate(self, request):
        self.calls.append(request.role)
        value = "Draft" if request.role == "writer" else "Polished"
        return Proposal(
            role=request.role,
            summary=value,
            operations=(
                {"op": "replace", "path": ["scenes", "start", "text"], "value": value},
            ),
        )


def pipeline():
    return [
        EditorialStage("draft", WRITER, "Draft", apply=True),
        EditorialStage("polish", DIALOGUE_EDITOR, "Polish", apply=True),
    ]


def test_resume_runs_only_remaining_stages():
    provider = CountingProvider()
    story = {"scenes": {"start": {"text": "Original"}}}
    first = run_editorial_pipeline(
        story, pipeline()[:1], {"writer": provider}
    )
    assert provider.calls == ["writer"]

    resumed = resume_editorial_pipeline(
        first,
        pipeline(),
        {"dialogue-editor": provider},
    )
    assert provider.calls == ["writer", "dialogue-editor"]
    assert [item.stage for item in resumed.stages] == ["draft", "polish"]
    assert resumed.story["scenes"]["start"]["text"] == "Polished"
    assert not resumed.halted


def test_resume_rejects_changed_pipeline_prefix():
    provider = CountingProvider()
    story = {"scenes": {"start": {"text": "Original"}}}
    first = run_editorial_pipeline(story, pipeline()[:1], {"writer": provider})
    changed = [
        EditorialStage("different-name", WRITER, "Draft", apply=True),
        pipeline()[1],
    ]
    with pytest.raises(ValueError, match="stage mismatch"):
        resume_editorial_pipeline(first, changed, {"dialogue-editor": provider})
