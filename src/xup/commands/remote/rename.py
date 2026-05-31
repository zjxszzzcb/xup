import subprocess
import sys

import click

from xup.utils import ensure_git_repo, get_repo_dir


@click.command()
@click.argument("old")
@click.argument("new")
def cmd_remote_rename(old, new):
    """Rename a git remote in ~/.xup."""
    ensure_git_repo()

    try:
        subprocess.run(
            ["git", "-C", str(get_repo_dir()), "remote", "rename", old, new],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"Error: failed to rename remote: {e}", fg="red", err=True)
        sys.exit(1)

    click.secho(f"Renamed remote '{old}' -> '{new}'", fg="green")
