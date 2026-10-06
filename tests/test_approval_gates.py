from storyforge.ai import Proposal
from storyforge.approval import approve, reject
from storyforge.gates import all_gates, approval_gate


STORY = {"scenes": {}}


def proposal(value="A"):
    return Proposal(
        role="writer",
        summary="Edit",
        operations=(
            {"op": "add", "path": ["scenes", "start"], "value": {"text": value}},
        ),
    )


def test_matching_approval_passes():
    item = proposal()
    result = approval_gate(approve(item, "editor"))(STORY, item)
    assert result.accepted


def test_rejection_fails_closed():
    item = proposal()
    result = approval_gate(reject(item, "editor", "No"))(STORY, item)
    assert not result.accepted
    assert "rejected" in result.reason


def test_changed_proposal_fails_closed():
    original = proposal()
    result = approval_gate(approve(original, "editor"))(STORY, proposal("B"))
    assert not result.accepted
    assert "does not match" in result.reason


def test_all_gates_requires_every_gate():
    item = proposal()
    calls = []

    def first(story, proposal):
        calls.append("first")
        from storyforge.editorial import GateResult
        return GateResult(True)

    def second(story, proposal):
        calls.append("second")
        from storyforge.editorial import GateResult
        return GateResult(False, "blocked")

    def third(story, proposal):
        calls.append("third")
        from storyforge.editorial import GateResult
        return GateResult(True)

    result = all_gates(first, second, third)(STORY, item)
    assert not result.accepted
    assert result.reason == "blocked"
    assert calls == ["first", "second"]
