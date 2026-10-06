import pytest

from storyforge.ai import Proposal
from storyforge.pipeline_config import PipelineConfigError, load_pipeline_config


BASE = {
    "format": "storyforge-pipeline",
    "version": 1,
    "stages": [
        {
            "name": "draft",
            "role": "writer",
            "instruction": "Draft.",
            "apply": True,
        }
    ],
}


def test_human_approval_gate_halts_fail_closed():
    data = {**BASE, "stages": [{**BASE["stages"][0], "gate": "human-approval"}]}
    stage = load_pipeline_config(data).stages[0]
    result = stage.gate({}, Proposal("writer", "draft", ()))
    assert result.accepted is False
    assert result.reason == "human approval required"


def test_gate_list_is_ordered_and_composed():
    data = {
        **BASE,
        "stages": [
            {
                **BASE["stages"][0],
                "role": "puzzle-designer",
                "gate": ["puzzle-solver", "human-approval"],
            }
        ],
    }
    stage = load_pipeline_config(data).stages[0]
    assert stage.gate is not None


def test_unknown_gate_fails_closed():
    data = {**BASE, "stages": [{**BASE["stages"][0], "gate": "shell-command"}]}
    with pytest.raises(PipelineConfigError, match="unknown gate"):
        load_pipeline_config(data)
