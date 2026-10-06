from storyforge.parser import Command, parse_command
from storyforge.runtime import Session


def test_explicit_affordance_selects_choice():
    choices = ("Pick up the rusty key", "Leave")
    commands = (("take key", "get key"), ("leave",))
    assert parse_command("take key", choices, commands) == Command("choose", 0)


def test_ambiguous_affordance_is_not_selected():
    choices = ("Take red key", "Take blue key")
    commands = (("take key",), ("take key",))
    assert parse_command("take key", choices, commands) == Command("unknown")


def test_unavailable_choice_does_not_expose_commands():
    story = {
        "start": "room",
        "variables": {"open": False},
        "scenes": {
            "room": {
                "choices": [{
                    "text": "Open door",
                    "commands": ["open door"],
                    "requires": [{"variable": "open", "equals": True}],
                    "ending": "end",
                }]
            }
        },
        "endings": {"end": {}},
    }
    session = Session(story)
    assert session.choices() == []
