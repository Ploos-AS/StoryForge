import json
from pathlib import Path

import yaml

import storyforge.cli as cli


def test_run_writes_persisted_editorial_artifact(tmp_path, monkeypatch):
    story = {
        "storyforge": "0",
        "metadata": {"id": "test", "version": "0.1.0", "title": "Test", "profile": "text-adventure"},
        "start": "start",
        "characters": {},
        "locations": {},
        "items": {},
        "variables": {},
        "scenes": {"start": {"text": "Old", "choices": [{"text": "End", "ending": "end"}]}},
        "endings": {"end": {"text": "End"}},
    }
    pipeline = {
        "format": "storyforge-pipeline",
        "version": 1,
        "stages": [{"name": "draft", "role": "writer", "instruction": "Rewrite.", "apply": True}],
    }
    providers = {
        "format": "storyforge-providers",
        "version": 1,
        "providers": {"local": {"kind": "openai-compatible", "model": "test", "endpoint": "http://example.invalid"}},
        "roles": {"writer": "local"},
    }
    for name, value in (("story.yaml", story), ("pipeline.yaml", pipeline), ("providers.yaml", providers)):
        (tmp_path / name).write_text(yaml.safe_dump(value), encoding="utf-8")

    def transport(endpoint, payload, headers):
        return {"choices": [{"message": {"content": json.dumps({
            "role": "writer",
            "summary": "Rewrite",
            "operations": [{"op": "replace", "path": ["scenes", "start", "text"], "value": "New"}],
        })}}]}

    monkeypatch.setattr(cli, "json_post_transport", transport)
    output = tmp_path / "run.json"
    monkeypatch.setattr("sys.argv", [
        "storyforge", "run", str(tmp_path / "story.yaml"),
        "--pipeline", str(tmp_path / "pipeline.yaml"),
        "--providers", str(tmp_path / "providers.yaml"),
        "-o", str(output),
    ])
    assert cli.main() == 0
    artifact = json.loads(output.read_text())
    assert artifact["format"] == "storyforge-editorial-run"
    assert artifact["story"]["scenes"]["start"]["text"] == "New"
    assert artifact["stages"][0]["applied"] is True
