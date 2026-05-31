from pathlib import Path

DEFAULT_NS = "origin"


def get_repo_dir() -> Path:
    return Path.home() / ".xup"


def get_tools_root() -> Path:
    return get_repo_dir() / "repo"


def ensure_repo() -> None:
    get_repo_dir().mkdir(parents=True, exist_ok=True)


def tool_dir(tool: str) -> Path:
    if "/" in tool:
        return get_tools_root() / tool
    return get_tools_root() / DEFAULT_NS / tool
