"""Centralized path constants for the xup runtime."""

import os
from pathlib import Path

# Directory name for tool manifests inside each tool folder.
XUP_CONFIG_DIR_NAME = ".xup"

# Root directory for all xup data; defaults to ~/.xup.
XUP_HOME = Path(os.getenv("XUP_HOME", Path.home() / XUP_CONFIG_DIR_NAME))

# All cloned repos live here.
XUP_REPOS_DIR = XUP_HOME / "repos"

__all__ = [
    "XUP_CONFIG_DIR_NAME",
    "XUP_HOME",
    "XUP_REPOS_DIR",
]