from pathlib import Path
from storyforge.loader import load_story
from storyforge.schema import validate_schema
from storyforge.validator import validate_story


def test_lighthouse_is_valid():
    story = load_story(Path("examples/lighthouse/story.yaml"))
    assert validate_schema(story) == []
    assert validate_story(story) == []


def test_missing_target_is_rejected():
    story = {
        "storyforge": "0",
        "start": "a",
        "scenes": {"a": {"choices": [{"text": "Go", "goto": "missing"}]}},
        "endings": {},
    }
    assert any("missing scene" in error for error in validate_story(story))


def test_schema_rejects_unknown_profile():
    story = {
        "storyforge": "0",
        "metadata": {"profile": "platformer"},
        "start": "a",
        "scenes": {"a": {"choices": [{"text": "End", "ending": "end"}]}},
        "endings": {"end": {"text": "Done"}},
    }
    assert any("platformer" in error for error in validate_schema(story))
