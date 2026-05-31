import shutil
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .path import expand
from .repo import tool_dir


@dataclass
class CopyResult:
    src: str
    dst: str
    status: str  # "copied", "skipped", "backed_up"
    message: str = ""


class ManifestNotFoundError(FileNotFoundError):
    pass


def apply(tool: str, force: bool = False) -> list[CopyResult]:
    """Load setup.toml for a tool and copy its declared files.

    Returns a list of CopyResult describing each operation.
    Raises ManifestNotFoundError if setup.toml is missing.
    Raises FileExistsError if a destination exists and force=False.
    """
    manifest_path = tool_dir(tool) / ".xup" / "setup.toml"
    if not manifest_path.exists():
        raise ManifestNotFoundError(f"setup.toml not found for '{tool}'")

    with open(manifest_path, "rb") as f:
        manifest = tomllib.load(f)

    copy_to = manifest.get("copy_to", {})
    if not copy_to:
        return []

    tool_dir_path = tool_dir(tool)
    results: list[CopyResult] = []

    for src, dst in copy_to.items():
        src_path = (tool_dir_path / src).resolve()
        dst_path = expand(dst)

        if not src_path.exists():
            results.append(CopyResult(
                src=src, dst=dst, status="skipped",
                message=f"source not found: {src_path}",
            ))
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)

        if dst_path.exists():
            if not force:
                raise FileExistsError(
                    f"Destination exists (use -f to overwrite): {dst_path}"
                )
            backup = Path(str(dst_path) + ".xup-backup")
            if backup.exists():
                if backup.is_dir():
                    shutil.rmtree(backup)
                else:
                    backup.unlink()
            shutil.move(str(dst_path), str(backup))
            results.append(CopyResult(
                src=src, dst=dst, status="backed_up",
                message=backup.name,
            ))

        if src_path.is_dir():
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
        results.append(CopyResult(src=src, dst=dst, status="copied"))

    return results
