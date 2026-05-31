from unittest.mock import patch
from click.testing import CliRunner
from xup.cli import app

runner = CliRunner()


def test_remote_add(xup_home):
    with patch("xup.commands.remote.add.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["remote", "add", "origin", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Added remote 'origin'" in result.output


def test_remote_set_url_one_arg(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.remote.set_url.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["remote", "set-url", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Set remote 'origin'" in result.output


def test_remote_set_url_two_args(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.remote.set_url.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["remote", "set-url", "upstream", "git@github.com:u/r.git"])
        assert result.exit_code == 0
        assert "Set remote 'upstream'" in result.output


def test_remote_remove(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.remote.remove.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["remote", "remove", "origin"])
        assert result.exit_code == 0
        assert "Removed remote 'origin'" in result.output


def test_remote_rename(xup_home):
    (xup_home / ".git").mkdir()
    with patch("xup.commands.remote.rename.subprocess.run") as mock_run:
        mock_run.return_value = None
        result = runner.invoke(app, ["remote", "rename", "origin", "old"])
        assert result.exit_code == 0
        assert "Renamed remote 'origin' -> 'old'" in result.output
