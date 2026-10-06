from dataclasses import dataclass

from .headless import HeadlessRuntime


@dataclass(frozen=True)
class PlaytestStep:
    action_id: str
    before: dict
    after: dict


@dataclass(frozen=True)
class PlaytestTrace:
    initial: dict
    steps: tuple[PlaytestStep, ...]
    final: dict


def execute_plan(story: dict, action_ids: list[str]) -> PlaytestTrace:
    runtime = HeadlessRuntime(story)
    initial = runtime.snapshot()
    steps = []
    for action_id in action_ids:
        before = runtime.snapshot()
        after = runtime.execute(action_id)
        steps.append(PlaytestStep(action_id, before, after))
        if after.get("status") in {"ended", "error"}:
            break
    return PlaytestTrace(initial, tuple(steps), runtime.snapshot())
