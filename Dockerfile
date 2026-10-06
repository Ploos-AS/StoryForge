FROM python:3.12-alpine AS build

WORKDIR /src
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-alpine

LABEL org.opencontainers.image.title="StoryForge" \
      org.opencontainers.image.description="AI-assisted deterministic narrative game toolchain" \
      org.opencontainers.image.source="https://github.com/Ploos-AS/StoryForge" \
      org.opencontainers.image.licenses="MIT"

RUN addgroup -S storyforge && adduser -S -G storyforge storyforge
COPY --from=build /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

USER storyforge
WORKDIR /work
ENTRYPOINT ["storyforge"]
CMD ["--help"]
