from storyforge.state import apply_effects, available_choices, requirements_met


def test_requirements_gate_choices():
    scene = {
        "choices": [
            {"text": "Open", "requires": [{"variable": "has_key", "equals": True}]},
            {"text": "Wait"},
        ]
    }
    assert [c["text"] for c in available_choices(scene, {"has_key": False})] == ["Wait"]
    assert [c["text"] for c in available_choices(scene, {"has_key": True})] == ["Open", "Wait"]


def test_effects_are_immutable_and_deterministic():
    initial = {"door_open": False, "trust": 1}
    result = apply_effects(
        [
            {"variable": "door_open", "set": True},
            {"variable": "trust", "increment": 2},
        ],
        initial,
    )
    assert initial == {"door_open": False, "trust": 1}
    assert result == {"door_open": True, "trust": 3}


def test_requirement_equality():
    assert requirements_met([{"variable": "mood", "equals": "calm"}], {"mood": "calm"})
