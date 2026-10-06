def requirements_met(requirements: list[dict], state: dict) -> bool:
    inventory = set(state.get("_inventory", ()))
    owners = dict(state.get("_owners", ()))
    for req in requirements:
        if "has_item" in req and req["has_item"] not in inventory:
            return False
        if "lacks_item" in req and req["lacks_item"] in inventory:
            return False
        if "owned_by" in req and owners.get(req["owned_by"]["item"]) != req["owned_by"]["character"]:
            return False
        if "variable" in req and state.get(req["variable"]) != req["equals"]:
            return False
    return True


def apply_effects(effects: list[dict], state: dict) -> dict:
    result = dict(state)
    had_inventory = "_inventory" in result
    inventory = set(result.get("_inventory", ()))
    owners = dict(result.get("_owners", ()))
    for effect in effects:
        if "take_item" in effect:
            inventory.add(effect["take_item"])
            owners.pop(effect["take_item"], None)
        elif "drop_item" in effect:
            inventory.discard(effect["drop_item"])
        elif "give_item" in effect:
            item = effect["give_item"]["item"]
            inventory.discard(item)
            owners[item] = effect["give_item"]["character"]
        else:
            name = effect["variable"]
            if "set" in effect:
                result[name] = effect["set"]
            elif "increment" in effect:
                result[name] = result.get(name, 0) + effect["increment"]
            elif "decrement" in effect:
                result[name] = result.get(name, 0) - effect["decrement"]
    if had_inventory or any("take_item" in effect or "drop_item" in effect or "give_item" in effect for effect in effects):
        result["_inventory"] = tuple(sorted(inventory))
    if "_owners" in result or owners or any("give_item" in effect for effect in effects):
        result["_owners"] = tuple(sorted(owners.items()))
    return result


def initial_state(story: dict) -> dict:
    state = dict(story.get("variables", {}))
    state["_inventory"] = tuple(sorted(story.get("inventory", [])))
    ownership = story.get("ownership", {})
    if ownership:
        state["_owners"] = tuple(sorted(ownership.items()))
    return state


def available_choices(scene: dict, state: dict) -> list[dict]:
    from .actions import compile_choice

    choices = [compile_choice(choice) for choice in scene.get("choices", [])]
    return [choice for choice in choices if requirements_met(choice.get("requires", []), state)]
