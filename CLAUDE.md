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
uv run pytest tests/test_install.py

# Run a specific test
uv run pytest tests/test_install.py::test_copy_file -v

# Build
uv build

# Install (production)
uv tool install .
```

## Architecture

### Entry Point
`src/xup/cli.py` — Click app with `FallbackGroup` that routes `xup <tool>` to the hidden `_copy` command. Known subcommands (`pull`, `push`, `diff`, `commit`, `remote`) work normally.

### Core Flow
1. **Copy** (`utils/copy.py`) — `apply(tool, force)` loads `setup.toml` via `tomllib`, copies files/dirs to destinations; returns `list[CopyResult]`. Backs up existing files with `.xup-backup` suffix when `force=True`.
2. **Repo** (`utils/repo.py`) — `get_repo_dir()` returns `~/.xup`, `get_tools_root()` returns `~/.xup/repo`. `tool_dir(tool)` resolves to namespace-prefixed path. Functions (not constants) for testability.

### Commands (`src/xup/commands/`)
- `install` — Default command: copies tool files; `--sync` to git pull first, `--all` to copy all tools, `--force` to overwrite
- `pull` / `push` — Git wrappers with `remote@branch` syntax support
- `diff` / `commit` — Git convenience wrappers
- `remote/` — Subcommands: `add`, `list`, `remove`, `rename`, `set-url`

### Utilities (`src/xup/utils/`)
- `path.py` — `expand()` for `~` expansion
- `git.py` — `ensure_git_repo()`, remote resolution, `remote@branch` parsing
- `copy.py` — Pure function `apply()` returns `CopyResult`, no I/O side effects
- `repo.py` — Path functions and resolution

### Repository Layout
```
~/.xup/
├── repo/<namespace>/<tool>/.xup/setup.toml   # Manifest
├── repo/<namespace>/<tool>/<source_files>     # Dotfile sources
└── .git/                                       # Optional git repo
```

### Manifest Format (`setup.toml`)
```toml
[copy_to]
"source_relative_path" = "~/absolute/dest/path"
```

## Key Design Constraints
- Python 3.11+ (uses `tomllib` from stdlib)
- Only runtime dependency: `click>=8.0`
- Safety first: refuses overwrite without `-f`, creates `.xup-backup` files
- Namespaces allow multiple dotfile collections (default: `origin`)
- Utils layer is pure: no print/logging, only exceptions and return values

## Testing
Tests use pytest with real filesystem operations in temp directories. `conftest.py` provides `xup_home` fixture that monkeypatches `Path.home()`. Since `get_repo_dir()` calls `Path.home()` at runtime (not import time), the fixture provides full isolation without per-module patching. Git tests use actual `git` commands, not mocks.
