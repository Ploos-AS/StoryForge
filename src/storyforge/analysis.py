from collections import defaultdict, deque
from dataclasses import dataclass

from .state import apply_effects, available_choices


StateKey = tuple[str, tuple[tuple[str, object], ...]]


@dataclass(frozen=True)
class DeadState:
    scene: str
    state: tuple[tuple[str, object], ...]
    kind: str


def _freeze(state: dict) -> tuple[tuple[str, object], ...]:
    return tuple(sorted(state.items()))


def build_state_graph(story: dict):
    initial = dict(story.get("variables", {}))
    start: StateKey = (story["start"], _freeze(initial))
    queue = deque([(story["start"], initial)])
    visited = {start}
    edges: dict[StateKey, set[StateKey]] = defaultdict(set)
    ending_sources: set[StateKey] = set()

    while queue:
        scene_id, state = queue.popleft()
        key = (scene_id, _freeze(state))
        for choice in available_choices(story["scenes"][scene_id], state):
            next_state = apply_effects(choice.get("effects", []), state)
            if choice.get("ending"):
                ending_sources.add(key)
                continue
            target_key = (choice["goto"], _freeze(next_state))
            edges[key].add(target_key)
            if target_key not in visited:
                visited.add(target_key)
                queue.append((choice["goto"], next_state))

    return visited, edges, ending_sources


def dead_states(story: dict) -> list[DeadState]:
    states, edges, ending_sources = build_state_graph(story)
    reverse: dict[StateKey, set[StateKey]] = defaultdict(set)
    for source, targets in edges.items():
        for target in targets:
            reverse[target].add(source)

    can_finish = set(ending_sources)
    queue = deque(ending_sources)
    while queue:
        current = queue.popleft()
        for predecessor in reverse.get(current, set()):
            if predecessor not in can_finish:
                can_finish.add(predecessor)
                queue.append(predecessor)

    result = []
    for scene, state in sorted(states - can_finish):
        kind = "dead-end" if not edges.get((scene, state)) else "softlock"
        result.append(DeadState(scene, state, kind))
    return result
