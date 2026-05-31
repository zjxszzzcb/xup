import click

from .add import cmd_remote_add
from .list import cmd_remote_list
from .remove import cmd_remote_remove
from .rename import cmd_remote_rename
from .set_url import cmd_remote_set_url


@click.group(help="Manage git remotes for ~/.xup")
def remote():
    pass


remote.add_command(cmd_remote_add, "add")
remote.add_command(cmd_remote_list, "list")
remote.add_command(cmd_remote_remove, "remove")
remote.add_command(cmd_remote_rename, "rename")
remote.add_command(cmd_remote_set_url, "set-url")
