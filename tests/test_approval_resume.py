from storyforge.ai import Proposal
from storyforge.approval import approve
from storyforge.authoring import WRITER
from storyforge.editorial import EditorialResult, EditorialStage, GateResult, StageResult, resume_editorial_pipeline
from storyforge.gates import approval_gate


def test_resume_reuses_blocked_proposal_without_provider_call():
    story = {"scenes": {"start": {"text": "Old"}}}
    proposal = Proposal("writer", "rewrite", (
        {"op": "replace", "path": ["scenes", "start", "text"], "value": "New"},
    ))
    previous = EditorialResult(
        story,
        (StageResult("draft", proposal, False, GateResult(False, "human approval required")),),
        halted=True,
    )
    stage = EditorialStage("draft", WRITER, "Rewrite.", True, approval_gate(approve(proposal, "editor")))
    result = resume_editorial_pipeline(previous, [stage], {})
    assert result.halted is False
    assert result.story["scenes"]["start"]["text"] == "New"
    assert result.stages[0].applied is True
