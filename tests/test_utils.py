from pathlib import Path
from xup.utils.repo import tool_dir
from xup.utils.path import expand
from xup.utils.git import parse_remote_ref


def test_tool_dir_default_namespace(xup_home):
    assert tool_dir("vscode") == xup_home / "repo" / "origin" / "vscode"


def test_tool_dir_explicit_namespace(xup_home):
    assert tool_dir("zzzcb/vscode") == xup_home / "repo" / "zzzcb" / "vscode"


def test_expand_tilde():
    assert expand("~/.zshrc") == Path.home() / ".zshrc"


def test_parse_remote_ref_with_branch():
    remote, branch = parse_remote_ref("origin@test")
    assert remote == "origin"
    assert branch == "test"


def test_parse_remote_ref_without_branch():
    remote, branch = parse_remote_ref("origin")
    assert remote == "origin"
    assert branch is None


def test_parse_remote_ref_none():
    remote, branch = parse_remote_ref(None)
    assert remote is None
    assert branch is None
