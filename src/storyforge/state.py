def requirements_met(requirements: list[dict], state: dict) -> bool:
    return all(state.get(req["variable"]) == req["equals"] for req in requirements)


def apply_effects(effects: list[dict], state: dict) -> dict:
    result = dict(state)
    for effect in effects:
        name = effect["variable"]
        if "set" in effect:
            result[name] = effect["set"]
        elif "increment" in effect:
            result[name] = result.get(name, 0) + effect["increment"]
        elif "decrement" in effect:
            result[name] = result.get(name, 0) - effect["decrement"]
    return result


def available_choices(scene: dict, state: dict) -> list[dict]:
    return [
        choice for choice in scene.get("choices", [])
        if requirements_met(choice.get("requires", []), state)
    ]
