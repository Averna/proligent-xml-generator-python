"""
Validation utilities for Proligent data model.

This module contains validation functions used across the data model
to ensure data integrity and compliance with Proligent requirements.
"""

from pathlib import Path


class DocumentValidator:
    """Validator for Document-related business rules."""

    @staticmethod
    def validate_file_name(file_name: str, identifier: str) -> None:
        """
        Validate that a document file name follows the expected format.

        The file name must:
        1. Start with either 'Document_' or 'CompressedDocument_'
        2. Be immediately followed by the document's identifier
        3. Optionally contain additional characters after the identifier
        4. End with a file extension

        Args:
            file_name: The file name or path to validate.
            identifier: The document's identifier (GUID) that must appear in the file name.

        Raises:
            ValueError: If the file_name format is invalid.

        Examples:
            >>> DocumentValidator.validate_file_name(
            ...     "Document_D0C0601D-0000-0000-0000-000000000001_Report.pdf",
            ...     "D0C0601D-0000-0000-0000-000000000001"
            ... )
            >>> DocumentValidator.validate_file_name(
            ...     "CompressedDocument_A1B2C3D4-1111-2222-3333-444444444444.zip",
            ...     "A1B2C3D4-1111-2222-3333-444444444444"
            ... )
        """
        # Extract just the filename without directory path
        file_name_only = Path(file_name).name

        # Expected prefixes for document files
        expected_prefixes = ["Document_", "CompressedDocument_"]

        # Check if file_name starts with one of the expected prefixes
        valid_prefix = False
        for prefix in expected_prefixes:
            if file_name_only.startswith(prefix):
                valid_prefix = True
                # Extract the part after the prefix
                after_prefix = file_name_only[len(prefix) :]

                # Check if the identifier follows immediately after the prefix
                if not after_prefix.startswith(identifier):
                    raise ValueError(
                        f"File name must contain the document identifier '{identifier}' "
                        f"immediately after the prefix '{prefix}': {file_name_only}"
                    )
                break

        if not valid_prefix:
            raise ValueError(
                f"File name must start with 'Document_' or 'CompressedDocument_': {file_name_only}"
            )

        # Check that there's a file extension (at least one dot followed by chars)
        if "." not in file_name_only:
            raise ValueError(f"File name must have a file extension: {file_name_only}")


class FileNameValidator:
    """Validator for file name business rules."""

    @staticmethod
    def validate_xml_file_name(file_name: str) -> None:
        """
        Validate that an XML file name follows Proligent conventions.

        The file name must start with 'Proligent_' and end with '.xml'.

        Args:
            file_name: The file name or path to validate.

        Raises:
            ValueError: If the file_name format is invalid.

        Examples:
            >>> FileNameValidator.validate_xml_file_name("Proligent_test.xml")
            >>> FileNameValidator.validate_xml_file_name("C:\\\\Temp\\\\Proligent_output.xml")
        """
        # Extract just the filename without directory path
        file_name_only = Path(file_name).name

        if not file_name_only.startswith("Proligent_"):
            raise ValueError(f"File name must start with 'Proligent_': {file_name_only}")

        if not file_name_only.endswith(".xml"):
            raise ValueError(f"File name must end with '.xml': {file_name_only}")
