from storyforge.continuity import continuity_issues


def test_clean_machine_facts_have_no_issues():
    story = {
        "characters": {"anna": {}},
        "items": {"key": {}},
        "locations": {"dock": {}},
        "ownership": {"key": "anna"},
        "character_state": {"anna": {"trust": 1}},
        "scenes": {"start": {"location": "dock", "choices": []}},
    }
    assert continuity_issues(story) == []


def test_reports_reference_and_ownership_conflicts():
    story = {
        "characters": {"anna": {}},
        "items": {"key": {}},
        "locations": {},
        "ownership": {"key": "ghost"},
        "inventory": ["key", "missing"],
        "character_state": {"missing_person": {}},
        "scenes": {"start": {"location": "nowhere", "choices": []}},
    }
    codes = {issue.code for issue in continuity_issues(story)}
    assert codes == {
        "unknown-character-state",
        "unknown-owner",
        "conflicting-item-owner",
        "unknown-inventory-item",
        "unknown-scene-location",
    }
