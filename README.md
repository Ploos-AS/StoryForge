# StoryForge

AI-assisted, deterministic toolchain for building narrative games.

StoryForge separates creative generation from authoritative game state. Its
engine-independent IR can describe visual novels, point-and-click adventures
and text adventures, then validate and export them to target runtimes.

## M0

M0 establishes:

- StoryForge IR v0
- Python reference CLI
- deterministic graph validation
- minimal Ren'Py exporter
- `The Lighthouse` golden example
- CI tests

No AI API key is required to build or validate a StoryForge project. AI
providers will be optional adapters above the deterministic core.

## Quick start

```sh
python -m pip install -e ".[dev]"
storyforge validate examples/lighthouse/story.yaml
storyforge export renpy examples/lighthouse/story.yaml -o build/lighthouse/script.rpy
pytest
```

See `docs/architecture.md` and `docs/ir-v0.md`.

## License

Software is licensed under the MIT License.
