import sys
from pathlib import Path

import click

from xup.utils import ManifestNotFoundError, apply, tool_dir


@click.command("_copy", hidden=True)
@click.argument("tool", required=False)
@click.option("--force", "-f", is_flag=True, help="Force overwrite existing files")
def cmd_copy(tool, force):
    """Copy dotfiles for a tool into place."""
    if tool is None:
        click.secho("Error: tool name is required", fg="red", err=True)
        sys.exit(1)

    try:
        results = apply(tool, force=force)
    except ManifestNotFoundError:
        click.secho(
            f"Error: setup.toml not found for '{tool}'",
            fg="red",
            err=True,
        )
        click.secho(
            f"  Expected: {tool_dir(tool) / '.xup' / 'setup.toml'}",
            err=True,
        )
        sys.exit(1)
    except FileExistsError as e:
        click.secho(f"Error: {e}", fg="red", err=True)
        sys.exit(1)

    for r in results:
        if r.status == "skipped":
            click.secho(f"  Skip: {r.message}", fg="yellow")
        elif r.status == "backed_up":
            click.secho(f"  Backup: {r.dst} -> {r.message}", fg="yellow")
        elif r.status == "copied":
            click.secho(f"  Copy: {r.src} -> {r.dst}", fg="green")
