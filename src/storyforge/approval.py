import hashlib
import json
from dataclasses import asdict, dataclass

from .ai import Proposal


APPROVAL_FORMAT = "storyforge-approval"
APPROVAL_VERSION = 1


def proposal_fingerprint(proposal: Proposal) -> str:
    payload = {
        "role": proposal.role,
        "summary": proposal.summary,
        "operations": list(proposal.operations),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


@dataclass(frozen=True)
class Approval:
    proposal: str
    decision: str
    reviewer: str
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "format": APPROVAL_FORMAT,
            "version": APPROVAL_VERSION,
            **asdict(self),
        }


def approve(proposal: Proposal, reviewer: str, note: str = "") -> Approval:
    if not reviewer.strip():
        raise ValueError("reviewer must not be empty")
    return Approval(proposal_fingerprint(proposal), "approved", reviewer, note)


def reject(proposal: Proposal, reviewer: str, note: str = "") -> Approval:
    if not reviewer.strip():
        raise ValueError("reviewer must not be empty")
    return Approval(proposal_fingerprint(proposal), "rejected", reviewer, note)


def approval_matches(approval: Approval, proposal: Proposal) -> bool:
    return approval.proposal == proposal_fingerprint(proposal)
