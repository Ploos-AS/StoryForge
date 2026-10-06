from storyforge.assets import asset_manifest


def test_manifest_is_stable_and_provider_neutral():
    story = {
        "assets": {
            "dock_bg": {
                "kind": "background",
                "description": "Stormy harbour at night",
                "target": "amiga-ocs",
                "constraints": ["320x256", "32 colours"],
            },
            "anna_portrait": {
                "kind": "portrait",
                "description": "Anna, suspicious expression",
            },
        }
    }
    manifest = asset_manifest(story)
    assert manifest["format"] == "storyforge-assets"
    assert manifest["version"] == 1
    assert [asset["id"] for asset in manifest["assets"]] == [
        "anna_portrait",
        "dock_bg",
    ]
    assert manifest["assets"][1]["target"] == "amiga-ocs"
    assert manifest["assets"][1]["constraints"] == ["320x256", "32 colours"]


def test_empty_manifest_is_valid():
    assert asset_manifest({}) == {
        "format": "storyforge-assets",
        "version": 1,
        "assets": [],
    }
