from storyforge.actions import compile_action
from storyforge.state import apply_effects, initial_state, requirements_met


def test_give_moves_item_to_character():
    req, effects = compile_action({"type": "give", "item": "key", "character": "anna"})
    assert req == [{"has_item": "key"}]
    state = {"_inventory": ("key",), "_owners": ()}
    result = apply_effects(effects, state)
    assert result["_inventory"] == ()
    assert result["_owners"] == (("key", "anna"),)


def test_owned_by_requirement():
    state = {"_inventory": (), "_owners": (("key", "anna"),)}
    assert requirements_met([{"owned_by": {"item": "key", "character": "anna"}}], state)
    assert not requirements_met([{"owned_by": {"item": "key", "character": "bob"}}], state)


def test_take_transfers_item_back_to_player():
    state = {"_inventory": (), "_owners": (("key", "anna"),)}
    result = apply_effects([{"take_item": "key"}], state)
    assert result["_inventory"] == ("key",)
    assert result["_owners"] == ()


def test_initial_ownership_is_canonical():
    story = {"inventory": [], "ownership": {"coin": "bob", "key": "anna"}}
    state = initial_state(story)
    assert state["_owners"] == (("coin", "bob"), ("key", "anna"))
