import pytest

from storyforge.pipeline_config import PipelineConfigError, load_pipeline_config


def data():
    return {
        "format": "storyforge-pipeline",
        "version": 1,
        "stages": [
            {
                "name": "draft",
                "role": "writer",
                "instruction": "Improve the opening.",
                "apply": True,
            },
            {
                "name": "review",
                "role": "continuity-editor",
                "instruction": "Check established facts.",
            },
        ],
    }


def test_loads_known_roles_into_editorial_stages():
    pipeline = load_pipeline_config(data())
    assert [stage.name for stage in pipeline.stages] == ["draft", "review"]
    assert pipeline.stages[0].role.name == "writer"
    assert pipeline.stages[0].apply is True
    assert pipeline.stages[1].role.name == "continuity-editor"


def test_unknown_role_fails_closed():
    value = data()
    value["stages"][0]["role"] = "invented-agent"
    with pytest.raises(PipelineConfigError, match="unknown role"):
        load_pipeline_config(value)


def test_duplicate_stage_names_are_rejected():
    value = data()
    value["stages"][1]["name"] = "draft"
    with pytest.raises(PipelineConfigError, match="duplicate stage"):
        load_pipeline_config(value)


def test_unknown_stage_fields_are_rejected():
    value = data()
    value["stages"][0]["magic"] = True
    with pytest.raises(PipelineConfigError, match="unsupported fields"):
        load_pipeline_config(value)
