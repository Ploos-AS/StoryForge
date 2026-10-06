import json

import pytest

from storyforge.ai import ProposalError
from storyforge.authoring import writer_request
from storyforge.providers.openai_compatible import OpenAICompatibleProvider


STORY = {"scenes": {"start": {"text": "Old"}}}


def test_provider_maps_request_and_parses_proposal():
    seen = {}

    def transport(endpoint, payload, headers):
        seen.update(endpoint=endpoint, payload=payload, headers=headers)
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "role": "writer",
                                "summary": "Rewrite",
                                "operations": [
                                    {
                                        "op": "replace",
                                        "path": ["scenes", "start", "text"],
                                        "value": "New",
                                    }
                                ],
                            }
                        )
                    }
                }
            ]
        }

    provider = OpenAICompatibleProvider(
        "http://localhost/v1/chat/completions", "test-model", transport, "secret"
    )
    proposal = provider.generate(writer_request(STORY, "Rewrite opening"))
    assert proposal.role == "writer"
    assert proposal.operations[0]["value"] == "New"
    assert seen["payload"]["model"] == "test-model"
    assert seen["payload"]["response_format"] == {"type": "json_object"}
    assert seen["headers"]["authorization"] == "Bearer secret"
    user = json.loads(seen["payload"]["messages"][1]["content"])
    assert user["instruction"] == "Rewrite opening"
    assert user["context"] == STORY


def test_invalid_provider_response_fails_closed():
    provider = OpenAICompatibleProvider(
        "http://localhost", "model", lambda endpoint, payload, headers: {"choices": []}
    )
    with pytest.raises(ProposalError, match="invalid provider response"):
        provider.generate(writer_request(STORY, "Rewrite"))
