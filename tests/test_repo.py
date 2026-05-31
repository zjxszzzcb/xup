"""Tests for repo management functions (``xup.repo``)."""

from pathlib import Path
from unittest.mock import patch

from conftest import _make_tool
from xup.repo import (
    XupRepoManager,
    add_repo,
    get_repo_and_tools,
    get_repo_path,
    remove_repo,
)
from xup.const import get_xup_repos_dir


class TestGetRepoPath:
    """Tests for ``get_repo_path``."""

    def test_returns_repos_subdir(self, xup_home: Path):
        """Resolves to ``~/.xup/repos/<name>``."""
        result = get_repo_path("dotfiles")
        assert result == xup_home / "repos" / "dotfiles"


class TestAddRepo:
    """Tests for ``add_repo``."""

    def test_clones_repo(self, xup_home: Path):
        """Clones a repo under the repos directory."""
        with patch("xup.repo.git_clone") as mock_clone:
            add_repo("myrepo", "git@github.com:u/r.git")
            mock_clone.assert_called_once_with(
                "git@github.com:u/r.git",
                str(get_xup_repos_dir() / "myrepo"),
            )

    def test_rejects_duplicate(self, xup_home: Path):
        """Raises ``FileExistsError`` when the repo already exists."""
        repo_path = get_xup_repos_dir() / "existing"
        repo_path.mkdir(parents=True)

        import pytest
        with pytest.raises(FileExistsError, match="already exists"):
            add_repo("existing", "git@github.com:u/r.git")


class TestRemoveRepo:
    """Tests for ``remove_repo``."""

    def test_removes_existing_repo(self, xup_home: Path):
        """Deletes the repo directory."""
        repo_path = get_xup_repos_dir() / "to-delete"
        repo_path.mkdir(parents=True)
        (repo_path / "file.txt").write_text("data")

        removed = remove_repo("to-delete")
        assert removed == ["to-delete"]
        assert not repo_path.exists()

    def test_returns_empty_for_missing_repo(self, xup_home: Path):
        """Returns an empty list when no repos match."""
        removed = remove_repo("nonexistent")
        assert removed == []


class TestGetRepoAndTools:
    """Tests for ``get_repo_and_tools``."""

    def test_lists_repos_and_tools(self, xup_home: Path):
        """Returns ``{repo_name: [tool_names]}``."""
        _make_tool(xup_home, "vim", "", ns="dotfiles")
        _make_tool(xup_home, "bat", "", ns="dotfiles")

        result = get_repo_and_tools()
        assert "dotfiles" in result
        assert set(result["dotfiles"]) == {"vim", "bat"}

    def test_returns_empty_when_no_repos(self, xup_home: Path):
        """Returns ``{}`` when the repos directory is empty."""
        result = get_repo_and_tools()
        assert result == {}


class TestAvailableToolNames:
    """Tests for ``XupRepoManager.available_tool_names``."""

    def test_excludes_hidden_dirs(self, xup_home: Path):
        """Hidden directories (``.``, ``..``, ``.git``) are excluded."""
        repo_path = get_xup_repos_dir() / "myrepo"
        repo_path.mkdir(parents=True)
        (repo_path / "tool-a").mkdir()
        (repo_path / ".git").mkdir()
        (repo_path / ".xup").mkdir()

        manager = XupRepoManager(repo_path)
        assert manager.available_tool_names == ["tool-a"]
