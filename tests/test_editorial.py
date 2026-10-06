from storyforge.ai import Proposal
from storyforge.authoring import DIALOGUE_EDITOR, WRITER
from storyforge.editorial import EditorialStage, run_editorial_pipeline


class Provider:
    def generate(self, request):
        if request.role == "writer":
            return Proposal(
                role="writer",
                summary="Draft opening",
                operations=(
                    {"op": "replace", "path": ["scenes", "start", "text"], "value": "Draft"},
                ),
            )
        return Proposal(
            role="dialogue-editor",
            summary="Polish opening",
            operations=(
                {"op": "replace", "path": ["scenes", "start", "text"], "value": "Polished"},
            ),
        )


def test_pipeline_only_applies_explicit_stages():
    story = {"scenes": {"start": {"text": "Original", "choices": []}}}
    provider = Provider()
    result = run_editorial_pipeline(
        story,
        [
            EditorialStage("draft", WRITER, "Draft it", apply=False),
            EditorialStage("polish", DIALOGUE_EDITOR, "Polish it", apply=True),
        ],
        {"writer": provider, "dialogue-editor": provider},
    )
    assert story["scenes"]["start"]["text"] == "Original"
    assert result.story["scenes"]["start"]["text"] == "Polished"
    assert [stage.applied for stage in result.stages] == [False, True]


def test_applied_stage_becomes_context_for_next_stage():
    story = {"scenes": {"start": {"text": "Original", "choices": []}}}

    class InspectingProvider(Provider):
        def generate(self, request):
            if request.role == "dialogue-editor":
                assert request.context["scenes"]["start"]["text"] == "Draft"
            return super().generate(request)

    provider = InspectingProvider()
    result = run_editorial_pipeline(
        story,
        [
            EditorialStage("draft", WRITER, "Draft it", apply=True),
            EditorialStage("polish", DIALOGUE_EDITOR, "Polish it", apply=True),
        ],
        {"writer": provider, "dialogue-editor": provider},
    )
    assert result.story["scenes"]["start"]["text"] == "Polished"
