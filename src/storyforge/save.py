from copy import deepcopy

from .runtime import Session


SAVE_FORMAT = "storyforge-save"
SAVE_VERSION = 1


class SaveError(ValueError):
    pass


def dump_session(session: Session) -> dict:
    variables = {k: deepcopy(v) for k, v in session.state.items() if not k.startswith("_")}
    inventory = list(session.state.get("_inventory", ()))
    ownership = dict(session.state.get("_owners", ()))
    characters = {
        name: dict(attrs)
        for name, attrs in session.state.get("_characters", ())
    }
    return {
        "format": SAVE_FORMAT,
        "version": SAVE_VERSION,
        "scene": session.scene,
        "ending": session.ending,
        "state": {
            "variables": variables,
            "inventory": inventory,
            "ownership": ownership,
            "characters": characters,
        },
    }


def load_session(story: dict, data: dict) -> Session:
    if data.get("format") != SAVE_FORMAT:
        raise SaveError("not a StoryForge save")
    if data.get("version") != SAVE_VERSION:
        raise SaveError(f"unsupported save version: {data.get('version')!r}")

    scene = data.get("scene")
    ending = data.get("ending")
    if scene not in story.get("scenes", {}):
        raise SaveError(f"unknown saved scene: {scene!r}")
    if ending is not None and ending not in story.get("endings", {}):
        raise SaveError(f"unknown saved ending: {ending!r}")

    saved = data.get("state", {})
    variables = saved.get("variables", {})
    inventory = saved.get("inventory", [])
    ownership = saved.get("ownership", {})
    characters = saved.get("characters", {})

    if not isinstance(variables, dict) or not isinstance(inventory, list):
        raise SaveError("invalid saved state")
    if not isinstance(ownership, dict) or not isinstance(characters, dict):
        raise SaveError("invalid saved state")

    session = Session(story)
    session.scene = scene
    session.ending = ending
    state = deepcopy(variables)
    state["_inventory"] = tuple(sorted(inventory))
    if ownership:
        state["_owners"] = tuple(sorted(ownership.items()))
    if characters:
        state["_characters"] = tuple(
            sorted((name, tuple(sorted(attrs.items()))) for name, attrs in characters.items())
        )
    session.state = state
    return session
