from pathlib import Path
from functools import lru_cache
import xmlschema

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


@lru_cache(maxsize=1)
def _load_schema() -> xmlschema.XMLSchema:
    schema_path = Path(__file__).resolve().parents[1] / "proligent" / "xsd" / "Datawarehouse.xsd"
    return xmlschema.XMLSchema(str(schema_path))
