import json
from pathlib import Path
from jsonschema import Draft202012Validator


def _schema_path() -> Path:
    return Path(__file__).resolve().parents[2] / "schemas" / "storyforge-v0.schema.json"


def validate_schema(story: dict) -> list[str]:
    schema = json.loads(_schema_path().read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(story), key=lambda error: list(error.path))
    return [
        "schema: " + (".".join(map(str, error.path)) + ": " if error.path else "") + error.message
        for error in errors
    ]
