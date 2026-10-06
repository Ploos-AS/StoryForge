from storyforge.design import design_metrics


def test_design_metrics_measure_structure():
    story = {
        "start": "start",
        "scenes": {
            "start": {
                "choices": [
                    {"text": "Left", "goto": "left"},
                    {"text": "Right", "ending": "quick"},
                ]
            },
            "left": {"choices": [{"text": "Finish", "ending": "slow"}]},
        },
        "endings": {"quick": {}, "slow": {}},
    }
    metrics = design_metrics(story)
    assert metrics.scenes == 2
    assert metrics.endings == 2
    assert metrics.choices == 3
    assert metrics.branching_scenes == 1
    assert metrics.average_choices_per_scene == 1.5
    assert metrics.shortest_ending_steps == 1
    assert metrics.longest_shortest_ending_steps == 2


def test_empty_story_metrics_are_safe():
    metrics = design_metrics({})
    assert metrics.scenes == 0
    assert metrics.average_choices_per_scene == 0.0
    assert metrics.shortest_ending_steps is None
