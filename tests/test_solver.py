from storyforge.solver import solve, unreachable_endings


def test_solver_finds_stateful_walkthrough():
    story = {
        "storyforge": "0",
        "start": "room",
        "variables": {"has_key": False},
        "scenes": {
            "room": {
                "choices": [
                    {
                        "text": "Take key",
                        "effects": [{"variable": "has_key", "set": True}],
                        "goto": "door",
                    }
                ]
            },
            "door": {
                "choices": [
                    {
                        "text": "Unlock",
                        "requires": [{"variable": "has_key", "equals": True}],
                        "ending": "free",
                    }
                ]
            },
        },
        "endings": {"free": {"text": "Outside."}},
    }
    solutions = solve(story)
    assert [step.choice for step in solutions["free"].steps] == ["Take key", "Unlock"]


def test_solver_reports_unreachable_ending():
    story = {
        "storyforge": "0",
        "start": "room",
        "variables": {"flag": False},
        "scenes": {
            "room": {
                "choices": [
                    {
                        "text": "Impossible",
                        "requires": [{"variable": "flag", "equals": True}],
                        "ending": "secret",
                    },
                    {"text": "Leave", "ending": "normal"},
                ]
            }
        },
        "endings": {"normal": {"text": "Done"}, "secret": {"text": "Secret"}},
    }
    assert unreachable_endings(story) == ["secret"]
