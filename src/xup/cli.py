import argparse
import json

from xup.repo import (
    XupRepoManager,
    add_repo,
    get_repo_and_tools,
    remove_repo,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("arg0")
    parser.add_argument("--sync", action="store_true")

    known_args, unk_args = parser.parse_known_args()
    arg0 = known_args.arg0

    if arg0 == 'repo':
        manage_repo(unk_args)

    repo_name, tool_name = arg0.rsplit("/", maxsplit=1)
    repo_manager = XupRepoManager(arg0)

    if known_args.sync:
        repo_manager.sync_tool_settings(tool_name)
    else:
        repo_manager.apply_tool_settings(tool_name)


def manage_repo(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    known_args, unk_args = parser.parse_known_args(args)

    command = known_args.command

    if command == 'add':
        add_repo(unk_args[0], unk_args[1])
    elif command == 'rm':
        remove_repo(*unk_args)
    elif command == 'ls':
        print(json.dumps(get_repo_and_tools(), indent=2))


if __name__ == "__main__":
    main()