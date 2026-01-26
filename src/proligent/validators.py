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
