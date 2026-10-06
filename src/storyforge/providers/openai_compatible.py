import json
from dataclasses import dataclass
from typing import Callable

from ..ai import Proposal, ProposalError, validate_proposal
from ..authoring import AuthoringRequest


Transport = Callable[[str, dict, dict[str, str]], dict]


@dataclass(frozen=True)
class OpenAICompatibleProvider:
    endpoint: str
    model: str
    transport: Transport
    api_key: str | None = None

    def generate(self, request: AuthoringRequest) -> Proposal:
        headers = {"content-type": "application/json"}
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Return only a JSON StoryForge Proposal with keys "
                        "role, summary, operations. Do not return markdown."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "role": request.role,
                            "instruction": request.instruction,
                            "context": request.context,
                            "constraints": list(request.constraints),
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                },
            ],
            "response_format": {"type": "json_object"},
        }
        response = self.transport(self.endpoint, payload, headers)
        try:
            content = response["choices"][0]["message"]["content"]
            data = json.loads(content)
            proposal = Proposal(
                role=data["role"],
                summary=data["summary"],
                operations=tuple(data["operations"]),
            )
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise ProposalError("invalid provider response") from exc
        validate_proposal(proposal)
        return proposal
