# Release and version contract

StoryForge has one package version: `project.version` in `pyproject.toml`.

The installed CLI exposes exactly that version:

```
storyforge --version
```

A version release tag must be `v<project.version>`. The release-contract workflow rejects a tag whose version differs from the Python package.

The OCI workflow already derives version tags from Git refs. Combining the two contracts means a successful `vX.Y.Z` release has the same semantic version in the Python package, CLI, Git tag, and OCI tag.

Development pushes to `main` may still publish the moving `main` and SHA OCI tags. Immutable version tags are created only from matching Git version tags.
