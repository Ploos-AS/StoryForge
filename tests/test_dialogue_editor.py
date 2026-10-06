import pytest

from storyforge.ai import Proposal, ProposalError
from storyforge.authoring import dialogue_request, propose_with_dialogue_editor


STORY = {
    "characters": {"anna": {"name": "Anna"}},
    "scenes": {"dock": {"text": "Hello.", "choices": []}},
}


class FakeDialogueEditor:
    def generate(self, request):
        assert request.role == "dialogue-editor"
        assert any("choice IDs" in rule for rule in request.constraints)
        return Proposal(
            role="dialogue-editor",
            summary="Sharpen Anna's greeting",
            operations=(
                {
                    "op": "replace",
                    "path": ["scenes", "dock", "text"],
                    "value": "You came after all.",
                },
            ),
        )


def test_dialogue_request_preserves_logic_constraint():
    request = dialogue_request(STORY, "Make Anna more suspicious")
    assert request.role == "dialogue-editor"
    assert any("gameplay logic" in rule for rule in request.constraints)


def test_dialogue_editor_returns_reviewable_proposal():
    proposal = propose_with_dialogue_editor(
        FakeDialogueEditor(), STORY, "Make Anna more suspicious"
    )
    assert proposal.operations[0]["op"] == "replace"


class WrongRole:
    def generate(self, request):
        return Proposal(role="writer", summary="Wrong", operations=())


def test_dialogue_editor_rejects_wrong_role():
    with pytest.raises(ProposalError):
        propose_with_dialogue_editor(WrongRole(), STORY, "Edit dialogue")
