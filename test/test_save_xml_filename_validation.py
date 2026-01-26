from __future__ import annotations

from pathlib import Path
import tempfile

import pytest

from proligent.model import DataWareHouse
from proligent.validators import FileNameValidator


def test_save_xml_with_valid_filename(tmp_path: Path) -> None:
    """Test that save_xml accepts valid filenames starting with 'Proligent_' and ending with '.xml'."""
    warehouse = DataWareHouse()
    valid_file = tmp_path / "Proligent_test.xml"

    # Should not raise any exception
    warehouse.save_xml(str(valid_file))

    # Verify file was created
    assert valid_file.exists()


def test_save_xml_with_invalid_prefix(tmp_path: Path) -> None:
    """Test that save_xml raises ValueError when filename doesn't start with 'Proligent_'."""
    warehouse = DataWareHouse()
    invalid_file = tmp_path / "Test_file.xml"

    with pytest.raises(ValueError, match="File name must start with 'Proligent_'"):
        warehouse.save_xml(str(invalid_file))

    # Verify file was not created
    assert not invalid_file.exists()


def test_save_xml_with_invalid_extension(tmp_path: Path) -> None:
    """Test that save_xml raises ValueError when filename doesn't end with '.xml'."""
    warehouse = DataWareHouse()
    invalid_file = tmp_path / "Proligent_test.txt"

    with pytest.raises(ValueError, match="File name must end with '.xml'"):
        warehouse.save_xml(str(invalid_file))

    # Verify file was not created
    assert not invalid_file.exists()


def test_save_xml_with_no_prefix_no_extension(tmp_path: Path) -> None:
    """Test that save_xml raises ValueError when filename has neither correct prefix nor extension."""
    warehouse = DataWareHouse()
    invalid_file = tmp_path / "test.txt"

    # Should raise ValueError (will catch the first validation failure - missing prefix)
    with pytest.raises(ValueError, match="File name must start with 'Proligent_'"):
        warehouse.save_xml(str(invalid_file))

    # Verify file was not created
    assert not invalid_file.exists()


def test_save_xml_without_destination_generates_valid_filename() -> None:
    """Test that save_xml with no destination parameter generates a valid filename."""
    warehouse = DataWareHouse()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Override the destination_dir in UTIL to use temp directory
        import proligent.model as model_module
        original_dest = model_module.UTIL.destination_dir
        try:
            model_module.UTIL.destination_dir = temp_dir

            # Should not raise any exception
            warehouse.save_xml()

            # Verify a file was created with the correct naming pattern
            temp_path = Path(temp_dir)
            xml_files = list(temp_path.glob("Proligent_*.xml"))
            assert len(xml_files) == 1
            assert xml_files[0].name.startswith("Proligent_")
            assert xml_files[0].name.endswith(".xml")
        finally:
            # Restore original destination
            model_module.UTIL.destination_dir = original_dest


def test_save_xml_with_complex_valid_filename(tmp_path: Path) -> None:
    """Test that save_xml accepts valid filenames with complex names."""
    warehouse = DataWareHouse()
    valid_file = tmp_path / "Proligent_complex_name_123_test.xml"

    # Should not raise any exception
    warehouse.save_xml(str(valid_file))

    # Verify file was created
    assert valid_file.exists()


def test_save_xml_with_path_and_valid_filename(tmp_path: Path) -> None:
    """Test that save_xml works with full paths containing valid filename."""
    warehouse = DataWareHouse()
    subdirectory = tmp_path / "subdir"
    subdirectory.mkdir()
    valid_file = subdirectory / "Proligent_in_subdirectory.xml"

    # Should not raise any exception
    warehouse.save_xml(str(valid_file))

    # Verify file was created
    assert valid_file.exists()


# Direct validator tests
def test_filename_validator_accepts_valid_xml_filename() -> None:
    """Test that FileNameValidator.validate_xml_file_name accepts valid filenames."""
    # Should not raise for valid filenames
    FileNameValidator.validate_xml_file_name("Proligent_test.xml")
    FileNameValidator.validate_xml_file_name("Proligent_complex_name_123.xml")
    FileNameValidator.validate_xml_file_name("C:\\Temp\\Proligent_output.xml")


def test_filename_validator_rejects_invalid_prefix() -> None:
    """Test that FileNameValidator.validate_xml_file_name rejects invalid prefix."""
    with pytest.raises(ValueError, match="File name must start with 'Proligent_'"):
        FileNameValidator.validate_xml_file_name("Invalid_test.xml")


def test_filename_validator_rejects_invalid_extension() -> None:
    """Test that FileNameValidator.validate_xml_file_name rejects invalid extension."""
    with pytest.raises(ValueError, match="File name must end with '.xml'"):
        FileNameValidator.validate_xml_file_name("Proligent_test.txt")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
