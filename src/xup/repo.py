import shutil
import tomllib
from dataclasses import dataclass
from pathlib import Path

from xup.const import *
from xup.utils import git_clone


def get_repo_path(name: str) -> Path:
    return XUP_REPOS_DIR / name


def add_repo(name: str, url: str):
    """Add a remote or clone if repo does not exist."""
    repo_path = get_repo_path(name)
    if repo_path.exists():
        raise FileExistsError(f"Repo {name} already exists at: {repo_path}")

    git_clone(url, str(repo_path))


def remove_repo(*repo_names: str):
    for name in repo_names:
        repo_path = get_repo_path(name)
        if repo_path.exists():
            shutil.rmtree(repo_path)


def get_repo_and_tools() -> dict[str, list[str]]:
    available_tools: dict[str, list[str]] = {}
    for repo_path in XUP_REPOS_DIR.iterdir():
        repo_manager = XupRepoManager(repo_path)
        available_tools[repo_path.name] = repo_manager.available_tool_names
    return available_tools


@dataclass
class CopyElem:
    src: str
    dst: str


@dataclass
class SetupConfig:
    copy_to: list[CopyElem]


class XupRepoManager:
    def __init__(self, repo_root: Path | str):
        self.repo_root = Path(repo_root)

    def apply_tool_settings(self, tool_name: str):
        setup_config = self.get_tool_setup_config(tool_name)

        for copy_item in setup_config.copy_to:
            src_path = Path(copy_item.src)
            dst_path = Path(copy_item.dst)
            dst_path.mkdir(parents=True, exist_ok=True)

            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)

    def sync_tool_settings(self, tool_name: str):
        setup_config = self.get_tool_setup_config(tool_name)

        for copy_item in setup_config.copy_to:
            src_path = Path(copy_item.src)
            dst_path = Path(copy_item.dst)

            if src_path.is_dir():
                shutil.copytree(dst_path, src_path)
            else:
                shutil.copy2(dst_path, src_path)

    def get_tool_setup_config(self, tool_name: str) -> SetupConfig:
        tool_dir = self.repo_root / tool_name
        if not tool_dir.exists():
            raise ValueError()

        setup_toml = tool_dir / XUP_CONFIG_DIR_NAME / "setup.toml"
        setup_config = self.parse_setup_toml(setup_toml)

        return setup_config

    @staticmethod
    def parse_setup_toml(setup_toml: Path) -> SetupConfig:
        with open(setup_toml, "rb") as f:
            setup_configs = tomllib.load(f)

        copy_to_dict = setup_configs.get("copy_to", {}).items()
        copy_to_items = [CopyElem(src=src, dst=dst) for src, dst in copy_to_dict]

        return SetupConfig(
            copy_to=copy_to_items,
        )

    @property
    def available_tool_names(self) -> list[str]:
        tools = []
        for tool_dir in self.repo_root.iterdir():
            if tool_dir.is_dir():
                tools.append(tool_dir.name)
        return tools
