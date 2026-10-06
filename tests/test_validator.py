from pathlib import Path
from storyforge.loader import load_story
from storyforge.validator import validate_story


def test_lighthouse_is_valid():
    assert validate_story(load_story(Path("examples/lighthouse/story.yaml"))) == []


def test_missing_target_is_rejected():
    story = {"storyforge": "0", "start": "a", "scenes": {"a": {"choices": [{"text": "Go", "goto": "missing"}]}}, "endings": {}}
    assert any("missing scene" in error for error in validate_story(story))
