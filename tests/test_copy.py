"""Tests for copy/apply logic (``xup.repo.XupRepoManager``)."""

from pathlib import Path

import pytest

from conftest import _make_tool
from xup.const import get_xup_repos_dir
from xup.repo import ManifestNotFoundError, XupRepoManager


def _manager_for(xup_home: Path, repo_name: str = "main") -> XupRepoManager:
    """Create a ``XupRepoManager`` pointing at *repo_name*."""
    return XupRepoManager(get_xup_repos_dir() / repo_name)


class TestApplyToolSettings:
    """Tests for ``XupRepoManager.apply_tool_settings``."""

    def test_copies_file(self, xup_home: Path):
        """Copies a declared file to the destination."""
        tool_dir = _make_tool(
            xup_home, "vscode",
            '[copy_to]\n"settings.json" = "~/dest/settings.json"\n',
        )
        (tool_dir / "settings.json").write_text("{}")

        results = _manager_for(xup_home).apply_tool_settings("vscode")
        assert len(results) == 1
        assert results[0].status == "copied"
        assert (Path.home() / "dest" / "settings.json").read_text() == "{}"

    def test_skips_missing_source(self, xup_home: Path):
        """Skips copy when the source file does not exist."""
        _make_tool(
            xup_home, "vscode",
            '[copy_to]\n"missing.txt" = "~/missing.txt"\n',
        )

        results = _manager_for(xup_home).apply_tool_settings("vscode")
        assert len(results) == 1
        assert results[0].status == "skipped"

    def test_raises_on_missing_manifest(self, xup_home: Path):
        """Raises ``ManifestNotFoundError`` for unknown tools."""
        with pytest.raises(ManifestNotFoundError):
            _manager_for(xup_home).apply_tool_settings("missing")

    def test_refuses_overwrite(self, xup_home: Path):
        """Raises ``FileExistsError`` when destination exists and *force* is off."""
        tool_dir = _make_tool(
            xup_home, "vscode",
            '[copy_to]\n"settings.json" = "~/dest/settings.json"\n',
        )
        (tool_dir / "settings.json").write_text("new")
        dest = Path.home() / "dest" / "settings.json"
        dest.parent.mkdir(parents=True)
        dest.write_text("old")

        with pytest.raises(FileExistsError):
            _manager_for(xup_home).apply_tool_settings("vscode")

    def test_force_overwrite_with_backup(self, xup_home: Path):
        """``force=True`` overwrites and creates ``.xup-backup``."""
        tool_dir = _make_tool(
            xup_home, "vscode",
            '[copy_to]\n"settings.json" = "~/dest/settings.json"\n',
        )
        (tool_dir / "settings.json").write_text("new")
        dest = Path.home() / "dest" / "settings.json"
        dest.parent.mkdir(parents=True)
        dest.write_text("old")

        results = _manager_for(xup_home).apply_tool_settings(
            "vscode", force=True,
        )
        assert dest.read_text() == "new"
        assert (Path.home() / "dest" / "settings.json.xup-backup").exists()
        backed_up = [r for r in results if r.status == "backed_up"]
        assert len(backed_up) == 1

    def test_copies_directory(self, xup_home: Path):
        """Copies an entire directory when the source is a dir."""
        tool_dir = _make_tool(
            xup_home, "nvim",
            '[copy_to]\n"config" = "~/nvim-config"\n',
        )
        (tool_dir / "config").mkdir()
        (tool_dir / "config" / "init.lua").write_text("vim.opt.number = true")

        results = _manager_for(xup_home).apply_tool_settings("nvim")
        assert len(results) == 1
        assert results[0].status == "copied"
        assert (Path.home() / "nvim-config" / "init.lua").exists()

    def test_namespaced_tool(self, xup_home: Path):
        """Applies settings for a namespaced tool ``ns/tool``."""
        tool_dir = _make_tool(
            xup_home, "bat",
            '[copy_to]\n"config" = "~/bat.conf"\n',
            ns="zzzcb",
        )
        (tool_dir / "config").write_text("theme=TwoDark")

        results = _manager_for(xup_home, repo_name="zzzcb").apply_tool_settings("bat")
        assert results[0].status == "copied"
        assert (Path.home() / "bat.conf").read_text() == "theme=TwoDark"


class TestSyncToolSettings:
    """Tests for ``XupRepoManager.sync_tool_settings``."""

    def test_syncs_file_back(self, xup_home: Path):
        """Reverse-copies a deployed file back to the repo."""
        tool_dir = _make_tool(
            xup_home, "vscode",
            '[copy_to]\n"settings.json" = "~/dest/settings.json"\n',
        )
        (tool_dir / "settings.json").write_text("original")

        dest = Path.home() / "dest" / "settings.json"
        dest.parent.mkdir(parents=True)
        dest.write_text("updated")

        results = _manager_for(xup_home).sync_tool_settings("vscode")
        assert len(results) == 1
        assert results[0].status == "copied"
        assert (tool_dir / "settings.json").read_text() == "updated"

    def test_sync_skips_missing_dest(self, xup_home: Path):
        """Skips sync when the deployed file does not exist."""
        _make_tool(
            xup_home, "vscode",
            '[copy_to]\n"missing.txt" = "~/missing.txt"\n',
        )

        results = _manager_for(xup_home).sync_tool_settings("vscode")
        assert len(results) == 1
        assert results[0].status == "skipped"
