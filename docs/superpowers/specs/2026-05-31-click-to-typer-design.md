# Refactor xup CLI from Click to Typer

**Date:** 2026-05-31
**Status:** Draft

## Motivation

Replace Click decorators with Typer's type annotation style for a more modern, concise CLI implementation. No behavior changes — the user-facing CLI stays identical.

## Approach

**Typer callback + subcommand** (Approach A). Use Typer's `@app.callback()` to handle the default `xup <tool>` setup action, and a `repo` Typer sub-app for repository management commands.

## CLI Structure

```
xup <tool>          Setup tool files into place
xup <tool> -f       Force overwrite existing files
xup repo add <url>  Add a repository
xup repo list       List remotes
xup repo remove     Remove remote
xup repo rename     Rename remote
xup repo set-url    Set remote URL
```

## File Changes

### Delete

- `src/xup/commands/copy.py` — logic moves into `cli.py` callback

### Modify

| File | Change |
|------|--------|
| `pyproject.toml` | `click>=8.0` → `typer>=0.12`; entry point `xup.cli:main` → `xup.cli:app` |
| `src/xup/cli.py` | Replace `FallbackGroup` + Click group with Typer app + setup callback |
| `src/xup/commands/repo/__init__.py` | Replace `@click.group` with `typer.Typer` sub-app |
| `src/xup/commands/repo/add.py` | Click decorators → `Annotated` type annotations |
| `src/xup/commands/repo/list.py` | Same migration pattern |
| `src/xup/commands/repo/remove.py` | Same migration pattern |
| `src/xup/commands/repo/rename.py` | Same migration pattern |
| `src/xup/commands/repo/set_url.py` | Same migration pattern |
| `tests/test_cli.py` | `click.testing.CliRunner` → `typer.testing.CliRunner` |

### Unchanged

- `src/xup/utils/` — all utility modules remain as-is
- `tests/conftest.py`, `tests/test_copy.py`, `tests/test_repo.py`, `tests/test_utils.py` — no changes needed (they test utils, not CLI)

## Implementation Details

### cli.py

```python
import typer
from typing import Annotated

app = typer.Typer(invoke_without_command=True, add_completion=False)

@app.callback()
def setup(
    ctx: typer.Context,
    tool: Annotated[str, typer.Argument(help="Tool to setup")] = "",
    force: Annotated[bool, typer.Option("--force", "-f", help="Force overwrite")] = False,
):
    """xup — Setup tool files into place."""
    if not tool:
        typer.echo(ctx.get_help())
        raise typer.Exit()
    # Call utils/copy.apply() with tool and force
```

### commands/repo/__init__.py

```python
import typer

repo_app = typer.Typer(help="Manage the xup repository")

# Import and register subcommands
# Each subcommand file exports a function registered via @repo_app.command()
```

### Subcommand Pattern (example: add.py)

```python
from typing import Annotated
import typer

def repo_add(
    url: Annotated[str, typer.Argument(help="Repository URL")],
    namespace: Annotated[str, typer.Option("--namespace", "-n", help="Namespace")] = "main",
):
    """Clone or add a repository."""
```

### Error Handling

- Replace `click.secho(msg, fg="red", err=True)` + `sys.exit(1)` with `typer.echo(msg, err=True)` + `raise typer.Exit(1)`
- Use `raise typer.BadParameter(msg)` for argument validation errors

### Testing

- `from typer.testing import CliRunner` replaces `from click.testing import CliRunner`
- API is identical: `runner.invoke(app, ["<tool>", "-f"])`
- Existing test assertions remain valid

## Constraints

- Python 3.11+ (uses `Annotated` from stdlib `typing`)
- New runtime dependency: `typer>=0.12` (pulls in `click` and `rich`)
- No behavioral changes — all CLI interactions remain identical
- `utils/` layer is untouched (pure functions, no CLI coupling)
