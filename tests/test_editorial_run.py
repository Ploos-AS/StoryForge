import copy
import json

import pytest

from storyforge.ai import Proposal
from storyforge.editorial import EditorialResult, GateResult, StageResult
from storyforge.editorial_run import EditorialRunError, dump_editorial_result, load_editorial_run


def result():
    proposal = Proposal(
        role="writer",
        summary="Draft",
        operations=(
            {"op": "replace", "path": ["scenes", "start", "text"], "value": "New"},
        ),
    )
    return EditorialResult(
        {"scenes": {"start": {"text": "New"}}},
        (StageResult("draft", proposal, True, GateResult(True)),),
        halted=False,
    )


def test_editorial_run_is_json_roundtrippable():
    data = dump_editorial_result(result())
    encoded = json.dumps(data)
    loaded = json.loads(encoded)
    assert load_editorial_run(loaded) == loaded
    assert loaded["format"] == "storyforge-editorial-run"
    assert loaded["version"] == 1


def test_tampered_proposal_is_rejected():
    data = dump_editorial_result(result())
    data["stages"][0]["proposal"]["operations"][0]["value"] = "Tampered"
    with pytest.raises(EditorialRunError, match="fingerprint mismatch"):
        load_editorial_run(data)


def test_wrong_format_and_version_are_rejected():
    data = dump_editorial_result(result())
    wrong = copy.deepcopy(data)
    wrong["format"] = "other"
    with pytest.raises(EditorialRunError):
        load_editorial_run(wrong)
    wrong = copy.deepcopy(data)
    wrong["version"] = 2
    with pytest.raises(EditorialRunError):
        load_editorial_run(wrong)
