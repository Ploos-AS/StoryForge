class ActionError(ValueError):
    pass


def compile_action(action: dict) -> tuple[list[dict], list[dict]]:
    """Compile a semantic adventure action to deterministic requirements/effects."""
    kind = action.get("type")

    if kind == "take":
        item = action["item"]
        return [{"lacks_item": item}], [{"take_item": item}]

    if kind == "drop":
        item = action["item"]
        return [{"has_item": item}], [{"drop_item": item}]

    if kind == "use":
        item = action["item"]
        return [{"has_item": item}], list(action.get("effects", []))

    if kind == "give":
        item = action["item"]
        character = action["character"]
        return [{"has_item": item}], [{"give_item": {"item": item, "character": character}}]

    if kind == "combine":
        left = action["left"]
        right = action["right"]
        result = action["result"]
        if len({left, right, result}) != 3:
            raise ActionError("combine requires three distinct item ids")
        return (
            [{"has_item": left}, {"has_item": right}],
            [{"drop_item": left}, {"drop_item": right}, {"take_item": result}],
        )

    raise ActionError(f"unknown action type: {kind!r}")


def compile_choice(choice: dict) -> dict:
    """Return a choice with semantic action lowered into primitive IR."""
    if "action" not in choice:
        return choice
    requirements, effects = compile_action(choice["action"])
    result = dict(choice)
    del result["action"]
    result["requires"] = requirements + list(result.get("requires", []))
    result["effects"] = effects + list(result.get("effects", []))
    return result
