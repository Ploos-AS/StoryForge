import pytest

from storyforge.migrations import MigrationError, migrate_save
from storyforge.runtime import Session
from storyforge.save import dump_session, load_session


def story(version, scene="new_room"):
    return {
        "metadata": {"id": "demo", "version": version},
        "start": scene,
        "variables": {"points": 0},
        "scenes": {scene: {"choices": []}},
        "endings": {},
    }


def old_save():
    session = Session({
        "metadata": {"id": "demo", "version": "1.0.0"},
        "start": "old_room",
        "variables": {"score": 7},
        "inventory": ["old_key"],
        "ownership": {"coin": "old_npc"},
        "character_state": {"old_npc": {"trust": 2}},
        "scenes": {"old_room": {"choices": []}},
        "endings": {},
    })
    return dump_session(session)


def test_declarative_migration_and_load():
    migrations = [{
        "from": "1.0.0",
        "to": "1.1.0",
        "operations": [
            {"rename_scene": {"from": "old_room", "to": "new_room"}},
            {"rename_variable": {"from": "score", "to": "points"}},
            {"set_variable": {"name": "introduced", "value": True}},
            {"rename_item": {"from": "old_key", "to": "new_key"}},
            {"rename_character": {"from": "old_npc", "to": "anna"}},
        ],
    }]
    data = migrate_save(old_save(), story("1.1.0"), migrations)
    assert data["story"]["version"] == "1.1.0"
    assert data["scene"] == "new_room"
    assert data["state"]["variables"] == {"points": 7, "introduced": True}
    assert data["state"]["inventory"] == ["new_key"]
    assert data["state"]["characters"]["anna"]["trust"] == 2
    assert data["state"]["ownership"]["coin"] == "anna"
    assert load_session(story("1.1.0"), data).scene == "new_room"


def test_migrations_chain_versions():
    data = migrate_save(
        old_save(),
        story("1.2.0"),
        [
            {"from": "1.0.0", "to": "1.1.0", "operations": []},
            {"from": "1.1.0", "to": "1.2.0", "operations": [{"rename_scene": {"from": "old_room", "to": "new_room"}}]},
        ],
    )
    assert data["story"]["version"] == "1.2.0"


def test_missing_path_is_rejected():
    with pytest.raises(MigrationError):
        migrate_save(old_save(), story("2.0.0"), [])


def test_different_story_is_rejected():
    target = story("1.1.0")
    target["metadata"]["id"] = "other"
    with pytest.raises(MigrationError):
        migrate_save(old_save(), target, [])
