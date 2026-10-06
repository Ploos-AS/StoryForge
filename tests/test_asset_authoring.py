from storyforge.ai import Proposal
from storyforge.authoring import asset_spec_request, propose_with_asset_spec_generator


STORY = {"assets": {}}


class FakeAssetSpecGenerator:
    def generate(self, request):
        assert request.role == "asset-spec-generator"
        return Proposal(
            role="asset-spec-generator",
            summary="Add harbour background requirement",
            operations=(
                {
                    "op": "add",
                    "path": ["assets", "dock_bg"],
                    "value": {
                        "kind": "background",
                        "description": "Stormy harbour at night",
                        "target": "amiga-ocs",
                        "constraints": ["320x256", "32 colours"],
                    },
                },
            ),
        )


def test_asset_spec_role_is_provider_neutral():
    request = asset_spec_request(STORY, "Specify the harbour art")
    assert any("specific" in rule and "provider" in rule for rule in request.constraints)
    proposal = propose_with_asset_spec_generator(
        FakeAssetSpecGenerator(), STORY, "Specify harbour art"
    )
    assert proposal.operations[0]["path"] == ["assets", "dock_bg"]
