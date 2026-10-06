# StoryForge

AI-assisted, deterministic toolchain for building narrative games.

StoryForge separates creative AI generation from authoritative game state. Its engine-independent IR supports narrative structure, deterministic state, puzzles, inventory, character state, analysis, solver-backed qualification, reviewable AI proposals, human approval gates, and reproducible editorial runs.

## 0.1.0 release candidate

The 0.1.0 line provides:

- StoryForge IR v0 with JSON Schema validation;
- deterministic state, inventory, ownership and character state;
- solver, dead-end and softlock analysis;
- deterministic text/headless runtime and save migrations;
- Ren'Py export;
- provider-neutral AI authoring roles and reviewable proposals;
- puzzle, continuity, design, asset-spec and playtest tooling;
- persisted editorial runs, approval artifacts and no-replay resume;
- declarative provider, pipeline and gate configuration;
- OpenAI-compatible/Ollama-compatible provider contract;
- `storyforge run` and `storyforge resume`;
- Alpine non-root OCI packaging for amd64/arm64;
- OCI runtime qualification and release-version gates.

No AI API key is required for deterministic validation, solving, analysis, runtime or export. AI credentials are runtime inputs only.

## Quick start

```sh
python -m pip install -e ".[dev]"
storyforge validate examples/lighthouse/story.yaml
storyforge solve examples/lighthouse/story.yaml
storyforge analyze examples/lighthouse/story.yaml
pytest
```

OCI:

```sh
docker build -t storyforge .
docker run --rm -v "$PWD:/work:ro" storyforge validate examples/lighthouse/story.yaml
```

See `docs/architecture.md`, `docs/ir-v0.md`, `docs/editorial-run-cli.md`, and `docs/oci.md`.

## License

Software is licensed under the MIT License.
