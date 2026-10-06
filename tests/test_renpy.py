from pathlib import Path

from storyforge.exporters.renpy import export_renpy


def test_renpy_exports_requirements_effects_and_actions(tmp_path: Path):
    story = {
        "start": "room",
        "variables": {"open": False},
        "inventory": [],
        "ownership": {},
        "character_state": {"anna": {"trust": 1}},
        "items": {"key": {}, "coin": {}},
        "characters": {"anna": {}},
        "scenes": {
            "room": {
                "text": "Room",
                "choices": [
                    {"text": "Take key", "action": {"type": "take", "item": "key"}, "goto": "room"},
                    {
                        "text": "Unlock",
                        "requires": [{"has_item": "key"}],
                        "effects": [
                            {"variable": "open", "set": True},
                            {"character": {"id": "anna", "attribute": "trust", "increment": 1}},
                        ],
                        "ending": "win",
                    },
                ],
            }
        },
        "endings": {"win": {"text": "Open"}},
    }
    output = tmp_path / "script.rpy"
    export_renpy(story, output)
    text = output.read_text()
    assert "default sf_vars = {'open': False}" in text
    assert "'key' not in sf_inventory" in text
    assert "$ sf_inventory.add('key')" in text
    assert '"Unlock" if \'key\' in sf_inventory:' in text
    assert "$ sf_vars['open'] = True" in text
    assert "sf_characters.setdefault('anna', {})['trust']" in text
