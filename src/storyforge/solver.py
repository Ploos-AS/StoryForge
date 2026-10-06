from collections import deque
from dataclasses import dataclass

from .state import apply_effects, available_choices, initial_state


@dataclass(frozen=True)
class Step:
    scene: str
    choice: str


@dataclass(frozen=True)
class Solution:
    ending: str
    steps: tuple[Step, ...]
    final_state: tuple[tuple[str, object], ...]


def _freeze(state: dict) -> tuple[tuple[str, object], ...]:
    return tuple(sorted(state.items()))


def solve(story: dict) -> dict[str, Solution]:
    """Return the shortest deterministic walkthrough found for each ending."""
    start = story["start"]
    initial = initial_state(story)
    queue = deque([(start, initial, tuple())])
    visited = {(start, _freeze(initial))}
    solutions: dict[str, Solution] = {}

    while queue:
        scene_id, state, steps = queue.popleft()
        scene = story["scenes"][scene_id]
        for choice in available_choices(scene, state):
            next_state = apply_effects(choice.get("effects", []), state)
            next_steps = steps + (Step(scene_id, choice["text"]),)
            if choice.get("ending"):
                ending = choice["ending"]
                solutions.setdefault(
                    ending,
                    Solution(ending, next_steps, _freeze(next_state)),
                )
                continue

            target = choice["goto"]
            key = (target, _freeze(next_state))
            if key not in visited:
                visited.add(key)
                queue.append((target, next_state, next_steps))

    return solutions


def unreachable_endings(story: dict) -> list[str]:
    reached = solve(story)
    return sorted(set(story.get("endings", {})) - set(reached))
