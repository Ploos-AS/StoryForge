from pathlib import Path

import pytest

from storyforge.migration_loader import load_migrations, validate_migrations
from storyforge.migrations import MigrationError


def test_loads_manifests_in_filename_order(tmp_path: Path):
    (tmp_path / "20.yaml").write_text("from: 1.1.0\nto: 1.2.0\noperations: []\n")
    (tmp_path / "10.yaml").write_text("from: 1.0.0\nto: 1.1.0\noperations: []\n")
    migrations = load_migrations(tmp_path)
    assert [m["from"] for m in migrations] == ["1.0.0", "1.1.0"]
    validate_migrations(migrations)


def test_missing_directory_is_empty(tmp_path: Path):
    assert load_migrations(tmp_path / "missing") == []


def test_duplicate_source_rejected():
    with pytest.raises(MigrationError):
        validate_migrations([
            {"from": "1.0.0", "to": "1.1.0", "operations": []},
            {"from": "1.0.0", "to": "2.0.0", "operations": []},
        ])


def test_invalid_operation_shape_rejected():
    with pytest.raises(MigrationError):
        validate_migrations([
            {"from": "1.0.0", "to": "1.1.0", "operations": [{"a": {}, "b": {}}]},
        ])
