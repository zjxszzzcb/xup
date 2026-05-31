import click

from xup.commands.copy import cmd_copy
from xup.commands.repo import repo


class FallbackGroup(click.Group):
    """Route unknown args to the default copy command."""

    _GROUP_FLAGS = {"--help", "-h", "--version", "-v"}

    def parse_args(self, ctx, args):
        if not args or args[0] in self._GROUP_FLAGS:
            return super().parse_args(ctx, args)
        if not args[0].startswith("-") and args[0] in self.commands:
            return super().parse_args(ctx, args)
        args = ["_copy"] + args
        return super().parse_args(ctx, args)


@click.group(
    "xup",
    cls=FallbackGroup,
    invoke_without_command=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option("0.1.1", "-v", "--version", prog_name="xup", message="%(prog)s %(version)s")
def app():
    """Setup tool

    \b
    xup <tool>              Copy tool files into place
    xup <tool> -f           Force overwrite existing files
    """
    pass


app.add_command(cmd_copy, "_copy")
app.add_command(repo, "repo")


def main() -> None:
    app()
