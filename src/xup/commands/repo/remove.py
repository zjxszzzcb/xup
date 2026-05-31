import subprocess
import sys

import click

from xup.utils import ensure_git_repo, get_repo_dir


@click.command()
@click.argument("name")
def cmd_repo_remove(name):
    """Remove a git remote from ~/.xup."""
    ensure_git_repo()

    try:
        subprocess.run(
            ["git", "-C", str(get_repo_dir()), "remote", "remove", name],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"Error: failed to remove remote: {e}", fg="red", err=True)
        sys.exit(1)

    click.secho(f"Removed remote '{name}'", fg="green")
