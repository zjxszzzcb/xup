# setup.toml Guide

Each tool declares its config files in `repo/<namespace>/<tool>/.xup/setup.toml` within the repository.

## File Location

```
repo-root/
└── repo/
    └── <namespace>/
        └── <tool>/
            └── .xup/
                └── setup.toml
```

- `<namespace>` defaults to `origin` when omitted (e.g. `xup vscode`)
- `<tool>` is the name you pass to `xup <tool>`
- At runtime xup places the repository at `~/.xup`, so the default path is `~/.xup/repo/origin/<tool>/.xup/setup.toml`

## Basic Format

`setup.toml` uses [TOML](https://toml.io). The top level contains a `[copy_to]` table:

```toml
[copy_to]
"source_file" = "destination_path"
```

- **Key (source)**: path relative to `<tool>/`
- **Value (destination)**: target path; `~` is expanded to the user's home directory

## Examples

### Copy a Single File

```toml
[copy_to]
"settings.json" = "~/.config/Code/User/settings.json"
```

Directory layout inside the repo:

```
repo-root/repo/vscode/
├── .xup/
│   └── setup.toml
└── settings.json
```

Run with:

```bash
xup vscode              # uses origin namespace
xup zzzcb/vscode        # uses zzzcb namespace
```

### Copy an Entire Directory

If the source is a directory, xup recursively copies it to the destination:

```toml
[copy_to]
"config/nvim" = "~/.config/nvim"
```

Directory layout:

```
repo-root/repo/nvim/
├── .xup/
│   └── setup.toml
└── config/
    └── nvim/
        └── init.lua
```

### Multi-file Example

```toml
[copy_to]
"settings.json" = "~/.config/Code/User/settings.json"
".zshrc" = "~/.zshrc"
".gitconfig" = "~/.gitconfig"
"config/starship.toml" = "~/.config/starship.toml"
```

## Behavior

### First Copy

xup creates parent directories as needed and copies the file or directory to the destination.

### Overwrite Protection

If the destination already exists:

- **By default**: raises an error and exits, protecting existing files
- **With `-f`**: moves the existing file/directory to `<name>.xup-backup`, then copies the new one

```bash
xup vscode -f
```

Backup examples:

```
~/.zshrc          →  ~/.zshrc.xup-backup
~/.config/nvim/   →  ~/.config/nvim.xup-backup
```

### Path Expansion Rules

- `~` is expanded to the current user's home directory (e.g. `/home/alice` or `/Users/alice`)
- Relative paths (not starting with `/` or `~`) are resolved against the current working directory; **always use `~` or absolute paths for clarity**
