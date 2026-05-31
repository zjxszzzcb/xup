import os
from pathlib import Path


XUP_CONFIG_DIR_NAME = ".xup"

XUP_HOME = Path(os.getenv("XUP_HOME", Path.home() / XUP_CONFIG_DIR_NAME))
XUP_REPOS_DIR = XUP_HOME / "repos"


__all__ = [
    "XUP_CONFIG_DIR_NAME",
    "XUP_HOME",
    "XUP_REPOS_DIR",
]