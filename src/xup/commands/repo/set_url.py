import subprocess
import sys

import click

from xup.utils import ensure_git_repo, get_repo_dir


@click.command("set-url")
@click.argument("name_or_url")
@click.argument("url", required=False)
def cmd_repo_set_url(name_or_url, url):
    """Set the URL of a git remote for ~/.xup."""
    ensure_git_repo()

    if url is None:
        name, url = "main", name_or_url
    else:
        name = name_or_url

    try:
        subprocess.run(
            ["git", "-C", str(get_repo_dir()), "remote", "set-url", name, url],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.secho(f"Error: failed to set remote URL: {e}", fg="red", err=True)
        sys.exit(1)

    click.secho(f"Set remote '{name}' -> {url}", fg="green")
