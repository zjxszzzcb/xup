<h1 align="center">
  <code>xup</code>
</h1>

<p align="center">
  <strong>A config management and sync tool.</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#usage">Usage</a>
</p>

---

## Why xup?

Most setup tools managers try to do too much — templating engines, secret management, OS-specific branching… **xup** does one thing and does it well: it reads a tiny TOML setup file and copies your files into place. That's it.

- **Zero config** — just a `setup.toml` per tool
- **File copies** — no symlinks, no magic, just plain files where you want them
- **Safe by default** — won't overwrite existing files unless you say `-f`
- **Zero dependencies** — pure Python 3.11+ (stdlib only)

## Prerequisites

- **Python** >= 3.11
- **Git** (for `repo` commands)

## Installation

```bash
pip install xup
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install xup
```

## Quick Start

1. **Clone your dotfiles repo**:

   ```bash
   xup repo add dotfiles git@github.com:you/dotfiles.git
   ```

2. **Copy a tool into place**:

   ```bash
   xup vscode
   ```

   Done! Files declared in the tool's `setup.toml` are copied to their destinations.

## Usage

```
usage: xup [-h] [--sync] [-f] arg0

Minimal setup-tools manager

positional arguments:
  arg0           tool name (or 'repo')

options:
  --sync         pull deployed files back to repo
  -f, --force    overwrite existing files (creates .xup-backup)
  -h, --help     show this help message and exit
```

### `xup <tool>`

Reads `~/.xup/repos/<repo>/<tool>/.xup/setup.toml` and copies the declared files into place.

```bash
# Copy a single tool (from default repo "main")
xup nvim

# Force overwrite (backs up existing files to *.xup-backup)
xup nvim -f

# Specify a repo explicitly
xup dotfiles/nvim
```

### `xup <tool> --sync`

Reverse operation — pull deployed files back into the repo.

```bash
xup nvim --sync
```

### `xup repo`

Manage repos (each repo is a git clone under `~/.xup/repos/`).

```bash
# Clone a dotfiles repo
xup repo add dotfiles git@github.com:you/dotfiles.git

# List all repos and their tools
xup repo ls

# Remove a repo
xup repo rm dotfiles
```

## Manifest Format

Each tool lives in a folder inside a repo and contains a `.xup/setup.toml`:

```toml
[copy_to]
"zshrc" = "~/.zshrc"
"p10k.zsh" = "~/.p10k.zsh"
"config/alacritty" = "~/.config/alacritty"
```

| Key       | Description                                                        |
|-----------|--------------------------------------------------------------------|
| `copy_to` | Map of **source** (relative to tool dir) → **destination** (supports `~`) |

## Repository Layout

```
~/.xup/
└── repos/
    ├── dotfiles/              # A cloned git repo
    │   ├── .git/
    │   ├── nvim/
    │   │   ├── .xup/
    │   │   │   └── setup.toml
    │   │   ├── init.lua
    │   │   └── lua/
    │   │       └── plugins.lua
    │   └── vscode/
    │       ├── .xup/
    │       │   └── setup.toml
    │       └── settings.json
    └── work/                  # Another repo
        └── vscode/
            ├── .xup/
            │   └── setup.toml
            └── settings.json
```

## Source Structure

```
src/xup/
├── cli.py        # Entry point — argparse CLI
├── const.py      # Path helpers (functions for testability)
├── repo.py       # XupRepoManager, copy/sync logic, repo CRUD
└── utils.py      # expand(), git_clone(), parse_remote_ref()
```

## Development

```bash
# Clone & setup
uv venv
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/xup --cov-report=term-missing

# Build
uv build
```

## License

MIT
