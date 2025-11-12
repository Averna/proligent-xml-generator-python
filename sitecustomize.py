"""Ensure the `src` directory is available on sys.path for package imports."""

import importlib
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


def _alias_module(source: str, alias: str) -> None:
    if alias in sys.modules:
        return
    module = importlib.import_module(source)
    sys.modules[alias] = module


_alias_module("proligent.datawarehouse", "datawarehouse")
for submodule in (
    "datawarehouse",
    "datawarehouse_process_run",
    "datawarehouse_operation_run",
    "datawarehouse_sequence_run",
    "datawarehouse_step_run",
    "datawarehouse_measure",
    "datawarehouse_model",
    "datawarehouse_product_unit",
):
    _alias_module(f"proligent.datawarehouse.{submodule}", f"datawarehouse.{submodule}")

_alias_module("test.test_mocks", "test_mocks")
