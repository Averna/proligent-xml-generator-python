from __future__ import annotations

import difflib
import re
import shutil
import sys
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Tuple

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


def _extract_documents_from_xml(xml_path: Path) -> List[Tuple[str, str]]:
    """
    Extract document information from an XML file.

    Args:
        xml_path: Path to the XML file

    Returns:
        List of tuples (identifier, file_name) for each document found in the XML
    """
    documents = []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Define the namespace
        namespace = {'ns': 'http://www.averna.com/products/proligent/analytics/DIT/6.85'}

        # Find all Document elements (they can be at various levels in the XML)
        for doc_elem in root.findall('.//ns:Document', namespace):
            identifier = doc_elem.get('Identifier')
            file_name = doc_elem.get('FileName')

            if identifier and file_name:
                documents.append((identifier, file_name))

    except Exception as e:
        print(f"Warning: Could not extract documents from {xml_path}: {e}")

    return documents


def _create_dummy_document(output_folder: Path, identifier: str, file_name: str) -> None:
    """
    Create a dummy document file with the suggested filename format.

    Args:
        output_folder: Folder where the document should be created
        identifier: Document identifier (GUID)
        file_name: Original filename from the XML
    """
    # Build the suggested filename using the format from Document.suggested_document_file_name
    suggested_filename = f"Document_{identifier}_{file_name}"
    file_path = output_folder / suggested_filename

    # Create a simple dummy file with some content
    # The content identifies what document this is
    content = f"""Dummy Document File
===================

This is a placeholder document generated for testing purposes.

Document ID: {identifier}
Original Filename: {file_name}
Suggested Filename: {suggested_filename}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This file would normally contain the actual document content.
"""

    file_path.write_text(content, encoding='utf-8')


def _generate_dummy_documents_for_xml(xml_path: Path, output_folder: Path) -> None:
    """
    Extract all documents from an XML file and generate dummy document files.

    Args:
        xml_path: Path to the XML file to parse
        output_folder: Folder where dummy documents should be created
    """
    documents = _extract_documents_from_xml(xml_path)

    if not documents:
        return

    # Ensure output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)

    # Create dummy files for each document
    for identifier, file_name in documents:
        _create_dummy_document(output_folder, identifier, file_name)


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
        generator: Callable that receives the path where the XML should be written and timestamp,
                  then returns the actual path.
        expected_filename: File name of the expected XML stored under tests/expected.
        validator: Callable used to validate the generated XML against the schema.
    """

    run_root = _ensure_run_dir()
    prefix = run_root / f"Proligent_{test_name}"

    expected_path = copy_expected_file_to_out_folder(expected_filename, prefix)

    target_path = prefix.with_suffix(".actual.xml")
    with mock_uuid_sequence():
        actual_path = Path(generator(target_path, None))
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
    start_timestamp = datetime.now()
    start_timestamp_str = start_timestamp.strftime("%Y%m%d_%H%M%S")

    # Create "real" subfolder
    real_folder = run_root / "real"
    real_folder.mkdir(parents=True, exist_ok=True)

    # Generate real XML in the "real" subfolder
    real_xml_filename = f"Proligent_{test_name}.real.{start_timestamp_str}.xml"
    real_xml_target_path = real_folder / real_xml_filename
    real_xml_path = Path(generator(real_xml_target_path, start_timestamp))
    if not real_xml_path.exists():
        raise AssertionError(f"Generated XML not found at {real_xml_path}")
    validator(real_xml_path)

    # Generate dummy documents for the real XML
    _generate_dummy_documents_for_xml(real_xml_path, real_folder)

    # return the test's 'actual' file path
    return actual_path


def copy_expected_file_to_out_folder(expected_filename: str, prefix: Path) -> Path:
    expected_path = EXPECTED_DIR / expected_filename
    if not expected_path.exists():
        raise AssertionError(f"Expected XML fixture '{expected_filename}' not found.")

    expected_copy = prefix.with_suffix(".expected.xml")
    shutil.copy(expected_path, expected_copy)
    return expected_path

