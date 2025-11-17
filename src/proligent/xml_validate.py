from dataclasses import dataclass
from pathlib import Path
from functools import lru_cache
import xmlschema


@dataclass(slots=True)
class ValidationFailureMetadata:
    """Metadata describing why XML schema validation failed."""

    message: str
    reason: str | None = None
    path: str | None = None
    line: int | None = None
    column: int | None = None


# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------

def validate_xml(file_path: Path | str) -> None:
    """
    Validate an XML document against the canonical DTO schema.

    Args:
        file_path: Path to the XML document to validate.

    Raises:
        xmlschema.validators.exceptions.XMLSchemaValidationError: if validation fails.
    """

    schema = _load_schema()
    xml_path = Path(file_path).resolve()
    schema.validate(str(xml_path))


def validate_xml_safe(file_path: Path | str) -> tuple[bool, ValidationFailureMetadata | None]:
    """
    Validate an XML document and return metadata instead of raising an exception.
    If there are multiple problems, it only reports the first one it finds.

    Args:
        file_path: Path to the XML document to validate.

    Returns:
        Tuple of (is_valid, metadata) where `metadata` contains contextual details
        when validation fails. Metadata is ``None`` when the XML passes validation.
    """

    try:
        validate_xml(file_path)
    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        metadata = ValidationFailureMetadata(
            message=getattr(err, "message", str(err)),
            reason=getattr(err, "reason", None),
            path=getattr(err, "path", None),
        )
        position = getattr(err, "position", None)
        if position:
            metadata.line, metadata.column = position
        return False, metadata
    return True, None


@lru_cache(maxsize=1)
def _load_schema() -> xmlschema.XMLSchema:
    schema_path = Path(__file__).resolve().parents[1] / "proligent" / "xsd" / "Datawarehouse.xsd"
    return xmlschema.XMLSchema(str(schema_path))
