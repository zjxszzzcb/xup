import pytest
from pathlib import Path
from xup.utils.copy import ManifestNotFoundError, apply
from conftest import _make_tool


def test_apply_copies_file(xup_home):
    _make_tool(xup_home, "vscode", '[copy_to]\n"settings.json" = "~/dest/settings.json"\n')
    (xup_home / "repo" / "origin" / "vscode" / "settings.json").write_text("{}")

    results = apply("vscode")
    assert len(results) == 1
    assert results[0].status == "copied"
    assert (Path.home() / "dest" / "settings.json").read_text() == "{}"


def test_apply_skips_missing_source(xup_home):
    _make_tool(xup_home, "vscode", '[copy_to]\n"missing.txt" = "~/missing.txt"\n')
    results = apply("vscode")
    assert len(results) == 1
    assert results[0].status == "skipped"


def test_apply_raises_on_missing_manifest(xup_home):
    with pytest.raises(ManifestNotFoundError):
        apply("missing")


def test_apply_refuses_overwrite(xup_home):
    _make_tool(xup_home, "vscode", '[copy_to]\n"settings.json" = "~/dest/settings.json"\n')
    (xup_home / "repo" / "origin" / "vscode" / "settings.json").write_text("{}")
    dest = Path.home() / "dest" / "settings.json"
    dest.parent.mkdir(parents=True)
    dest.write_text("old")

    with pytest.raises(FileExistsError):
        apply("vscode")


def test_apply_force_overwrite(xup_home):
    _make_tool(xup_home, "vscode", '[copy_to]\n"settings.json" = "~/dest/settings.json"\n')
    (xup_home / "repo" / "origin" / "vscode" / "settings.json").write_text("new")
    dest = Path.home() / "dest" / "settings.json"
    dest.parent.mkdir(parents=True)
    dest.write_text("old")

    results = apply("vscode", force=True)
    assert dest.read_text() == "new"
    assert (Path.home() / "dest" / "settings.json.xup-backup").exists()
    backed_up = [r for r in results if r.status == "backed_up"]
    assert len(backed_up) == 1
