import argparse
import json
from pathlib import Path
import re
import yaml

from .loader import load_story
from .migration_loader import load_migrations, validate_migrations
from .migrations import MigrationError
from .schema import validate_schema
from .validator import validate_story
from .exporters.renpy import export_renpy
from .solver import solve, unreachable_endings
from .analysis import dead_states
from .limits import StateSpaceLimitError
from .runtime import Session
from .parser import parse_command
from .approval import approve, reject, load_approval
from .editorial_run import dump_editorial_result, restore_editorial_result
from .editorial import run_editorial_pipeline, resume_editorial_pipeline
from .pipeline_config import load_pipeline_config
from .provider_config import load_provider_config
from .provider_runtime import resolve_role_providers
from .http_transport import json_post_transport


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

    vm = sub.add_parser("validate-migrations")
    vm.add_argument("directory")

    init = sub.add_parser("init")
    init.add_argument("directory")
    init.add_argument("--title", default="Untitled Story")
    init.add_argument("--id")
    init.add_argument("--version", default="0.1.0")
    init.add_argument(
        "--profile",
        choices=["visual-novel", "point-and-click", "text-adventure"],
        default="text-adventure",
    )

    play = sub.add_parser("play")
    play.add_argument("story")

    validate = sub.add_parser("validate")
    validate.add_argument("story")

    analyze = sub.add_parser("analyze")
    analyze.add_argument("story")
    analyze.add_argument("--max-states", type=int, default=10_000)

    solve_cmd = sub.add_parser("solve")
    solve_cmd.add_argument("story")
    solve_cmd.add_argument("--max-states", type=int, default=10_000)

    run = sub.add_parser("run")
    run.add_argument("story")
    run.add_argument("--pipeline", required=True)
    run.add_argument("--providers", required=True)
    run.add_argument("-o", "--output", required=True)

    resume = sub.add_parser("resume")
    resume.add_argument("run")
    resume.add_argument("--pipeline", required=True)
    resume.add_argument("--providers", required=True)
    resume.add_argument("--approval", action="append", default=[])
    resume.add_argument("-o", "--output", required=True)

    status = sub.add_parser("run-status")
    status.add_argument("run")

    review = sub.add_parser("review")
    review.add_argument("run")
    review.add_argument("stage")
    review.add_argument("decision", choices=["approve", "reject"])
    review.add_argument("--reviewer", required=True)
    review.add_argument("--note", default="")
    review.add_argument("-o", "--output", required=True)

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
        story_id = args.id or re.sub(r"[^a-z0-9._-]+", "-", args.title.casefold()).strip("-") or "story"
        template["metadata"] = {"id": story_id, "version": args.version, "title": args.title, "profile": args.profile}
        story_path.write_text(
            yaml.safe_dump(template, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(story_path)
        return 0

    if args.command == "run":
        story = load_story(args.story)
        errors = validate_schema(story) + validate_story(story)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        pipeline_data = yaml.safe_load(Path(args.pipeline).read_text(encoding="utf-8"))
        provider_data = yaml.safe_load(Path(args.providers).read_text(encoding="utf-8"))
        pipeline = load_pipeline_config(pipeline_data)
        registry = load_provider_config(provider_data)
        providers = resolve_role_providers(registry, json_post_transport)
        result = run_editorial_pipeline(story, list(pipeline.stages), providers)
        Path(args.output).write_text(
            json.dumps(dump_editorial_result(result), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(args.output)
        return 3 if result.halted else 0

    if args.command == "resume":
        previous = restore_editorial_result(
            json.loads(Path(args.run).read_text(encoding="utf-8"))
        )
        approvals = {}
        for path in args.approval:
            approval = load_approval(json.loads(Path(path).read_text(encoding="utf-8")))
            matches = [
                item.stage for item in previous.stages
                if item.proposal and approval.proposal == __import__("storyforge.approval", fromlist=["proposal_fingerprint"]).proposal_fingerprint(item.proposal)
            ]
            if len(matches) != 1:
                print(f"ERROR: approval {path} does not uniquely match a run proposal")
                return 2
            approvals[matches[0]] = approval
        pipeline_data = yaml.safe_load(Path(args.pipeline).read_text(encoding="utf-8"))
        provider_data = yaml.safe_load(Path(args.providers).read_text(encoding="utf-8"))
        pipeline = load_pipeline_config(pipeline_data, approvals)
        registry = load_provider_config(provider_data)
        providers = resolve_role_providers(registry, json_post_transport)
        result = resume_editorial_pipeline(previous, list(pipeline.stages), providers)
        Path(args.output).write_text(
            json.dumps(dump_editorial_result(result), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(args.output)
        return 3 if result.halted else 0

    if args.command in {"run-status", "review"}:
        data = json.loads(Path(args.run).read_text(encoding="utf-8"))
        run = restore_editorial_result(data)
        if args.command == "run-status":
            print(f"halted: {str(run.halted).lower()}")
            print(f"stages: {len(run.stages)}")
            for item in run.stages:
                gate = "none" if item.gate is None else ("pass" if item.gate.accepted else "fail")
                print(f"{item.stage}: applied={str(item.applied).lower()} gate={gate}")
            return 0

        matches = [item for item in run.stages if item.stage == args.stage]
        if len(matches) != 1:
            print(f"ERROR: expected exactly one stage named {args.stage!r}")
            return 2
        item = matches[0]
        artifact = (
            approve(item.proposal, args.reviewer, args.note)
            if args.decision == "approve"
            else reject(item.proposal, args.reviewer, args.note)
        )
        Path(args.output).write_text(
            json.dumps(artifact.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(args.output)
        return 0

    story = load_story(args.story)
    errors = validate_schema(story) + validate_story(story)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.command == "play":
        session = Session(story)
        while True:
            turn = session.view()
            if turn.ending is not None:
                print(turn.ending_text)
                return 0
            print(f"\
{turn.text}")
            for index, choice in enumerate(turn.choices, 1):
                print(f"  {index}. {choice}")
            if not turn.choices:
                print("No available choices.")
                return 3
            structured = session.choices()
            commands = tuple(tuple(choice.get("commands", ())) for choice in structured)
            command = parse_command(input("> "), turn.choices, commands)
            if command.kind == "choose":
                session.choose(command.choice)
            elif command.kind == "look":
                continue
            elif command.kind == "inventory":
                inventory = session.state.get("_inventory", ())
                print("Inventory: " + (", ".join(inventory) if inventory else "(empty)"))
            elif command.kind == "help":
                print("Commands: choice number/text, look, inventory, help")
            else:
                print("I don't understand that command.")

    if args.command == "validate-migrations":
        try:
            migrations = load_migrations(args.directory)
            validate_migrations(migrations)
        except MigrationError as exc:
            print(f"invalid migrations: {exc}")
            return 2
        print(f"valid migrations: {len(migrations)}")
        return 0

    if args.command == "validate":
        print("OK")
        return 0

    if args.command == "analyze":
        try:
            dead = dead_states(story, max_states=args.max_states)
        except StateSpaceLimitError as error:
            print(f"LIMIT: {error}")
            return 4
        if not dead:
            print("OK: no dead states")
            return 0
        for item in dead:
            print(f"{item.kind.upper()} [{item.scene}] {dict(item.state)}")
        return 3

    if args.command == "solve":
        try:
            solutions = solve(story, max_states=args.max_states)
        except StateSpaceLimitError as error:
            print(f"LIMIT: {error}")
            return 4
        for ending, solution in solutions.items():
            print(f"ENDING {ending}")
            for number, step in enumerate(solution.steps, 1):
                print(f"  {number}. [{step.scene}] {step.choice}")
        missing = sorted(set(story.get("endings", {})) - set(solutions))
        if missing:
            for ending in missing:
                print(f"UNREACHABLE {ending}")
            return 2
        return 0

    print(export_renpy(story, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
