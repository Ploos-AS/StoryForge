import json

from storyforge.headless import HeadlessRuntime


STORY = {
    "start": "room",
    "scenes": {
        "room": {
            "text": "A room.",
            "choices": [
                {
                    "id": "leave",
                    "text": "Leave",
                    "commands": ["leave room", "go out"],
                    "ending": "outside",
                }
            ],
        }
    },
    "endings": {"outside": {"text": "Outside."}},
}


def test_snapshot_is_json_serializable():
    api = HeadlessRuntime(STORY)
    snapshot = api.snapshot()
    assert snapshot == {
        "status": "playing",
        "scene": "room",
        "text": "A room.",
        "actions": [{
            "id": "leave",
            "text": "Leave",
            "commands": ["leave room", "go out"],
        }],
    }
    json.dumps(snapshot)


def test_execute_by_stable_id_returns_new_snapshot():
    api = HeadlessRuntime(STORY)
    result = api.execute("leave")
    assert result["status"] == "ended"
    assert result["ending"] == {"id": "outside", "text": "Outside."}
    assert result["actions"] == []
    json.dumps(result)


def test_invalid_action_returns_structured_error():
    result = HeadlessRuntime(STORY).execute("missing")
    assert result["status"] == "error"
    assert result["error"]["code"] == "choice_not_available"
    json.dumps(result)
