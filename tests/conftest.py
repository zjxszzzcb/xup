import pytest
from pathlib import Path
from click.testing import CliRunner
from xup.cli import app

runner = CliRunner()


def _make_tool(xup_home, tool: str, setup_text: str, ns: str = "origin"):
    """Create a minimal tool with setup.toml under xup_home."""
    p = xup_home / "repo" / ns / tool
    p.mkdir(parents=True)
    (p / ".xup").mkdir()
    (p / ".xup" / "setup.toml").write_text(setup_text)
    return p


@pytest.fixture
def xup_home(tmp_path, monkeypatch):
    """Provide an isolated xup home directory."""
    repo_dir = tmp_path / ".xup"
    repo_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return repo_dir
