import pytest

from storyforge.runtime import RuntimeError, Session
from storyforge.validator import validate_story


STORY = {
    "start": "room",
    "scenes": {
        "room": {
            "choices": [
                {"id": "wait", "text": "Wait", "commands": ["wait here"], "goto": "room"},
                {"id": "leave", "text": "Leave", "ending": "end"},
            ]
        }
    },
    "endings": {"end": {}},
}


def test_actions_expose_stable_machine_interface():
    session = Session(STORY)
    actions = session.actions()
    assert actions[0].id == "wait"
    assert actions[0].text == "Wait"
    assert actions[0].commands == ("wait here",)


def test_choose_id_executes_same_transition():
    session = Session(STORY)
    turn = session.choose_id("leave")
    assert turn.ending == "end"


def test_unknown_choice_id_is_rejected():
    with pytest.raises(RuntimeError):
        Session(STORY).choose_id("missing")


def test_duplicate_choice_ids_are_invalid():
    story = {
        "start": "a",
        "scenes": {
            "a": {"choices": [{"id": "same", "text": "A", "goto": "b"}]},
            "b": {"choices": [{"id": "same", "text": "B", "ending": "end"}]},
        },
        "endings": {"end": {}},
    }
    assert "duplicate choice id 'same'" in validate_story(story)
