import argparse
from .loader import load_story
from .validator import validate_story
from .exporters.renpy import export_renpy


def main() -> int:
    parser = argparse.ArgumentParser(prog="storyforge")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate"); validate.add_argument("story")
    export = sub.add_parser("export"); export.add_argument("target", choices=["renpy"]); export.add_argument("story"); export.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    story = load_story(args.story)
    errors = validate_story(story)
    if errors:
        for error in errors: print(f"ERROR: {error}")
        return 1
    if args.command == "validate":
        print("OK"); return 0
    print(export_renpy(story, args.output)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
