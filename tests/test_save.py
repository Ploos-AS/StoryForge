import json
import pytest

from storyforge.runtime import Session
from storyforge.save import SaveError, dump_session, load_session


STORY = {
    "start": "a",
    "variables": {"score": 1},
    "inventory": ["key"],
    "ownership": {"coin": "anna"},
    "character_state": {"anna": {"trust": 2}},
    "scenes": {
        "a": {"choices": [{"id": "go", "text": "Go", "effects": [{"variable": "score", "increment": 1}], "goto": "b"}]},
        "b": {"choices": [{"id": "end", "text": "End", "ending": "done"}]},
    },
    "endings": {"done": {"text": "Done"}},
}


def test_save_is_json_and_round_trips_canonical_state():
    session = Session(STORY)
    session.choose_id("go")
    data = dump_session(session)
    json.dumps(data)
    restored = load_session(STORY, data)
    assert restored.scene == session.scene
    assert restored.ending == session.ending
    assert restored.state == session.state
    assert restored.actions()[0].id == "end"


def test_ended_session_round_trips():
    session = Session(STORY)
    session.choose_id("go")
    session.choose_id("end")
    restored = load_session(STORY, dump_session(session))
    assert restored.view().ending == "done"


def test_wrong_format_and_version_are_rejected():
    with pytest.raises(SaveError):
        load_session(STORY, {"format": "other", "version": 1})
    with pytest.raises(SaveError):
        load_session(STORY, {"format": "storyforge-save", "version": 99})


def test_unknown_scene_is_rejected():
    data = dump_session(Session(STORY))
    data["scene"] = "missing"
    with pytest.raises(SaveError):
        load_session(STORY, data)
