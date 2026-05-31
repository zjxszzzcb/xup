import subprocess
import sys

import click

from .repo import get_repo_dir


def ensure_git_repo() -> None:
    get_repo_dir().mkdir(parents=True, exist_ok=True)
    if not (get_repo_dir() / ".git").exists():
        click.secho("Error: ~/.xup is not a git repository", fg="red", err=True)
        sys.exit(1)


def get_git_remotes() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(get_repo_dir()), "remote"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [r for r in result.stdout.strip().split("\n") if r]


def resolve_remote(name: str | None) -> str:
    if name is not None:
        return name
    remotes = get_git_remotes()
    if not remotes:
        raise ValueError("No remotes configured")
    if len(remotes) > 1:
        raise ValueError(f"Multiple remotes found: {', '.join(remotes)}. Please specify one.")
    return remotes[0]


def parse_remote_ref(ref: str | None) -> tuple[str | None, str | None]:
    """Parse a remote reference like 'origin' or 'origin@test'.
    Returns (remote_name, branch_name).
    If ref is None, returns (None, None).
    """
    if ref is None:
        return None, None
    if "@" in ref:
        remote, branch = ref.split("@", 1)
        return remote, branch
    return ref, None
