import json

from storyforge.ai import Proposal
from storyforge.approval import approve, approval_matches, proposal_fingerprint, reject


def proposal(text="New"):
    return Proposal(
        role="writer",
        summary="Edit opening",
        operations=(
            {"op": "replace", "path": ["scenes", "start", "text"], "value": text},
        ),
    )


def test_approval_is_json_serializable_and_bound_to_proposal():
    item = proposal()
    approval = approve(item, "editor", "Looks good")
    data = approval.to_dict()
    json.dumps(data)
    assert data["format"] == "storyforge-approval"
    assert data["version"] == 1
    assert data["decision"] == "approved"
    assert approval_matches(approval, item)


def test_changed_proposal_invalidates_approval():
    approval = approve(proposal(), "editor")
    assert not approval_matches(approval, proposal("Changed after review"))


def test_fingerprint_is_deterministic():
    assert proposal_fingerprint(proposal()) == proposal_fingerprint(proposal())


def test_rejection_is_also_a_review_artifact():
    item = proposal()
    approval = reject(item, "editor", "Breaks tone")
    assert approval.decision == "rejected"
    assert approval_matches(approval, item)
