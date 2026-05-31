"""CLI entry point for xup.

Dispatches ``xup <tool>`` and ``xup repo`` commands to the core logic in
:mod:`xup.repo`.
"""

import argparse
import json
import sys

from xup.repo import (
    XupRepoManager,
    add_repo,
    get_repo_and_tools,
    remove_repo,
)


def main(args: list[str] | None = None) -> None:
    """Parse top-level arguments and dispatch to the appropriate handler."""
    parser = argparse.ArgumentParser(
        prog="xup",
        description="Setup tools manager — copy config files into place.",
        usage="xup [--sync] <tool>\n       xup repo <command> [args]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="commands:\n  repo    manage repositories (add, rm, ls)",
    )
    parser.add_argument(
        "tool",
        metavar="<tool> / <command>",
        help="tool to apply (e.g. 'vscode', 'dotfiles/nvim')",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="sync local files back into the repo (reverse of apply)",
    )

    try:
        # Dispatch "repo" early so its -h/--help is not intercepted by the main parser.
        raw = args if args is not None else sys.argv[1:]
        if raw and raw[0] == "repo":
            _manage_repo(raw[1:])
            return

        known, remaining = parser.parse_known_args(args)

        # Default namespace is 'main'.
        if "/" in known.tool:
            repo_name, tool_name = known.tool.split("/", maxsplit=1)
        else:
            repo_name, tool_name = "main", known.tool

        repo_manager = XupRepoManager.from_repo_name(repo_name)

        if known.sync:
            repo_manager.sync_tool_settings(tool_name)
        else:
            repo_manager.apply_tool_settings(tool_name)
    except Exception as e:
        print(f"[Error] {e}", file=sys.stderr)
        sys.exit(1)


def _manage_repo(args: list[str]) -> None:
    """Handle ``xup repo {add|rm|ls}`` subcommands."""
    parser = argparse.ArgumentParser(
        prog="xup repo",
        description="Manage xup repositories (cloned git repos under ~/.xup/repos/).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    _sub_parser = sub.add_parser("add", help="clone a remote repo")
    _sub_parser.add_argument("name", help="local name for the repo")
    _sub_parser.add_argument("url", help="git URL to clone")

    _sub_parser = sub.add_parser("rm", help="remove one or more repos")
    _sub_parser.add_argument(
        "names",
        metavar="* names",
        nargs="+",
        help="repo name(s) to remove"
    )

    sub.add_parser("ls", help="list all repos and their tools")

    parsed = parser.parse_args(args)

    if parsed.command == "add":
        add_repo(parsed.name, parsed.url)
    elif parsed.command == "rm":
        remove_repo(*parsed.names)
    elif parsed.command == "ls":
        print(json.dumps(get_repo_and_tools(), indent=2))


if __name__ == "__main__":
    main()
