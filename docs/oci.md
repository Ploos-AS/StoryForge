# OCI image

StoryForge is packaged as an Alpine-based, non-root OCI CLI image.

Build locally:

```
docker build -t storyforge .
```

Run commands with the project directory mounted at `/work`:

```
docker run --rm -v "$PWD:/work" storyforge validate story.yaml
```

For AI-backed runs, inject secrets at runtime rather than storing them in an image or provider configuration:

```
docker run --rm \
  -v "$PWD:/work" \
  -e REVIEW_API_KEY \
  storyforge run story.yaml --pipeline pipeline.yaml --providers providers.yaml -o run.json
```

The GitHub workflow builds `linux/amd64` and `linux/arm64`. Pull requests build without publishing. Pushes to main and version tags publish to GHCR.

Project files and generated editorial artifacts are external to the image. The container runs as the unprivileged `storyforge` user.
