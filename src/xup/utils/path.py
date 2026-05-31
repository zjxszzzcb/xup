from pathlib import Path


def expand(path: str) -> Path:
    return Path(path).expanduser()
