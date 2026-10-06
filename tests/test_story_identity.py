import pytest

from storyforge.runtime import Session
from storyforge.save import SaveError, dump_session, load_session


def story(version="1.2.3"):
    return {
        "metadata": {"id": "demo.story", "version": version},
        "start": "start",
        "scenes": {"start": {"choices": []}},
        "endings": {},
    }


def test_save_contains_story_identity():
    data = dump_session(Session(story()))
    assert data["story"] == {"id": "demo.story", "version": "1.2.3"}


def test_matching_story_identity_loads():
    data = dump_session(Session(story()))
    assert load_session(story(), data).scene == "start"


def test_different_story_version_is_rejected():
    data = dump_session(Session(story("1.2.3")))
    with pytest.raises(SaveError):
        load_session(story("1.2.4"), data)


def test_legacy_unbound_save_remains_loadable():
    data = dump_session(Session(story()))
    data["story"] = None
    assert load_session(story(), data).scene == "start"
