from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class DesignMetrics:
    scenes: int
    endings: int
    choices: int
    branching_scenes: int
    average_choices_per_scene: float
    shortest_ending_steps: int | None
    longest_shortest_ending_steps: int | None


def design_metrics(story: dict) -> DesignMetrics:
    scenes = story.get("scenes", {})
    choices = sum(len(scene.get("choices", [])) for scene in scenes.values())
    branching = sum(len(scene.get("choices", [])) > 1 for scene in scenes.values())

    distances = {}
    start = story.get("start")
    if start in scenes:
        queue = deque([(start, 0)])
        seen = {start}
        while queue:
            scene_id, distance = queue.popleft()
            for choice in scenes[scene_id].get("choices", []):
                ending = choice.get("ending")
                if ending is not None:
                    distances[ending] = min(distances.get(ending, distance + 1), distance + 1)
                target = choice.get("goto")
                if target in scenes and target not in seen:
                    seen.add(target)
                    queue.append((target, distance + 1))

    values = tuple(distances.values())
    return DesignMetrics(
        scenes=len(scenes),
        endings=len(story.get("endings", {})),
        choices=choices,
        branching_scenes=branching,
        average_choices_per_scene=(choices / len(scenes)) if scenes else 0.0,
        shortest_ending_steps=min(values) if values else None,
        longest_shortest_ending_steps=max(values) if values else None,
    )
