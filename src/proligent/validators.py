"""
Validation utilities for Proligent data model.

This module contains validation functions used across the data model
to ensure data integrity and compliance with Proligent requirements.
"""

import os
import re


def _extract_filename(file_path: str) -> str:
    """
    Extract the filename from a path, handling both Windows and Unix separators.

    This is needed because Path.name on Unix doesn't parse Windows paths correctly.

    Args:
        file_path: The file path (can use / or \\ as separator).

    Returns:
        The filename without directory path.
    """
    # Replace backslashes with forward slashes to normalize
    normalized = file_path.replace("\\", "/")
    # Extract the last component (filename)
    return normalized.split("/")[-1]


class DocumentValidator:
    """Validator for Document-related business rules."""

    # GUID pattern matching the pattern in datawarehouse_model.py
    GUID_PATTERN = re.compile(
        r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}"
    )

    @staticmethod
    def extract_and_validate_file_name(file_name: str) -> str:
        """
        Validate that a document file name follows the expected format and extract the GUID.

        The file name must:
        1. Start with either 'Document_' or 'CompressedDocument_'
        2. Be immediately followed by a valid GUID (without braces or parentheses)
        3. Optionally contain additional characters after the GUID
        4. End with a file extension

        Args:
            file_name: The file name or path to validate.

        Returns:
            The extracted GUID from the filename.

        Raises:
            ValueError: If the file_name format is invalid or doesn't contain a valid GUID.

        Examples:
            >>> DocumentValidator.extract_and_validate_file_name(
            ...     "Document_D0C0601D-0000-0000-0000-000000000001_Report.pdf"
            ... )
            'D0C0601D-0000-0000-0000-000000000001'
            >>> DocumentValidator.extract_and_validate_file_name(
            ...     "CompressedDocument_A1B2C3D4-1111-2222-3333-444444444444.zip"
            ... )
            'A1B2C3D4-1111-2222-3333-444444444444'
        """
        # Extract just the filename without directory path
        # Use custom function to handle both Windows and Unix paths
        file_name_only = _extract_filename(file_name)

        # Expected prefixes for document files
        expected_prefixes = ["Document_", "CompressedDocument_"]

        # Check if file_name starts with one of the expected prefixes
        valid_prefix = None
        for prefix in expected_prefixes:
            if file_name_only.startswith(prefix):
                valid_prefix = prefix
                break

        if not valid_prefix:
            raise ValueError(
                f"File name must start with 'Document_' or 'CompressedDocument_': {file_name_only}"
            )

        # Extract the part after the prefix
        after_prefix = file_name_only[len(valid_prefix):]

        # Try to extract a GUID from the start of after_prefix
        match = DocumentValidator.GUID_PATTERN.match(after_prefix)
        if not match:
            raise ValueError(
                f"File name must contain a valid GUID immediately after the prefix '{valid_prefix}': {file_name_only}"
            )

        guid = match.group(0)

        # Check that there's a file extension (at least one dot followed by chars)
        if "." not in file_name_only:
            raise ValueError(f"File name must have a file extension: {file_name_only}")

        return guid


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
        # Use custom function to handle both Windows and Unix paths
        file_name_only = _extract_filename(file_name)

        if not file_name_only.startswith("Proligent_"):
            raise ValueError(f"File name must start with 'Proligent_': {file_name_only}")

        if not file_name_only.endswith(".xml"):
            raise ValueError(f"File name must end with '.xml': {file_name_only}")
