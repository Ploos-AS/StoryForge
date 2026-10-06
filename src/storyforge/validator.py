from collections import deque


def validate_story(story: dict) -> list[str]:
    errors: list[str] = []
    if story.get("storyforge") != "0":
        errors.append("storyforge must be '0'")
    variables = story.get("variables", {})
    items = story.get("items", {})
    for item in story.get("inventory", []):
        if item not in items:
            errors.append(f"initial inventory references unknown item {item!r}")
    start = story.get("start")
    scenes = story.get("scenes", {})
    endings = story.get("endings", {})
    if not isinstance(scenes, dict) or not scenes:
        errors.append("scenes must be a non-empty mapping")
        return errors
    if start not in scenes:
        errors.append(f"start scene {start!r} does not exist")
    targets = {}
    for scene_id, scene in scenes.items():
        targets[scene_id] = []
        if not isinstance(scene, dict):
            errors.append(f"scene {scene_id!r} must be a mapping")
            continue
        for choice in scene.get("choices", []):
            for req in choice.get("requires", []):
                if "variable" in req and req.get("variable") not in variables:
                    errors.append(f"choice in {scene_id!r} requires unknown variable {req.get('variable')!r}")
                item = req.get("has_item") or req.get("lacks_item")
                if item and item not in items:
                    errors.append(f"choice in {scene_id!r} references unknown item {item!r}")
            for effect in choice.get("effects", []):
                if "variable" in effect and effect.get("variable") not in variables:
                    errors.append(f"choice in {scene_id!r} changes unknown variable {effect.get('variable')!r}")
                item = effect.get("take_item") or effect.get("drop_item")
                if item and item not in items:
                    errors.append(f"choice in {scene_id!r} changes unknown item {item!r}")
            target, ending = choice.get("goto"), choice.get("ending")
            if bool(target) == bool(ending):
                errors.append(f"choice in {scene_id!r} must have exactly one of goto or ending")
            elif target:
                targets[scene_id].append(target)
                if target not in scenes:
                    errors.append(f"scene {scene_id!r} targets missing scene {target!r}")
            elif ending not in endings:
                errors.append(f"scene {scene_id!r} targets missing ending {ending!r}")
    if start in scenes:
        reachable, queue = {start}, deque([start])
        while queue:
            for target in targets.get(queue.popleft(), []):
                if target in scenes and target not in reachable:
                    reachable.add(target); queue.append(target)
        for scene_id in scenes:
            if scene_id not in reachable:
                errors.append(f"scene {scene_id!r} is unreachable")
    return errors
