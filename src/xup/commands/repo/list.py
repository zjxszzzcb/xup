import subprocess
import sys

import click

from xup.utils import ensure_git_repo, get_repo_dir


@click.command("list")
def cmd_repo_list():
    """List git remotes for ~/.xup (like git remote -v)."""
    ensure_git_repo()

    try:
        subprocess.run(
            ["git", "-C", str(get_repo_dir()), "remote", "-v"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"Error: git remote list failed: {e}", fg="red", err=True)
        sys.exit(1)
