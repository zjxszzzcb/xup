"""Shared test fixtures and helpers."""

import os
from pathlib import Path

import pytest


def _make_tool(xup_home: Path, tool: str, setup_text: str, ns: str = "main") -> Path:
    """Create a minimal tool with ``setup.toml`` under *xup_home*.

    Returns the tool directory path.
    """
    p = xup_home / "repos" / ns / tool
    p.mkdir(parents=True)
    (p / ".xup").mkdir()
    (p / ".xup" / "setup.toml").write_text(setup_text)
    return p


@pytest.fixture
def xup_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Provide an isolated xup home directory.

    Sets ``XUP_HOME`` and ``HOME`` environment variables so all xup
    path helpers (``get_xup_home``, ``expand``) resolve to the temp
    directory instead of the real ``~/.xup``.
    """
    home_dir = tmp_path
    repo_dir = tmp_path / ".xup"
    repo_dir.mkdir(parents=True, exist_ok=True)

    # Set env vars for get_xup_home() and expand()
    monkeypatch.setenv("XUP_HOME", str(repo_dir))
    monkeypatch.setenv("HOME", str(home_dir))

    # Also monkeypatch Path.home() for test assertions
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home_dir))

    return repo_dir
