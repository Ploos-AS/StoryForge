from storyforge.state import apply_effects, initial_state, requirements_met


def test_initial_character_state_is_canonical():
    story = {"character_state": {"anna": {"trust": 2, "met": False}}}
    state = initial_state(story)
    assert state["_characters"] == (("anna", (("met", False), ("trust", 2))),)


def test_character_requirement():
    state = {"_characters": (("anna", (("met", True), ("trust", 3))),)}
    assert requirements_met([{"character": {"id": "anna", "attribute": "met", "equals": True}}], state)
    assert not requirements_met([{"character": {"id": "anna", "attribute": "trust", "equals": 2}}], state)


def test_character_set_and_increment():
    state = {"_characters": (("anna", (("met", False), ("trust", 1))),)}
    result = apply_effects([
        {"character": {"id": "anna", "attribute": "met", "set": True}},
        {"character": {"id": "anna", "attribute": "trust", "increment": 2}},
    ], state)
    assert result["_characters"] == (("anna", (("met", True), ("trust", 3))),)
