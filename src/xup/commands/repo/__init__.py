import click

from .add import cmd_repo_add
from .list import cmd_repo_list
from .remove import cmd_repo_remove
from .rename import cmd_repo_rename
from .set_url import cmd_repo_set_url


@click.group(help="Manage the xup repository")
def repo():
    pass


repo.add_command(cmd_repo_add, "add")
repo.add_command(cmd_repo_list, "list")
repo.add_command(cmd_repo_remove, "remove")
repo.add_command(cmd_repo_rename, "rename")
repo.add_command(cmd_repo_set_url, "set-url")
