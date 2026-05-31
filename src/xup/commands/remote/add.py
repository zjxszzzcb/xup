import subprocess
import sys

import click

from xup.utils import ensure_repo, get_repo_dir


@click.command()
@click.argument("name")
@click.argument("url")
def cmd_remote_add(name, url):
    """Add a git remote to ~/.xup."""
    ensure_repo()
    repo_dir = get_repo_dir()

    if not (repo_dir / ".git").exists():
        try:
            subprocess.run(["git", "init"], cwd=str(repo_dir), check=True)
        except subprocess.CalledProcessError as e:
            click.secho(f"Error: git init failed: {e}", fg="red", err=True)
            sys.exit(1)

    try:
        subprocess.run(
            ["git", "-C", str(repo_dir), "remote", "add", name, url],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"Error: failed to add remote: {e}", fg="red", err=True)
        sys.exit(1)

    click.secho(f"Added remote '{name}' -> {url}", fg="green")
