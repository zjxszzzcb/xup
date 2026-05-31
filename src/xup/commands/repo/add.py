import subprocess
import sys

import click

from xup.utils import ensure_repo, get_repo_dir


@click.command()
@click.argument("url")
@click.option("-n", "--name", default="origin", help="Remote name (default: origin)")
def cmd_repo_add(url, name):
    """Add a remote or clone if repo does not exist."""
    ensure_repo()
    repo_dir = get_repo_dir()

    if not (repo_dir / ".git").exists():
        click.secho(f"Cloning {url} into {repo_dir}...", fg="cyan")
        try:
            subprocess.run(
                ["git", "clone", url, "-o", name, str(repo_dir)],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            click.secho(f"Error: git clone failed: {e}", fg="red", err=True)
            sys.exit(1)
        click.secho(f"Cloned and set remote '{name}' -> {url}", fg="green")
        return

    try:
        subprocess.run(
            ["git", "-C", str(repo_dir), "remote", "add", name, url],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"Error: failed to add remote: {e}", fg="red", err=True)
        sys.exit(1)

    click.secho(f"Added remote '{name}' -> {url}", fg="green")
