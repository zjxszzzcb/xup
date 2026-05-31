"""Tests for the CLI entry point (``xup.cli``)."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from conftest import _make_tool
from xup.cli import main


class TestToolCopy:
    """Tests for ``xup <tool>`` (apply tool settings)."""

    def test_copy_file(self, xup_home: Path, capsys: pytest.CaptureFixture[str]):
        """Copies a single file to its declared destination."""
        tool_dir = _make_tool(xup_home, "vscode", '[copy_to]\n"a.txt" = "~/a.txt"\n')
        (tool_dir / "a.txt").write_text("hi")

        main(["vscode"])
        assert (Path.home() / "a.txt").read_text() == "hi"

    def test_copy_namespace(self, xup_home: Path):
        """Copies a namespaced tool ``ns/tool``."""
        p = _make_tool(xup_home, "vscode", '[copy_to]\n"b.txt" = "~/b.txt"\n', ns="zzzcb")
        (p / "b.txt").write_text("ns")

        main(["zzzcb/vscode"])
        assert (Path.home() / "b.txt").read_text() == "ns"

    def test_copy_force_creates_backup(self, xup_home: Path):
        """Overwrites and creates a ``.xup-backup``."""
        tool_dir = _make_tool(xup_home, "vscode", '[copy_to]\n"a.txt" = "~/a.txt"\n')
        (tool_dir / "a.txt").write_text("new")
        (Path.home() / "a.txt").write_text("old")

        main(["vscode"])
        assert (Path.home() / "a.txt").read_text() == "new"
        assert (Path.home() / "a.txt.xup-backup").exists()

    def test_copy_missing_manifest(self, xup_home: Path):
        """Missing tool exits with an error."""
        with pytest.raises(SystemExit):
            main(["missing"])


class TestRepoSubcommand:
    """Tests for ``xup repo`` sub-commands."""

    def test_repo_add_clone(self, xup_home: Path):
        """``xup repo add`` clones a remote repo."""
        with patch("xup.repo.git_clone") as mock_clone:
            main(["repo", "add", "main", "git@github.com:u/r.git"])
            mock_clone.assert_called_once()

    def test_repo_add_rejects_duplicate(self, xup_home: Path):
        """``xup repo add`` rejects a repo name that already exists."""
        # Create a directory so the name collides
        from xup.const import get_xup_repos_dir
        (get_xup_repos_dir() / "main").mkdir(parents=True)

        with pytest.raises(SystemExit):
            main(["repo", "add", "main", "git@github.com:u/r.git"])

    def test_repo_rm(self, xup_home: Path):
        """``xup repo rm`` removes a repo directory."""
        _make_tool(xup_home, "test-tool", "", ns="myrepo")

        main(["repo", "rm", "myrepo"])
        assert not (xup_home / "repos" / "myrepo").exists()

    def test_repo_ls(self, xup_home: Path, capsys: pytest.CaptureFixture[str]):
        """``xup repo ls`` lists repos and their tools."""
        _make_tool(xup_home, "vim", "", ns="dotfiles")

        main(["repo", "ls"])
        output = capsys.readouterr().out
        data = json.loads(output)
        assert "dotfiles" in data
        assert "vim" in data["dotfiles"]
