import pytest

from storyforge.ai import Proposal, ProposalError, apply_proposal, validate_proposal


STORY = {
    "metadata": {"title": "Demo"},
    "scenes": {"start": {"text": "Old", "choices": []}},
}


def test_apply_proposal_returns_new_story():
    proposal = Proposal(
        role="writer",
        summary="Improve opening",
        operations=({"op": "replace", "path": ["scenes", "start", "text"], "value": "New"},),
    )
    result = apply_proposal(STORY, proposal)
    assert result["scenes"]["start"]["text"] == "New"
    assert STORY["scenes"]["start"]["text"] == "Old"


def test_add_is_explicit():
    proposal = Proposal(
        role="writer",
        summary="Add scene",
        operations=({"op": "add", "path": ["scenes", "second"], "value": {"text": "Hi", "choices": []}},),
    )
    assert "second" in apply_proposal(STORY, proposal)["scenes"]


def test_replace_missing_path_rejected():
    proposal = Proposal(
        role="writer",
        summary="Bad patch",
        operations=({"op": "replace", "path": ["scenes", "missing"], "value": {}},),
    )
    with pytest.raises(ProposalError):
        apply_proposal(STORY, proposal)


def test_unsupported_operation_rejected():
    proposal = Proposal(
        role="writer",
        summary="Delete content",
        operations=({"op": "remove", "path": ["scenes", "start"], "value": None},),
    )
    with pytest.raises(ProposalError):
        validate_proposal(proposal)
