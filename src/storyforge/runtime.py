from dataclasses import dataclass

from .state import apply_effects, available_choices, initial_state


class RuntimeError(ValueError):
    pass


@dataclass(frozen=True)
class AvailableAction:
    id: str | None
    text: str
    commands: tuple[str, ...]


@dataclass(frozen=True)
class Turn:
    scene: str
    text: str
    choices: tuple[str, ...]
    ending: str | None = None
    ending_text: str | None = None


class Session:
    def __init__(self, story: dict):
        self.story = story
        self.scene = story["start"]
        self.state = initial_state(story)
        self.ending: str | None = None

    def view(self) -> Turn:
        if self.ending is not None:
            ending = self.story["endings"][self.ending]
            return Turn(
                scene=self.scene,
                text="",
                choices=(),
                ending=self.ending,
                ending_text=str(ending.get("text", self.ending)),
            )
        scene = self.story["scenes"][self.scene]
        choices = available_choices(scene, self.state)
        return Turn(
            scene=self.scene,
            text=str(scene.get("text", "")),
            choices=tuple(str(choice["text"]) for choice in choices),
        )

    def choices(self) -> list[dict]:
        if self.ending is not None:
            return []
        return available_choices(self.story["scenes"][self.scene], self.state)

    def actions(self) -> tuple[AvailableAction, ...]:
        return tuple(
            AvailableAction(choice.get("id"), str(choice["text"]), tuple(choice.get("commands", ())))
            for choice in self.choices()
        )

    def choose_id(self, choice_id: str) -> Turn:
        matches = [i for i, choice in enumerate(self.choices()) if choice.get("id") == choice_id]
        if len(matches) != 1:
            raise RuntimeError(f"choice id is not available: {choice_id}")
        return self.choose(matches[0])

    def choose(self, index: int) -> Turn:
        if self.ending is not None:
            raise RuntimeError("story has already ended")
        scene = self.story["scenes"][self.scene]
        choices = self.choices()
        if index < 0 or index >= len(choices):
            raise RuntimeError(f"choice index out of range: {index}")
        choice = choices[index]
        self.state = apply_effects(choice.get("effects", []), self.state)
        if choice.get("ending"):
            self.ending = choice["ending"]
        else:
            self.scene = choice["goto"]
        return self.view()
