from storyforge.ai import Proposal
from storyforge.qualification import qualify_puzzle_proposal


BASE = {
    "storyforge": "0",
    "start": "start",
    "scenes": {
        "start": {
            "text": "A locked door.",
            "choices": [{"id": "open", "text": "Open", "ending": "escaped"}],
        }
    },
    "endings": {"escaped": {"text": "Outside."}},
}


def test_solvable_candidate_is_accepted():
    proposal = Proposal(
        role="puzzle-designer",
        summary="Improve prose without changing solution",
        operations=(
            {"op": "replace", "path": ["scenes", "start", "text"], "value": "A heavy locked door."},
        ),
    )
    result = qualify_puzzle_proposal(BASE, proposal)
    assert result.accepted
    assert result.solved_endings == ("escaped",)


def test_unreachable_ending_is_rejected():
    proposal = Proposal(
        role="puzzle-designer",
        summary="Add unreachable ending",
        operations=(
            {"op": "add", "path": ["endings", "secret"], "value": {"text": "Secret."}},
        ),
    )
    result = qualify_puzzle_proposal(BASE, proposal)
    assert not result.accepted
    assert "unreachable endings: secret" in result.errors
