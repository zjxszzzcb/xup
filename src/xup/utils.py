"""Low-level helpers shared across xup modules."""

import subprocess
from pathlib import Path


def git_clone(url: str, path: Path | str) -> None:
    """Clone a git repository into *path*."""
    subprocess.run(["git", "clone", "--", url, str(path)])
