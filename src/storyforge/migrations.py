from copy import deepcopy

from .save import SaveError


class MigrationError(SaveError):
    pass


def migrate_save(data: dict, target_story: dict, migrations: list[dict]) -> dict:
    result = deepcopy(data)
    saved_story = result.get("story")
    metadata = target_story.get("metadata", {})
    target_id = metadata.get("id")
    target_version = metadata.get("version")

    if not saved_story or not target_id or not target_version:
        raise MigrationError("save migration requires bound story identity")
    if saved_story.get("id") != target_id:
        raise MigrationError("cannot migrate a save from a different story")

    by_from = {}
    for migration in migrations:
        source = migration.get("from")
        if source in by_from:
            raise MigrationError(f"duplicate migration from version {source!r}")
        by_from[source] = migration

    seen = set()
    while result["story"]["version"] != target_version:
        version = result["story"]["version"]
        if version in seen:
            raise MigrationError("migration cycle detected")
        seen.add(version)
        migration = by_from.get(version)
        if migration is None:
            raise MigrationError(
                f"no migration path from {version!r} to {target_version!r}"
            )
        destination = migration.get("to")
        if not destination or destination == version:
            raise MigrationError(f"invalid migration destination from {version!r}")
        for operation in migration.get("operations", []):
            _apply_operation(result, operation)
        result["story"]["version"] = destination

    return result


def _rename_key(mapping: dict, old: str, new: str, kind: str) -> None:
    if old not in mapping:
        raise MigrationError(f"cannot rename missing {kind} {old!r}")
    if new in mapping:
        raise MigrationError(f"cannot overwrite existing {kind} {new!r}")
    mapping[new] = mapping.pop(old)


def _apply_operation(save: dict, operation: dict) -> None:
    state = save.setdefault("state", {})
    if "rename_scene" in operation:
        spec = operation["rename_scene"]
        if save.get("scene") == spec["from"]:
            save["scene"] = spec["to"]
        return
    if "rename_ending" in operation:
        spec = operation["rename_ending"]
        if save.get("ending") == spec["from"]:
            save["ending"] = spec["to"]
        return
    if "rename_variable" in operation:
        spec = operation["rename_variable"]
        _rename_key(state.setdefault("variables", {}), spec["from"], spec["to"], "variable")
        return
    if "set_variable" in operation:
        spec = operation["set_variable"]
        state.setdefault("variables", {})[spec["name"]] = deepcopy(spec["value"])
        return
    if "drop_variable" in operation:
        state.setdefault("variables", {}).pop(operation["drop_variable"], None)
        return
    if "rename_item" in operation:
        spec = operation["rename_item"]
        old, new = spec["from"], spec["to"]
        inventory = state.setdefault("inventory", [])
        state["inventory"] = [new if item == old else item for item in inventory]
        ownership = state.setdefault("ownership", {})
        if old in ownership:
            _rename_key(ownership, old, new, "item ownership")
        return
    if "rename_character" in operation:
        spec = operation["rename_character"]
        old, new = spec["from"], spec["to"]
        characters = state.setdefault("characters", {})
        if old in characters:
            _rename_key(characters, old, new, "character")
        ownership = state.setdefault("ownership", {})
        for item, owner in list(ownership.items()):
            if owner == old:
                ownership[item] = new
        return
    raise MigrationError(f"unknown migration operation: {operation!r}")
