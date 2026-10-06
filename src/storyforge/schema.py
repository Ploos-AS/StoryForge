import json
from importlib.resources import files

from jsonschema import Draft202012Validator


def _load_schema() -> dict:
    resource = files("storyforge").joinpath("schemas/storyforge-v0.schema.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def validate_schema(story: dict) -> list[str]:
    validator = Draft202012Validator(_load_schema())
    errors = sorted(validator.iter_errors(story), key=lambda error: list(error.path))
    return [
        "schema: " + (".".join(map(str, error.path)) + ": " if error.path else "") + error.message
        for error in errors
    ]
