from .runtime import RuntimeError, Session


class HeadlessRuntime:
    """Transport-independent JSON-compatible facade over a StoryForge Session."""

    def __init__(self, story: dict):
        self.session = Session(story)

    def snapshot(self) -> dict:
        turn = self.session.view()
        if turn.ending is not None:
            return {
                "status": "ended",
                "scene": turn.scene,
                "ending": {"id": turn.ending, "text": turn.ending_text},
                "actions": [],
            }
        return {
            "status": "playing",
            "scene": turn.scene,
            "text": turn.text,
            "actions": [
                {
                    "id": action.id,
                    "text": action.text,
                    "commands": list(action.commands),
                }
                for action in self.session.actions()
            ],
        }

    def execute(self, choice_id: str) -> dict:
        try:
            self.session.choose_id(choice_id)
        except RuntimeError as error:
            return {
                "status": "error",
                "error": {
                    "code": "choice_not_available",
                    "message": str(error),
                },
            }
        return self.snapshot()
