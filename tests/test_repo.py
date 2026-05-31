from unittest.mock import patch
from click.testing import CliRunner
from xup.cli import app

runner = CliRunner()


def test_repo_add_clone(xup_home):
    with patch("xup.commands.repo.add.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["repo", "add", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Cloning" in result.output


def test_repo_add_remote(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.repo.add.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["repo", "add", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Added remote 'origin'" in result.output


def test_repo_set_url_one_arg(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.repo.set_url.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["repo", "set-url", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Set remote 'origin'" in result.output


def test_repo_set_url_two_args(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.repo.set_url.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["repo", "set-url", "upstream", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Set remote 'upstream'" in result.output


def test_repo_remove(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.repo.remove.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["repo", "remove", "origin"])
        assert result.exit_code == 0
        assert "Removed remote 'origin'" in result.output


def test_repo_rename(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.repo.rename.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["repo", "rename", "origin", "old"])
        assert result.exit_code == 0
        assert "Renamed remote 'origin' -> 'old'" in result.output
