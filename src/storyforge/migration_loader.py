from pathlib import Path

import yaml

from .migrations import MigrationError


def load_migrations(path: str | Path) -> list[dict]:
    root = Path(path)
    if not root.exists():
        return []
    if not root.is_dir():
        raise MigrationError(f"migration path is not a directory: {root}")

    migrations = []
    for file in sorted((*root.glob("*.yaml"), *root.glob("*.yml"))):
        data = yaml.safe_load(file.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise MigrationError(f"{file}: migration must be a mapping")
        if not isinstance(data.get("from"), str) or not isinstance(data.get("to"), str):
            raise MigrationError(f"{file}: migration requires string from/to")
        operations = data.get("operations", [])
        if not isinstance(operations, list):
            raise MigrationError(f"{file}: operations must be a list")
        migrations.append(data)
    return migrations


def validate_migrations(migrations: list[dict]) -> None:
    sources = set()
    for migration in migrations:
        source = migration.get("from")
        destination = migration.get("to")
        if source in sources:
            raise MigrationError(f"duplicate migration from version {source!r}")
        sources.add(source)
        if not source or not destination or source == destination:
            raise MigrationError(f"invalid migration edge {source!r} -> {destination!r}")
        for operation in migration.get("operations", []):
            if not isinstance(operation, dict) or len(operation) != 1:
                raise MigrationError(f"invalid migration operation: {operation!r}")
