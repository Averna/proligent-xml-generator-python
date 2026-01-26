from __future__ import annotations

import pytest

from proligent.model import Document
from proligent.validators import DocumentValidator


def test_document_build_with_valid_document_prefix() -> None:
    """Test that build accepts valid filename with 'Document_' prefix."""
    doc_id = "D0C0601D-0000-0000-0000-000000000001"
    doc = Document(
        file_name=f"Document_{doc_id}_Report.pdf"
    )

    # Should not raise any exception
    document_type = doc.build()
    assert document_type.identifier == doc_id
    assert document_type.file_name == f"Document_{doc_id}_Report.pdf"


def test_document_build_with_valid_compressed_document_prefix() -> None:
    """Test that build accepts valid filename with 'CompressedDocument_' prefix."""
    doc_id = "A1B2C3D4-1111-2222-3333-444444444444"
    doc = Document(
        file_name=f"CompressedDocument_{doc_id}_Archive.zip"
    )

    # Should not raise any exception
    document_type = doc.build()
    assert document_type.identifier == doc_id
    assert document_type.file_name == f"CompressedDocument_{doc_id}_Archive.zip"


def test_document_build_with_full_path() -> None:
    """Test that build validates filename correctly even with full path."""
    doc_id = "D0C0601D-0000-0000-0000-000000000002"
    doc = Document(
        file_name=f"C:\\Documents\\Document_{doc_id}_Test.pdf"
    )

    # Should not raise any exception - validation uses only filename, not full path
    document_type = doc.build()
    assert document_type.identifier == doc_id


def test_document_build_with_invalid_prefix() -> None:
    """Test that build raises ValueError when filename doesn't start with correct prefix."""
    doc_id = "D0C0601D-0000-0000-0000-000000000003"
    doc = Document(
        file_name=f"InvalidPrefix_{doc_id}_Report.pdf"
    )

    with pytest.raises(ValueError, match="File name must start with 'Document_' or 'CompressedDocument_'"):
        doc.build()


def test_document_build_with_no_prefix() -> None:
    """Test that build raises ValueError when filename has no recognized prefix."""
    doc_id = "D0C0601D-0000-0000-0000-000000000004"
    doc = Document(
        file_name=f"{doc_id}_Report.pdf"
    )

    with pytest.raises(ValueError, match="File name must start with 'Document_' or 'CompressedDocument_'"):
        doc.build()


def test_document_build_with_identifier_not_after_prefix() -> None:
    """Test that build raises ValueError when GUID is not immediately after prefix."""
    doc_id = "D0C0601D-0000-0000-0000-000000000006"
    doc = Document(
        file_name=f"Document_Extra_{doc_id}_Report.pdf"
    )

    with pytest.raises(ValueError, match="File name must contain a valid GUID immediately after the prefix"):
        doc.build()


def test_document_build_with_no_extension() -> None:
    """Test that build raises ValueError when filename has no extension."""
    doc_id = "D0C0601D-0000-0000-0000-000000000007"
    doc = Document(
        file_name=f"Document_{doc_id}_Report"
    )

    with pytest.raises(ValueError, match="File name must have a file extension"):
        doc.build()


def test_document_build_with_additional_chars_between_identifier_and_extension() -> None:
    """Test that build accepts filename with additional characters between identifier and extension."""
    doc_id = "D0C0601D-0000-0000-0000-000000000008"
    doc = Document(
        file_name=f"Document_{doc_id}_Additional_Info_With_Underscores.pdf"
    )

    # Should not raise any exception
    document_type = doc.build()
    assert document_type.identifier == doc_id


def test_document_build_with_various_extensions() -> None:
    """Test that build accepts various file extensions."""
    doc_id = "D0C0601D-0000-0000-0000-000000000009"

    extensions = [".pdf", ".zip", ".txt", ".docx", ".xml", ".json", ".csv"]
    for ext in extensions:
        doc = Document(
            file_name=f"Document_{doc_id}_File{ext}"
        )

        # Should not raise any exception
        document_type = doc.build()
        assert document_type.identifier == doc_id


