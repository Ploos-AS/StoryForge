from storyforge.ai import Proposal
from storyforge.authoring import playtest_request, propose_with_playtester


class FakePlaytester:
    def generate(self, request):
        assert request.role == "playtester"
        return Proposal(
            role="playtester",
            summary="Investigate repeated harbour navigation",
            operations=(),
        )


def test_playtester_role_is_adversarial_but_non_authoritative():
    story = {"scenes": {}}
    request = playtest_request(story, "Try unusual legal strategies")
    assert any("Never invent" in rule for rule in request.constraints)
    proposal = propose_with_playtester(
        FakePlaytester(), story, "Try unusual legal strategies"
    )
    assert proposal.role == "playtester"
