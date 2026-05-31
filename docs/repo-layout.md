# Repository Layout

xup reads the repository from `~/.xup` at runtime. You can create this directory manually, clone a Git repository into it, or use `xup repo add`.

## Directory Structure

Inside the repository, the layout looks like this:

```
repo-root/
└── repo/
    ├── <namespace-a>/
    │   ├── <tool-a>/
    │   │   ├── .xup/
    │   │   │   └── setup.toml
    │   │   └── ... (any config files)
    │   └── <tool-b>/
    │       ├── .xup/
    │       │   └── setup.toml
    │       └── ... (any config files)
    └── <namespace-b>/
        └── ...
```

At runtime the repository lives at `~/.xup`, so the paths above become `~/.xup/repo/<namespace>/<tool>/`.

## Rules

### Namespaces

- `repo/` contains one subdirectory per **namespace** (e.g. `origin`, `upstream`, or a custom name like `zzzcb`)
- The default namespace is `origin`. Running `xup <tool>` looks in `repo/origin/<tool>/`
- Use `/` to specify a namespace: `xup zzzcb/vscode` looks in `repo/zzzcb/vscode/`

### Tool Directories

- Every **immediate subdirectory** of a namespace represents a tool
- The directory name is the tool name, used as `xup <tool-name>`
- Hidden directories (names starting with `.`) are ignored

### setup.toml

Each tool directory **must** contain `.xup/setup.toml`, otherwise xup skips it.

```
vscode/
└── .xup/
    └── setup.toml    ← required
```

### Config Files

The source paths declared in `[copy_to]` should live inside the tool directory:

```
vscode/
├── .xup/
│   └── setup.toml
└── settings.json     ← source file
```

### Git Repository (Optional)

To use `xup repo`, `~/.xup` must be a Git repository:

```bash
xup repo add git@github.com:you/dotfiles.git
```

Or set up manually:

```bash
cd ~/.xup
git init
git remote add origin <your-dotfiles-repo>
```

## Full Example

A real-world dotfiles repository:

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
```

**`repo/origin/git/.xup/setup.toml`**

```toml
[copy_to]
"gitconfig" = "~/.gitconfig"
```

**`repo/origin/nvim/.xup/setup.toml`**

```toml
[copy_to]
"init.lua" = "~/.config/nvim/init.lua"
"lua" = "~/.config/nvim/lua"
```

**`repo/origin/vscode/.xup/setup.toml`**

```toml
[copy_to]
"settings.json" = "~/.config/Code/User/settings.json"
```

## Remote URL Formats

`xup repo add` accepts any URL that Git understands:

- SSH: `git@github.com:you/dotfiles.git`
- HTTPS: `https://github.com/you/dotfiles.git`
- Local path: `~/projects/dotfiles`

```bash
xup repo add git@github.com:you/dotfiles.git
```
