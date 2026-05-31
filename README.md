<h1 align="center">
  <code>xup</code>
</h1>

<p align="center">
  <strong>A config management and sync tool.</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Docs</a>
</p>

---

## Why xup?

Most setup tools managers try to do too much — templating engines, secret management, OS-specific branching… **xup** does one thing and does it well: it reads a tiny TOML setup file and copies your files into place. That's it.

- **Zero config** — just a `setup.toml` per tool
- **File copies** — no symlinks, no magic, just plain files where you want them
- **Safe by default** — won't overwrite existing files unless you say `-f`

## Prerequisites

- **Python** >= 3.11
- **Git** (for sync and remote commands)

## Installation

```bash
pip install xup
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install xup
```

## Quick Start

1. **Create your dotfiles repo** (or clone an existing one into `~/.xup`):

   ```bash
   mkdir -p ~/.xup
   git init ~/.xup
   ```

2. **Add a tool** — for example, VSCode:

   ```bash
   mkdir -p ~/.xup/repo/origin/vscode/.xup
   ```

   Create `~/.xup/repo/origin/vscode/.xup/setup.toml`:

   ```toml
   [copy_to]
   "settings.json" = "~/.config/Code/User/settings.json"
   ```

   Place the actual `settings.json` next to the setup file:

   ```bash
   touch ~/.xup/repo/origin/vscode/settings.json
   ```

3. **Copy it into place**:

   ```bash
   xup vscode
   ```

   Done! `~/.config/Code/User/settings.json` is now a plain file copied from `~/.xup/repo/origin/vscode/settings.json`.

   Or use a different namespace:

   ```bash
   xup zzzcb/vscode
   ```

## Usage

```
Usage: xup [OPTIONS] COMMAND [ARGS]...

  A config management and sync tool.

  Usage:
    xup <tool>              Copy tool files into place
    xup <tool> -f           Force overwrite existing files

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  commit  Stage all changes in ~/.xup and commit.
  diff    Show changes in ~/.xup (git diff wrapper).
  pull    Pull latest changes from a remote.
  push    Push local changes to a remote.
  remote  Manage git remotes for ~/.xup.
```

### `xup <tool>`

Reads `~/.xup/repo/<namespace>/<tool>/.xup/setup.toml` and copies the declared files into place.

```bash
# Copy a single tool
xup nvim

# Force overwrite (backs up existing files to *.xup-backup)
xup nvim -f
```

### `xup pull [remote]`

Pull the latest changes from a Git remote.

```bash
# With a single remote configured, the name is optional
xup pull

# Pull a specific branch using remote@branch syntax
xup pull origin@test

# With multiple remotes, specify the name
xup pull origin
```

### `xup push [remote]`

Push local changes to a Git remote.

```bash
# With a single remote configured, the name is optional
xup push

# Push current branch to a specific remote branch
xup push origin@test

# Force push
xup push origin@test -f
```

### `xup diff [args...]`

Show pending changes in `~/.xup`. Extra arguments are forwarded to `git diff`.

```bash
xup diff
xup diff --stat
xup diff init.vim
```

### `xup commit -m <message>`

Stage all changes in `~/.xup` (`git add -A`) and commit in one step.

```bash
xup commit -m "update nvim config"
```

### `xup remote`

Manage git remotes without leaving the CLI.

```bash
xup remote add origin git@github.com:you/dotfiles.git
xup remote set-url git@github.com:you/dotfiles.git
xup remote set-url upstream git@github.com:upstream/dotfiles.git
xup remote rename origin upstream
xup remote remove upstream
```

## Documentation

- **[setup.toml Guide](docs/setup-guide.md)** — `[copy_to]` syntax, file/directory copy, backup behavior
- **[Repository Layout](docs/repo-layout.md)** — repo directory structure, Git remote URL formats, full example

## Manifest Format

Each tool lives in a folder under `repo/<namespace>/` and contains a `.xup/setup.toml`:

```toml
[copy_to]
"zshrc" = "~/.zshrc"
"p10k.zsh" = "~/.p10k.zsh"
"config/alacritty" = "~/.config/alacritty"
```

| Key      | Description                                            |
|----------|--------------------------------------------------------|
| `copy_to` | Map of **source** (relative to `repo/<namespace>/<tool>/`) → **destination** (supports `~`) |

See the [setup.toml Guide](docs/setup-guide.md) for details.

## Repository Layout

```
repo-root/
└── repo/
    ├── origin/
    │   ├── git/
    │   │   ├── .xup/
    │   │   │   └── setup.toml
    │   │   └── gitconfig
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
    └── zzzcb/
        └── vscode/
            ├── .xup/
            │   └── setup.toml
            └── settings.json
└── .git/
```

See [Repository Layout](docs/repo-layout.md) for details.

## Source Structure

```
src/xup/
├── cli.py              # Entry point — FallbackGroup + command registration
├── commands/
│   ├── install.py      # xup <tool> (copy + optional sync)
│   ├── pull.py         # xup pull
│   ├── push.py         # xup push
│   ├── diff.py         # xup diff
│   ├── commit.py       # xup commit
│   └── remote/
│       ├── __init__.py # remote subgroup registration
│       ├── add.py
│       ├── list.py
│       ├── remove.py
│       ├── rename.py
│       └── set_url.py
└── utils/
    ├── __init__.py     # Re-exports
    ├── copy.py         # File copy with backup logic (pure function)
    ├── path.py         # Path expansion helpers
    ├── repo.py         # get_repo_dir(), get_tools_root(), tool_dir()
    └── git.py          # Git remote helpers, ensure_git_repo()
```

## Development

```bash
# Clone & setup
uv venv
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run locally
python -m xup.cli -h

# Build
uv build
```

## License

MIT
