# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

xup is a minimal setup tools manager that reads TOML manifests and copies config files into place. No symlinks, no templating — just plain file copies. Built-in git sync support.

## Commands

```bash
# Development setup
uv venv && uv pip install -e ".[dev]"

# Run CLI
python -m xup.cli -h

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_copy.py

# Run a specific test
uv run pytest tests/test_copy.py::TestApplyToolSettings::test_copies_file -v

# Run with coverage
uv run pytest --cov=src/xup --cov-report=term-missing

# Build
uv build

# Install (production)
uv tool install .
```

## Architecture

### Entry Point
`src/xup/cli.py` — argparse CLI. `main(args)` parses top-level arguments and dispatches:
- `xup <tool>` → `XupRepoManager.apply_tool_settings()`
- `xup <tool> --sync` → `XupRepoManager.sync_tool_settings()`
- `xup repo {add|rm|ls}` → repo management

### Source Structure
```
src/xup/
├── __init__.py
├── cli.py        # CLI entry point (argparse)
├── const.py      # Path helpers: get_xup_home(), get_xup_repos_dir()
├── repo.py       # XupRepoManager, CopyElem, SetupConfig, repo CRUD
└── utils.py      # expand(), git_clone(), parse_remote_ref()
```

### Core Module Details

- **`const.py`** — Functions (not constants) for testability. `get_xup_home()` checks `XUP_HOME` env var first, falls back to `Path.home() / ".xup"`.
- **`utils.py`** — Low-level helpers: `expand()` for `~` expansion, `git_clone()` with `check=True`, `parse_remote_ref()` for `remote@branch` syntax.
- **`repo.py`** — Core domain: `XupRepoManager` handles tool manifest loading, copy/sync operations, backup logic. Free functions: `add_repo()`, `remove_repo()`, `get_repo_and_tools()`, `resolve_tool_arg()`.
- **`cli.py`** — Thin CLI layer. `main(args)` accepts optional `args` list for testability. `_manage_repo(args)` handles `xup repo` subcommands.

### Repository Layout
```
~/.xup/
└── repos/
    ├── dotfiles/          # A cloned git repo (= one "repo")
    │   ├── .git/
    │   ├── nvim/
    │   │   ├── .xup/
    │   │   │   └── setup.toml
    │   │   └── init.lua
    │   └── vscode/
    │       ├── .xup/
    │       │   └── setup.toml
    │       └── settings.json
    └── work/              # Another repo
        └── git/
            ├── .xup/
            │   └── setup.toml
            └── gitconfig
```

### Manifest Format (`setup.toml`)
```toml
[copy_to]
"source_relative_path" = "~/absolute/dest/path"
```

## Key Design Constraints
- Python 3.11+ (uses `tomllib` from stdlib)
- Zero runtime dependencies (stdlib + argparse only)
- Safety first: refuses overwrite without confirmation
- Default namespace is `main` — `xup vscode` resolves to `repos/main/vscode`
- Path helpers are functions for testability (not module-level constants)
- Dataclasses use `frozen=True` for immutability

## Testing
Tests use pytest with real filesystem operations in temp directories. `conftest.py` provides `xup_home` fixture that sets `XUP_HOME` and `HOME` env vars for full isolation. The `main()` function accepts an optional `args` parameter, allowing direct invocation in tests without monkeypatching `sys.argv`.