def test_document_build_with_compressed_document_and_additional_chars() -> None:
    """Test that build accepts CompressedDocument with additional characters."""
    doc_id = "A1B2C3D4-5555-6666-7777-888888888888"
    doc = Document(
        file_name=f"CompressedDocument_{doc_id}_v2_final.tar.gz"
    )

    # Should not raise any exception
    document_type = doc.build()
    assert document_type.identifier == doc_id


def test_document_build_with_name_and_description() -> None:
    """Test that build works correctly when name and description are provided."""
    doc_id = "D0C0601D-0000-0000-0000-000000000010"
    doc = Document(
        file_name=f"Document_{doc_id}_Report.pdf",
        name="Test Report",
        description="This is a test report"
    )

    document_type = doc.build()
    assert document_type.identifier == doc_id
    assert document_type.name == "Test Report"
    assert document_type.description == "This is a test report"


def test_document_build_with_minimal_valid_filename() -> None:
    """Test that build accepts minimal valid filename (prefix + identifier + extension)."""
    doc_id = "D0C0601D-0000-0000-0000-000000000011"
    doc = Document(
        file_name=f"Document_{doc_id}.pdf"
    )

    # Should not raise any exception
    document_type = doc.build()
    assert document_type.identifier == doc_id


# Direct validator tests
def test_validator_extracts_valid_document_guid() -> None:
    """Test that DocumentValidator.extract_and_validate_file_name extracts GUIDs correctly."""
    doc_id = "D0C0601D-0000-0000-0000-000000000012"

    # Should extract GUID from valid filenames
    extracted = DocumentValidator.extract_and_validate_file_name(f"Document_{doc_id}_Test.pdf")
    assert extracted == doc_id

    extracted = DocumentValidator.extract_and_validate_file_name(f"CompressedDocument_{doc_id}.zip")
    assert extracted == doc_id

    extracted = DocumentValidator.extract_and_validate_file_name(f"C:\\Temp\\Document_{doc_id}_Report.pdf")
    assert extracted == doc_id


def test_validator_rejects_invalid_prefix() -> None:
    """Test that DocumentValidator.extract_and_validate_file_name rejects invalid prefix."""
    doc_id = "D0C0601D-0000-0000-0000-000000000013"

    with pytest.raises(ValueError, match="File name must start with 'Document_' or 'CompressedDocument_'"):
        DocumentValidator.extract_and_validate_file_name(f"Invalid_{doc_id}.pdf")


def test_validator_rejects_missing_guid() -> None:
    """Test that DocumentValidator.extract_and_validate_file_name rejects filenames without valid GUID."""
    with pytest.raises(ValueError, match="File name must contain a valid GUID immediately after the prefix"):
        DocumentValidator.extract_and_validate_file_name("Document_NotAGuid_Report.pdf")


def test_validator_rejects_missing_extension() -> None:
    """Test that DocumentValidator.extract_and_validate_file_name rejects filenames without extension."""
    doc_id = "D0C0601D-0000-0000-0000-000000000015"

    with pytest.raises(ValueError, match="File name must have a file extension"):
        DocumentValidator.extract_and_validate_file_name(f"Document_{doc_id}")


def test_document_build_with_no_guid() -> None:
    """Test that build raises ValueError when filename doesn't contain a valid GUID."""
    doc = Document(
        file_name="Document_NotAGUID_Report.pdf"
    )

    with pytest.raises(ValueError, match="File name must contain a valid GUID immediately after the prefix"):
        doc.build()


def test_document_build_extracts_guid_case_insensitive() -> None:
    """Test that build extracts GUID with mixed case."""
    doc_id_lower = "d0c0601d-0000-0000-0000-000000000016"
    doc = Document(
        file_name=f"Document_{doc_id_lower}_Report.pdf"
    )

    document_type = doc.build()
    assert document_type.identifier == doc_id_lower

    doc_id_upper = "D0C0601D-AAAA-BBBB-CCCC-000000000017"
    doc = Document(
        file_name=f"Document_{doc_id_upper}_Report.pdf"
    )

    document_type = doc.build()
    assert document_type.identifier == doc_id_upper


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
