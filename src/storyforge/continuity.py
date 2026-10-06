from dataclasses import dataclass


@dataclass(frozen=True)
class ContinuityIssue:
    code: str
    message: str
    path: tuple[str, ...]


def continuity_issues(story: dict) -> list[ContinuityIssue]:
    issues = []
    characters = story.get("characters", {})
    items = story.get("items", {})
    locations = story.get("locations", {})

    for character in story.get("character_state", {}):
        if character not in characters:
            issues.append(ContinuityIssue(
                "unknown-character-state",
                f"character_state references unknown character {character!r}",
                ("character_state", character),
            ))

    for item, owner in story.get("ownership", {}).items():
        if item not in items:
            issues.append(ContinuityIssue(
                "unknown-owned-item",
                f"ownership references unknown item {item!r}",
                ("ownership", item),
            ))
        if owner not in characters:
            issues.append(ContinuityIssue(
                "unknown-owner",
                f"ownership references unknown character {owner!r}",
                ("ownership", item),
            ))

    inventory = story.get("inventory", [])
    for item in inventory:
        if item not in items:
            issues.append(ContinuityIssue(
                "unknown-inventory-item",
                f"inventory references unknown item {item!r}",
                ("inventory", item),
            ))
        if item in story.get("ownership", {}):
            issues.append(ContinuityIssue(
                "conflicting-item-owner",
                f"item {item!r} is both in player inventory and NPC ownership",
                ("inventory", item),
            ))

    for scene_id, scene in story.get("scenes", {}).items():
        location = scene.get("location")
        if location is not None and location not in locations:
            issues.append(ContinuityIssue(
                "unknown-scene-location",
                f"scene {scene_id!r} references unknown location {location!r}",
                ("scenes", scene_id, "location"),
            ))

    return issues
