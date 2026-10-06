from storyforge.state import apply_effects, initial_state, requirements_met


def test_take_and_drop_item():
    state = {"_inventory": ()}
    taken = apply_effects([{"take_item": "key"}], state)
    assert taken["_inventory"] == ("key",)
    dropped = apply_effects([{"drop_item": "key"}], taken)
    assert dropped["_inventory"] == ()


def test_inventory_requirements():
    state = {"_inventory": ("key",)}
    assert requirements_met([{"has_item": "key"}], state)
    assert not requirements_met([{"lacks_item": "key"}], state)


def test_initial_inventory_is_sorted():
    story = {"variables": {"score": 0}, "inventory": ["coin", "apple"]}
    assert initial_state(story) == {"score": 0, "_inventory": ("apple", "coin")}
