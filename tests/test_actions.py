import pytest

from storyforge.actions import ActionError, compile_action, compile_choice


def test_take_compiles_to_inventory_primitives():
    req, effects = compile_action({"type": "take", "item": "key"})
    assert req == [{"lacks_item": "key"}]
    assert effects == [{"take_item": "key"}]


def test_use_keeps_explicit_effects():
    choice = compile_choice({
        "text": "Use key",
        "action": {"type": "use", "item": "key", "effects": [{"variable": "open", "set": True}]},
        "ending": "win",
    })
    assert choice["requires"] == [{"has_item": "key"}]
    assert choice["effects"] == [{"variable": "open", "set": True}]
    assert "action" not in choice


def test_combine_consumes_inputs_and_creates_result():
    req, effects = compile_action({"type": "combine", "left": "stick", "right": "cloth", "result": "torch"})
    assert req == [{"has_item": "stick"}, {"has_item": "cloth"}]
    assert effects == [{"drop_item": "stick"}, {"drop_item": "cloth"}, {"take_item": "torch"}]


def test_combine_rejects_same_item_ids():
    with pytest.raises(ActionError):
        compile_action({"type": "combine", "left": "key", "right": "key", "result": "key"})
