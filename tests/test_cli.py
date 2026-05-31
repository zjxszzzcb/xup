from pathlib import Path
from click.testing import CliRunner
from xup.cli import app
from conftest import _make_tool

runner = CliRunner()


def test_copy_file(xup_home):
    _make_tool(xup_home, "vscode", '[copy_to]\n"a.txt" = "~/a.txt"\n')
    (xup_home / "repo" / "main" / "vscode" / "a.txt").write_text("hi")

    result = runner.invoke(app, ["vscode"])
    assert result.exit_code == 0
    assert (Path.home() / "a.txt").read_text() == "hi"


def test_copy_missing_manifest(xup_home):
    result = runner.invoke(app, ["missing"])
    assert result.exit_code == 1
    assert "setup.toml not found" in result.output


def test_copy_namespace(xup_home):
    p = _make_tool(xup_home, "vscode", '[copy_to]\n"b.txt" = "~/b.txt"\n', ns="zzzcb")
    (p / "b.txt").write_text("ns")

    result = runner.invoke(app, ["zzzcb/vscode"])
    assert result.exit_code == 0
    assert (Path.home() / "b.txt").read_text() == "ns"


def test_copy_force(xup_home):
    _make_tool(xup_home, "vscode", '[copy_to]\n"a.txt" = "~/a.txt"\n')
    (xup_home / "repo" / "main" / "vscode" / "a.txt").write_text("new")
    (Path.home() / "a.txt").write_text("old")

    result = runner.invoke(app, ["vscode", "--force"])
    assert result.exit_code == 0
    assert (Path.home() / "a.txt").read_text() == "new"
    assert (Path.home() / "a.txt.xup-backup").exists()
