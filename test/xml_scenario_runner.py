from __future__ import annotations

import difflib
import re
import shutil
import sys
import uuid
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
    generator: Callable[[Path, datetime | None, Callable[[str, str], str]], Path],
    expected_filename: str,
    validator: Callable[[Path], None],
) -> Path:
    """
    Execute an XML generation scenario and compare it with the expected output.

    Args:
        test_name: Name of the calling test, used to create the output folder.
        generator: Callable that receives the path where the XML should be written, timestamp, and
                  a make_document_filename function, then returns the actual path.
        expected_filename: File name of the expected XML stored under tests/expected.
        validator: Callable used to validate the generated XML against the schema.
    """

    run_root = _ensure_run_dir()
    prefix = run_root / f"Proligent_{test_name}"

    expected_path = copy_expected_file_to_out_folder(expected_filename, prefix)

    # For test mode: use static GUID from parameter
    def make_test_document_filename(static_guid: str, suffix: str) -> str:
        return f"Document_{static_guid}{suffix}"

    target_path = prefix.with_suffix(".actual.xml")
    with mock_uuid_sequence():
        actual_path = Path(generator(target_path, None, make_test_document_filename))
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
            f"See diff at {diff_path}"
        )

    # Generate a "real" XML with random GUIDs for actual use
    # For real mode: ignore static GUID parameter and generate random GUID
    def make_real_document_filename(static_guid: str, suffix: str) -> str:
        return f"Document_{uuid.uuid4()!s}{suffix}"

    start_timestamp = datetime.now()
    start_timestamp_str = start_timestamp.strftime("%Y%m%d_%H%M%S")

    # Create "real" subfolder
    real_folder = run_root / "real"
    real_folder.mkdir(parents=True, exist_ok=True)

    # Generate real XML in the "real" subfolder
    real_xml_filename = f"Proligent_{test_name}.real.{start_timestamp_str}.xml"
    real_xml_target_path = real_folder / real_xml_filename
    real_xml_path = Path(generator(real_xml_target_path, start_timestamp, make_real_document_filename))
    if not real_xml_path.exists():
        raise AssertionError(f"Generated XML not found at {real_xml_path}")
    validator(real_xml_path)

    # Extract document filenames from the XML and create dummy files
    create_dummy_documents(real_xml_path, real_folder)

    # return the test's 'actual' file path
    return actual_path


def copy_expected_file_to_out_folder(expected_filename: str, prefix: Path) -> Path:
    expected_path = EXPECTED_DIR / expected_filename
    if not expected_path.exists():
        raise AssertionError(f"Expected XML fixture '{expected_filename}' not found.")

    expected_copy = prefix.with_suffix(".expected.xml")
    shutil.copy(expected_path, expected_copy)
    return expected_path


def create_dummy_documents(xml_path: Path, output_folder: Path) -> None:
    """
    Extract document filenames from XML and create dummy files.

    Args:
        xml_path: Path to the XML file containing document references
        output_folder: Folder where dummy document files should be created
    """
    xml_content = xml_path.read_text(encoding="utf-8")

    # Extract all FileName attributes from Document elements
    # Pattern matches: FileName="Document_<guid>_<suffix>.<ext>" or FileName="CompressedDocument_<guid>_<suffix>.<ext>"
    pattern = r'FileName="((?:Compressed)?Document_[A-Fa-f0-9-]{36}[^"]+)"'
    filenames = re.findall(pattern, xml_content)

    # Create dummy files
    for filename in filenames:
        doc_path = output_folder / filename
        if not doc_path.exists():
            # Create a dummy file with minimal content
            doc_path.write_text(f"Dummy document: {filename}\nGenerated: {datetime.now()}\n", encoding="utf-8")
