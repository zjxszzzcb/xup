import subprocess
from pathlib import Path


def git_clone(url: str, path: Path | str):
    subprocess.run(["git", "clone", "--", url, str(path)])
