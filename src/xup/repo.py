"""Core domain logic: repo management, manifest parsing, and file copy/sync.

Each *repo* is a cloned git repository under ``~/.xup/repos/``.  A repo
contains one or more *tools* — sub-directories that hold a ``.xup/setup.toml``
manifest describing which files to copy into place.
"""

import shutil
import tomllib
from dataclasses import dataclass
from pathlib import Path

from xup.const import *
from xup.utils import git_clone


def get_repo_path(name: str) -> Path:
    """Return the filesystem path for a named repo."""
    return XUP_REPOS_DIR / name


def add_repo(name: str, url: str) -> None:
    """Clone *url* as a new repo named *name*.

    Raises:
        FileExistsError: if a repo with *name* already exists.
    """
    repo_path = get_repo_path(name)
    if repo_path.exists():
        raise FileExistsError(f"Repo `{name}` already exists at: {repo_path}")

    git_clone(url, str(repo_path))


def remove_repo(*repo_names: str) -> None:
    """Delete one or more repos by name.  Missing repos are silently skipped."""
    for name in repo_names:
        repo_path = get_repo_path(name)
        if repo_path.exists():
            shutil.rmtree(repo_path)


def get_repo_and_tools() -> dict[str, list[str]]:
    """Scan all repos and return a ``{repo_name: [tool_names]}`` mapping."""
    available_tools: dict[str, list[str]] = {}
    for repo_path in XUP_REPOS_DIR.iterdir():
        repo_manager = XupRepoManager(repo_path)
        available_tools[repo_path.name] = repo_manager.available_tool_names
    return available_tools


@dataclass(frozen=True)
class CopyElem:
    """A single source → destination file mapping."""

    src: str
    dst: str


@dataclass(frozen=True)
class SetupConfig:
    """Parsed representation of a ``setup.toml`` manifest."""

    copy_to: list[CopyElem]


class XupRepoManager:
    """High-level operations on a single xup repo.

    Handles manifest parsing, copying tool files into place, and syncing
    local changes back to the repo.
    """

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)

    @classmethod
    def from_repo_name(cls, repo_name: str) -> "XupRepoManager":
        """Create a manager by looking up *repo_name* in ``XUP_REPOS_DIR``."""
        return cls(get_repo_path(repo_name))

    # -- apply: repo → local filesystem --------------------------------------

    def apply_tool_settings(self, tool_name: str) -> None:
        """Copy tool files from the repo to their destinations.

        Creates parent directories as needed.  Overwrites existing files.
        """
        setup_config = self.get_tool_setup_config(tool_name)
        tool_dir = self.repo_root / tool_name

        for copy_item in setup_config.copy_to:
            src_path = tool_dir / copy_item.src
            dst_path = Path(copy_item.dst).expanduser()

            # Ensure the destination parent directory exists.
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)

    # -- sync: local filesystem → repo ---------------------------------------

    def sync_tool_settings(self, tool_name: str) -> None:
        """Pull local copies back into the repo (reverse of apply)."""
        setup_config = self.get_tool_setup_config(tool_name)
        tool_dir = self.repo_root / tool_name

        for copy_item in setup_config.copy_to:
            # Copy from the live location back into the repo checkout.
            src_path = tool_dir / copy_item.src
            dst_path = Path(copy_item.dst).expanduser()

            if src_path.is_dir():
                shutil.copytree(dst_path, src_path)
            else:
                shutil.copy2(dst_path, src_path)

    # -- manifest loading ----------------------------------------------------

    def get_tool_setup_config(self, tool_name: str) -> SetupConfig:
        """Load and parse the ``setup.toml`` for *tool_name*.

        Raises:
            ValueError: if the tool directory does not exist.
        """
        tool_dir = self.repo_root / tool_name
        if not tool_dir.exists():
            raise ValueError(f"Tool not found: {tool_name}")

        setup_toml = tool_dir / XUP_CONFIG_DIR_NAME / "setup.toml"
        return self.parse_setup_toml(setup_toml)

    @staticmethod
    def parse_setup_toml(setup_toml: Path) -> SetupConfig:
        """Parse a ``setup.toml`` file into a ``SetupConfig``."""
        with open(setup_toml, "rb") as f:
            setup_configs = tomllib.load(f)

        # The [copy_to] section maps relative source paths to absolute dests.
        copy_to_dict = setup_configs.get("copy_to", {}).items()
        copy_to_items = [CopyElem(src=src, dst=dst) for src, dst in copy_to_dict]

        return SetupConfig(copy_to=copy_to_items)

    # -- introspection -------------------------------------------------------

    @property
    def available_tool_names(self) -> list[str]:
        """Top-level sub-directories that could be tools.

        Hidden directories (e.g. ``.git``) are excluded.
        """
        tools = []
        for d in self.repo_root.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                tools.append(d.name)
        return tools
