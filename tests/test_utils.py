"""Tests for utility functions (``xup.utils``)."""

from pathlib import Path

from xup.utils import expand, parse_remote_ref


class TestExpand:
    """Tests for ``expand``."""

    def test_expands_tilde(self):
        """``~/.zshrc`` expands to ``<home>/.zshrc``."""
        assert expand("~/.zshrc") == Path.home() / ".zshrc"

    def test_absolute_path_unchanged(self):
        """Absolute paths pass through unchanged."""
        assert expand("/etc/hosts") == Path("/etc/hosts")

    def test_relative_path_unchanged(self):
        """Relative paths pass through unchanged."""
        assert expand("foo/bar") == Path("foo/bar")


class TestParseRemoteRef:
    """Tests for ``parse_remote_ref``."""

    def test_with_branch(self):
        """Parses ``"origin@test"`` into ``("origin", "test")``."""
        remote, branch = parse_remote_ref("origin@test")
        assert remote == "origin"
        assert branch == "test"

    def test_without_branch(self):
        """Parses ``"origin"`` into ``("origin", None)``."""
        remote, branch = parse_remote_ref("origin")
        assert remote == "origin"
        assert branch is None

    def test_none(self):
        """``None`` returns ``(None, None)``."""
        remote, branch = parse_remote_ref(None)
        assert remote is None
        assert branch is None

    def test_at_in_branch_name(self):
        """Only splits on the first ``@``."""
        remote, branch = parse_remote_ref("origin@feature@demo")
        assert remote == "origin"
        assert branch == "feature@demo"
