from storyforge.analysis import dead_states


def test_dead_end_is_detected():
    story = {
        "start": "start",
        "variables": {},
        "scenes": {
            "start": {"choices": [{"text": "Trap", "goto": "trap"}, {"text": "Win", "ending": "win"}]},
            "trap": {"choices": []},
        },
        "endings": {"win": {"text": "Done"}},
    }
    dead = dead_states(story)
    assert [(item.scene, item.kind) for item in dead] == [("trap", "dead-end")]


def test_softlock_cycle_is_detected():
    story = {
        "start": "start",
        "variables": {"key": True},
        "scenes": {
            "start": {
                "choices": [
                    {"text": "Lose key", "effects": [{"variable": "key", "set": False}], "goto": "hall"},
                    {"text": "Keep key", "goto": "hall"},
                ]
            },
            "hall": {
                "choices": [
                    {"text": "Loop", "goto": "hall"},
                    {"text": "Exit", "requires": [{"variable": "key", "equals": True}], "ending": "win"},
                ]
            },
        },
        "endings": {"win": {"text": "Done"}},
    }
    dead = dead_states(story)
    assert any(item.scene == "hall" and item.kind == "softlock" and ("key", False) in item.state for item in dead)


def test_winnable_story_has_no_dead_states():
    story = {
        "start": "start",
        "variables": {},
        "scenes": {"start": {"choices": [{"text": "Win", "ending": "win"}]}},
        "endings": {"win": {"text": "Done"}},
    }
    assert dead_states(story) == []
