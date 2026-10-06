import pytest

from storyforge.runtime import RuntimeError, Session


STORY = {
    "start": "room",
    "variables": {"open": False},
    "inventory": [],
    "items": {"key": {}},
    "scenes": {
        "room": {
            "text": "A locked room.",
            "choices": [
                {"text": "Take key", "action": {"type": "take", "item": "key"}, "goto": "room"},
                {"text": "Unlock door", "requires": [{"has_item": "key"}], "ending": "free"},
            ],
        }
    },
    "endings": {"free": {"text": "You escape."}},
}


def test_session_uses_storyforge_semantics():
    session = Session(STORY)
    assert session.view().choices == ("Take key",)
    turn = session.choose(0)
    assert turn.choices == ("Unlock door",)
    turn = session.choose(0)
    assert turn.ending == "free"
    assert turn.ending_text == "You escape."


def test_invalid_choice_is_rejected():
    with pytest.raises(RuntimeError):
        Session(STORY).choose(1)


def test_cannot_choose_after_ending():
    session = Session(STORY)
    session.choose(0)
    session.choose(0)
    with pytest.raises(RuntimeError):
        session.choose(0)
