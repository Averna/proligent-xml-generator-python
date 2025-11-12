from __future__ import annotations

import difflib
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable

from test_mocks import mock_uuid_sequence

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

RUN_DIR: Path | None = None
EXPECTED_DIR = Path(__file__).resolve().parent / "expected"


def _ensure_run_dir() -> Path:
    global RUN_DIR
    if RUN_DIR is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        RUN_DIR = Path(__file__).resolve().parent / "out" / timestamp
        RUN_DIR.mkdir(parents=True, exist_ok=True)
    return RUN_DIR


def run_xml_scenario(
    *,
    test_name: str,
    generator: Callable[[Path, datetime | None], Path],
    expected_filename: str,
    validator: Callable[[Path], None],
) -> Path:
    """
    Execute an XML generation scenario and compare it with the expected output.

    Args:
        test_name: Name of the calling test, used to create the output folder.
        generator: Callable that receives the path where the XML should be written and returns the actual path.
        expected_filename: File name of the expected XML stored under tests/expected.
        validator: Callable used to validate the generated XML against the schema.
    """

    run_root = _ensure_run_dir()
    prefix = run_root / f"Proligent_{test_name}"

    expected_path = copy_expected_file_to_out_folder(expected_filename, prefix)

    target_path = prefix.with_suffix(".actual.xml")
    with mock_uuid_sequence():
        actual_path = Path(generator(target_path))
    if not actual_path.exists():
        raise AssertionError(f"Generated XML not found at {actual_path}")

    validator(actual_path)

    actual_text = actual_path.read_text(encoding="utf-8")
    expected_text = expected_path.read_text(encoding="utf-8")

    if actual_text != expected_text:
        diff = difflib.unified_diff(
            expected_text.splitlines(),
            actual_text.splitlines(),
            fromfile="expected",
            tofile="generated",
            lineterm="",
        )
        diff_path = prefix.with_suffix(".diff.txt")
        diff_path.write_text("\n".join(diff), encoding="utf-8")
        raise AssertionError(
            f"Generated XML does not match expected fixture '{expected_filename}'. "
            f"See {diff_path} for the generated output."
        )

    # generate a 'real' canonical file with actual random GUIDs
    # the purpose is to generate files that can be integrated in Proligent
    start_timestamp = datetime.now()
    start_timestamp_str = start_timestamp.strftime("%Y%m%d_%H%M%S")
    real_xml_target_path = prefix.with_suffix(f".real.{start_timestamp_str}.xml")
    real_xml_path = Path(generator(real_xml_target_path, start_timestamp))
    if not real_xml_path.exists():
        raise AssertionError(f"Generated XML not found at {real_xml_path}")
    validator(real_xml_path)

    # return the test's 'actual' file path
    return actual_path


def copy_expected_file_to_out_folder(expected_filename: str, prefix: Path) -> Path:
    expected_path = EXPECTED_DIR / expected_filename
    if not expected_path.exists():
        raise AssertionError(f"Expected XML fixture '{expected_filename}' not found.")

    expected_copy = prefix.with_suffix(".expected.xml")
    shutil.copy(expected_path, expected_copy)
    return expected_path
