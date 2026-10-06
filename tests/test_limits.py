import pytest

from storyforge.analysis import build_state_graph
from storyforge.limits import StateSpaceLimitError
from storyforge.solver import solve


def unbounded_story():
    return {
        "start": "loop",
        "variables": {"counter": 0},
        "scenes": {
            "loop": {
                "choices": [{
                    "text": "Again",
                    "effects": [{"variable": "counter", "increment": 1}],
                    "goto": "loop",
                }]
            }
        },
        "endings": {},
    }


def test_solver_stops_at_state_limit():
    with pytest.raises(StateSpaceLimitError):
        solve(unbounded_story(), max_states=8)


def test_analysis_stops_at_state_limit():
    with pytest.raises(StateSpaceLimitError):
        build_state_graph(unbounded_story(), max_states=8)
