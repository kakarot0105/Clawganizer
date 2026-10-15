"""Command-line interface for Clawganizer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .config import USER_CONFIG_PATH, ensure_user_config, load_config
from .organizer import (
    OrganizeResult,
    organize,
    summarize_by_category,
    undo_last_run,
    validate_project_name,
)
from . import workspace as ws


def _print_result(result: OrganizeResult, *, verb: str = "Moved") -> int:
    if result.moved:
        by_cat = summarize_by_category(result.moved)
        print(f"{verb} {result.move_count} item(s):")
        for category, count in by_cat.items():
            print(f"  {category}: {count}")
        print("")
        for action in result.moved[:40]:
            arrow = "→" if not action.dry_run else "⟹"
            print(f"  [{action.category}] {action.source}")
            print(f"           {arrow} {action.destination}")
        if result.move_count > 40:
            print(f"  … and {result.move_count - 40} more")
    else:
        print("Nothing to organize. Your clutter folders look clean.")

    if result.skipped:
        print(f"\nSkipped {len(result.skipped)} item(s).")
    if result.errors:
        print(f"\n{len(result.errors)} error(s):")
        for err in result.errors:
            print(f"  ! {err}")
    if result.log_path:
        print(f"\nLog: {result.log_path}")
    return 1 if result.errors else 0


def cmd_run(args: argparse.Namespace) -> int:
    """Organize the whole computer (Downloads, Desktop, …)."""
    config = load_config(Path(args.config) if args.config else None)
    if args.targets:
        # Restrict to named home subfolders for this invocation.
        config = dict(config)
        targets = {name: False for name in config.get("targets", {})}
        for name in args.targets:
            targets[name] = True
        config["targets"] = targets

    sources = None
    if args.path:
        sources = [Path(p).expanduser().resolve() for p in args.path]

    dry_run = not args.apply
    if dry_run:
        print("Dry run (pass --apply to move files).\n")
    else:
        print("Organizing your computer…\n")

    result = organize(dry_run=dry_run, config=config, sources=sources)
    return _print_result(result, verb="Would move" if dry_run else "Moved")


def cmd_undo(args: argparse.Namespace) -> int:
    result = undo_last_run(dry_run=args.dry_run)
    verb = "Would restore" if args.dry_run else "Restored"
    return _print_result(result, verb=verb)


def cmd_init_config(_args: argparse.Namespace) -> int:
    path = ensure_user_config()
    print(f"Config ready: {path}")
    print("Edit targets/folders there, then run: clawganizer run --apply")
    return 0


def cmd_show_config(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config) if args.config else None)
    print(json.dumps(config, indent=2))
    if USER_CONFIG_PATH.exists():
        print(f"\n# user config: {USER_CONFIG_PATH}", file=sys.stderr)
    else:
        print(
            f"\n# using built-in defaults (run `clawganizer init` to write {USER_CONFIG_PATH})",
            file=sys.stderr,
        )
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    config = load_config()
    from .organizer import enabled_source_dirs, plan_moves

    sources = enabled_source_dirs(config)
    planned = plan_moves(config)
    print(f"Clawganizer {__version__}")
    print(f"Home: {Path.home()}")
    print("Targets:")
    for name, enabled in config.get("targets", {}).items():
        path = Path.home() / name
        exists = "ok" if path.is_dir() else "missing"
        state = "on" if enabled else "off"
        print(f"  [{state}] {name} ({exists}) → {path}")
    print(f"Pending loose files: {len(planned)}")
    if planned:
        for category, count in summarize_by_category(planned).items():
            print(f"  {category}: {count}")
    print(f"Config: {USER_CONFIG_PATH if USER_CONFIG_PATH.exists() else '(defaults)'}")
    return 0


def cmd_ui(args: argparse.Namespace) -> int:
    from .ui import serve_ui

    serve_ui(host=args.host, port=args.port, open_browser=not args.no_browser)
    return 0


def cmd_workspace(args: argparse.Namespace) -> int:
    action = args.workspace_command
    if action == "organize":
        root = ws.organize_workspace()
        print(f"OpenClaw workspace ready: {root}")
        return 0
    if action == "list":
        active, archived = ws.list_projects()
        print("Active projects:")
        for name in active or ["(none)"]:
            print(f"  - {name}")
        print("Archived projects:")
        for name in archived or ["(none)"]:
            print(f"  - {name}")
        return 0
    if action == "create":
        name = args.name
        if not validate_project_name(name):
            print("Invalid project name. Use letters, numbers, . _ - (max 64).", file=sys.stderr)
            return 1
        try:
            path = ws.create_project(name)
        except FileExistsError:
            print(f"Project already exists: {name}", file=sys.stderr)
            return 1
        print(f"Created: {path}")
        return 0
    if action == "archive":
        try:
            path = ws.archive_project(args.name)
        except FileNotFoundError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        except FileExistsError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(f"Archived: {path}")
        return 0
    if action == "status":
        status = ws.workspace_status()
        print(f"Workspace: {status['workspace']}")
        print(f"Active: {status['active']}")
        print(f"Archived: {status['archived']}")
        return 0
    print(f"Unknown workspace command: {action}", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clawganizer",
        description="Organize your whole computer with one command.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="Organize Downloads/Desktop (and configured targets)")
    run.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files (default is dry-run)",
    )
    run.add_argument(
        "--path",
        action="append",
        help="Organize a specific folder instead of home targets (repeatable)",
    )
    run.add_argument(
        "--targets",
        nargs="+",
        metavar="NAME",
        help="Only these home folders (e.g. Downloads Desktop)",
    )
    run.add_argument("--config", help="Path to a config JSON file")
    run.set_defaults(func=cmd_run)

    undo = sub.add_parser("undo", help="Undo the last applied organize run")
    undo.add_argument("--dry-run", action="store_true", help="Show what would be restored")
    undo.set_defaults(func=cmd_undo)

    status = sub.add_parser("status", help="Show targets and pending clutter")
    status.set_defaults(func=cmd_status)

    init = sub.add_parser("init", help="Write ~/.config/clawganizer/config.json")
    init.set_defaults(func=cmd_init_config)

    show = sub.add_parser("config", help="Print effective configuration")
    show.add_argument("--config", help="Path to a config JSON file")
    show.set_defaults(func=cmd_show_config)

    ui = sub.add_parser("ui", help="Open the tornado Run UI in your browser")
    ui.add_argument("--host", default="127.0.0.1", help="Bind address (default 127.0.0.1)")
    ui.add_argument("--port", type=int, default=8765, help="Port (default 8765)")
    ui.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not auto-open a browser tab",
    )
    ui.set_defaults(func=cmd_ui)

    wsp = sub.add_parser("workspace", help="OpenClaw project workspace helpers")
    wsp_sub = wsp.add_subparsers(dest="workspace_command", required=True)
    wsp_sub.add_parser("organize", help="Create ~/.openclaw folder layout")
    wsp_sub.add_parser("list", help="List active/archived projects")
    wsp_sub.add_parser("status", help="Workspace statistics")
    create = wsp_sub.add_parser("create", help="Create an active project")
    create.add_argument("name")
    archive = wsp_sub.add_parser("archive", help="Archive an active project")
    archive.add_argument("name")
    wsp.set_defaults(func=cmd_workspace)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Bare `clawganizer` → same as `clawganizer run` (dry-run preview).
    if args.command is None:
        args = parser.parse_args(["run"])

    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
