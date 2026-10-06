import pytest

from storyforge.ai import Proposal, ProposalError
from storyforge.authoring import continuity_request, propose_with_continuity_editor


STORY = {"characters": {"anna": {}}, "scenes": {}}


class FakeContinuityEditor:
    def generate(self, request):
        assert request.role == "continuity-editor"
        return Proposal(
            role="continuity-editor",
            summary="Clarify established fact",
            operations=(
                {"op": "add", "path": ["characters", "anna", "description"], "value": "Harbour keeper"},
            ),
        )


def test_continuity_role_contract():
    request = continuity_request(STORY, "Check Anna's description")
    assert any("authoritative" in rule for rule in request.constraints)
    assert propose_with_continuity_editor(
        FakeContinuityEditor(), STORY, "Clarify Anna"
    ).role == "continuity-editor"


class WrongRole:
    def generate(self, request):
        return Proposal(role="writer", summary="Wrong", operations=())


def test_wrong_role_rejected():
    with pytest.raises(ProposalError):
        propose_with_continuity_editor(WrongRole(), STORY, "Check continuity")
