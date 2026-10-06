from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AssetSpec:
    id: str
    kind: str
    description: str
    target: str | None = None
    constraints: tuple[str, ...] = ()
    source: str | None = None


def asset_manifest(story: dict) -> dict:
    specs = []
    for asset_id, data in sorted(story.get("assets", {}).items()):
        specs.append(
            AssetSpec(
                id=asset_id,
                kind=data["kind"],
                description=data["description"],
                target=data.get("target"),
                constraints=tuple(data.get("constraints", [])),
                source=data.get("source"),
            )
        )
    return {
        "format": "storyforge-assets",
        "version": 1,
        "assets": [
            {
                **asdict(spec),
                "constraints": list(spec.constraints),
            }
            for spec in specs
        ],
    }
