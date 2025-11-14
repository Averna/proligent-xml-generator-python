from __future__ import annotations

from pathlib import Path
import shutil

import pytest
import xmlschema

from proligent.xml_validate import validate_xml, validate_xml_safe

FIXTURE_DIR = Path(__file__).resolve().parent / "expected"
RESOURCE_DIR = Path(__file__).resolve().parent / "resources"


def test_validate_xml_passes_for_valid_document(tmp_path: Path) -> None:
    valid_fixture = FIXTURE_DIR / "Proligent_readme_example1.xml"
    test_file = tmp_path / "valid.xml"
    shutil.copy(valid_fixture, test_file)

    # Should not raise when XML matches the schema
    validate_xml(test_file)


def test_validate_xml_raises_for_invalid_document(tmp_path: Path) -> None:
    invalid_fixture = RESOURCE_DIR / "invalid_product_unit_missing_full_name.xml"
    test_file = tmp_path / "invalid.xml"
    shutil.copy(invalid_fixture, test_file)

    with pytest.raises(xmlschema.validators.exceptions.XMLSchemaValidationError):
        validate_xml(test_file)


def test_validate_xml_safe_returns_true_for_valid_document(tmp_path: Path) -> None:
    valid_fixture = FIXTURE_DIR / "Proligent_readme_example1.xml"
    test_file = tmp_path / "valid.xml"
    shutil.copy(valid_fixture, test_file)

    is_valid, metadata = validate_xml_safe(test_file)

    assert is_valid is True
    assert metadata is None


def test_validate_xml_safe_returns_metadata_for_invalid_document(tmp_path: Path) -> None:
    invalid_fixture = RESOURCE_DIR / "invalid_product_unit_missing_full_name.xml"
    test_file = tmp_path / "invalid.xml"
    shutil.copy(invalid_fixture, test_file)

    is_valid, metadata = validate_xml_safe(test_file)

    assert is_valid is False
    assert metadata is not None
    assert "ProductFullName" in metadata.message
    assert metadata.path == "/Proligent.Datawarehouse/ProductUnit"
    assert metadata.reason == "missing required attribute 'ProductFullName'"
