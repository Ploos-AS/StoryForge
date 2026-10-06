import pytest

from storyforge.ai import Proposal, ProposalError
from storyforge.authoring import propose_with_writer, writer_request


STORY = {"metadata": {"title": "Demo"}, "scenes": {}}


class FakeWriter:
    def generate(self, request):
        assert request.role == "writer"
        assert request.context is STORY
        assert request.constraints
        return Proposal(
            role="writer",
            summary="Add an opening scene",
            operations=(
                {"op": "add", "path": ["scenes", "opening"], "value": {"text": "Rain.", "choices": []}},
            ),
        )


def test_writer_builds_structured_request():
    request = writer_request(STORY, "Write a noir opening")
    assert request.role == "writer"
    assert request.instruction == "Write a noir opening"
    assert any("machine IDs" in rule for rule in request.constraints)


def test_writer_returns_validated_proposal():
    proposal = propose_with_writer(FakeWriter(), STORY, "Write opening")
    assert proposal.role == "writer"
    assert proposal.operations[0]["path"] == ["scenes", "opening"]


def test_empty_instruction_rejected():
    with pytest.raises(ProposalError):
        writer_request(STORY, "   ")


class WrongRole:
    def generate(self, request):
        return Proposal(role="puzzle-designer", summary="No", operations=())


def test_wrong_role_rejected():
    with pytest.raises(ProposalError):
        propose_with_writer(WrongRole(), STORY, "Write opening")
