from storyforge.playtest import execute_plan


STORY = {
    "storyforge": "0",
    "start": "start",
    "scenes": {
        "start": {
            "text": "Choose.",
            "choices": [
                {"id": "go", "text": "Go", "goto": "hall"},
            ],
        },
        "hall": {
            "text": "Hall.",
            "choices": [
                {"id": "finish", "text": "Finish", "ending": "done"},
            ],
        },
    },
    "endings": {"done": {"text": "Done."}},
}


def test_plan_executes_only_through_headless_runtime():
    trace = execute_plan(STORY, ["go", "finish"])
    assert trace.initial["scene"] == "start"
    assert [step.action_id for step in trace.steps] == ["go", "finish"]
    assert trace.steps[0].after["scene"] == "hall"
    assert trace.final["status"] == "ended"
    assert trace.final["ending"]["id"] == "done"


def test_illegal_action_is_recorded_and_stops_plan():
    trace = execute_plan(STORY, ["not-real", "go"])
    assert len(trace.steps) == 1
    assert trace.steps[0].after["status"] == "error"
    assert trace.steps[0].after["error"]["code"] == "choice_not_available"
