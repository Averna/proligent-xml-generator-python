"""Ensure the `src` directory is available on sys.path for package imports."""

from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent
src_dir = repo_root / "src"
pkg_dir = src_dir / "proligent"

for path in (src_dir, pkg_dir):
    if path.exists():
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
