import argparse
from pathlib import Path
import yaml

from .loader import load_story
from .schema import validate_schema
from .validator import validate_story
from .exporters.renpy import export_renpy
from .solver import solve, unreachable_endings
from .analysis import dead_states


TEMPLATE = {
    "storyforge": "0",
    "metadata": {"title": "Untitled Story", "profile": "text-adventure"},
    "start": "start",
    "characters": {},
    "locations": {},
    "items": {},
    "variables": {},
    "scenes": {
        "start": {
            "text": "Your story begins here.",
            "choices": [{"text": "Finish", "ending": "end"}],
        }
    },
    "endings": {"end": {"text": "The end."}},
}


def main() -> int:
    parser = argparse.ArgumentParser(prog="storyforge")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("directory")
    init.add_argument("--title", default="Untitled Story")
    init.add_argument(
        "--profile",
        choices=["visual-novel", "point-and-click", "text-adventure"],
        default="text-adventure",
    )

    validate = sub.add_parser("validate")
    validate.add_argument("story")

    analyze = sub.add_parser("analyze")
    analyze.add_argument("story")

    solve_cmd = sub.add_parser("solve")
    solve_cmd.add_argument("story")

    export = sub.add_parser("export")
    export.add_argument("target", choices=["renpy"])
    export.add_argument("story")
    export.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    if args.command == "init":
        directory = Path(args.directory)
        directory.mkdir(parents=True, exist_ok=True)
        story_path = directory / "story.yaml"
        if story_path.exists():
            print(f"ERROR: {story_path} already exists")
            return 1
        template = dict(TEMPLATE)
        template["metadata"] = {"title": args.title, "profile": args.profile}
        story_path.write_text(
            yaml.safe_dump(template, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(story_path)
        return 0

    story = load_story(args.story)
    errors = validate_schema(story) + validate_story(story)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.command == "validate":
        print("OK")
        return 0

    if args.command == "analyze":
        dead = dead_states(story)
        if not dead:
            print("OK: no dead states")
            return 0
        for item in dead:
            print(f"{item.kind.upper()} [{item.scene}] {dict(item.state)}")
        return 3

    if args.command == "solve":
        solutions = solve(story)
        for ending, solution in solutions.items():
            print(f"ENDING {ending}")
            for number, step in enumerate(solution.steps, 1):
                print(f"  {number}. [{step.scene}] {step.choice}")
        missing = unreachable_endings(story)
        if missing:
            for ending in missing:
                print(f"UNREACHABLE {ending}")
            return 2
        return 0

    print(export_renpy(story, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
