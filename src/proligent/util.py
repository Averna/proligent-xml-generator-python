import datetime
import hashlib
from pathlib import Path
import pytz
import uuid
import xmlschema
from xsdata.models.datatype import XmlDateTime


class Util:
    """
    Convenience helpers for building Datawarehouse payloads: time formatting,
    UUID generation, and XML validation.
    """

    def __init__(
        self,
        timezone: str | datetime.tzinfo | None = None,
        destination_dir: str = r"C:\Proligent\IntegrationService\Acquisition",
        schema_path: str | Path | None = None
    ) -> None:
        """
        Configure defaults used across XML generation.

        Args:
            timezone: Time zone used when serializing naive datetimes to the
                XML ``xs:dateTime`` fields expected by the Datawarehouse model.
                Accepts a tzinfo instance or a pytz time zone name; if omitted,
                the machine's local time zone is used.
            destination_dir: Default folder where ``save_xml`` will write files,
                matching the Integration Service pickup location.
            schema_path: Optional override for the Datawarehouse XSD used when
                validating generated XML.
        """
        self.timezone = timezone
        self.destination_dir = destination_dir
        self._schema_path = (
            Path(schema_path)
            if schema_path is not None
            else Path(__file__).resolve().parents[2] / "docs" / "xsd" / "Datawarehouse.xsd"
        )
        self._schema_cache: xmlschema.XMLSchema | None = None

    def format_datetime(self, date_time: datetime = None) -> XmlDateTime:
        """
        Convert a Python ``datetime`` into the ISO-8601 string the Datawarehouse
        schema expects for timestamps.

        If ``date_time`` is naive, the configured ``timezone`` (or the machine
        time zone by default) is applied before serialization.

        Args:
            date_time: Instant to serialize; defaults to ``datetime.now()`` when
                omitted.
        """
        if date_time is None:
            date_time = datetime.datetime.now()
        if date_time.tzinfo is None or date_time.tzinfo.utcoffset(date_time) is None:
            timezone = self._resolve_timezone()
            if hasattr(timezone, "localize"):
                localized_time = timezone.localize(date_time)  # type: ignore[attr-defined]
            else:
                localized_time = date_time.replace(tzinfo=timezone)
        else:
            localized_time = date_time
        formatted_time = localized_time.isoformat()
        return formatted_time

    @staticmethod
    def _machine_timezone() -> datetime.tzinfo:
        timezone = datetime.datetime.now().astimezone().tzinfo
        if timezone is None:
            timezone = datetime.timezone.utc
        return timezone

    def _resolve_timezone(self) -> datetime.tzinfo:
        if self.timezone is None:
            return self._machine_timezone()
        if isinstance(self.timezone, str):
            return pytz.timezone(self.timezone)
        return self.timezone

    @staticmethod
    def uuid() -> str:
        """Generate a unique identifier suitable for Datawarehouse element IDs."""
        return str(uuid.uuid4())

    @staticmethod
    def get_deterministic_guid(input_text: str, encoding: str | None = None) -> str:
        """
        Generate a deterministic GUID from a string using SHA-256 and UTF-8.
        This method must be in sync with Utils.GetDeterministicGuid in ResultsProcessor.
        """
        if input_text is None:
            raise ValueError("input_text cannot be None")

        # Kept for backward compatibility with older callers; UTF-8 is always used.
        _ = encoding

        hash_bytes = hashlib.sha256(input_text.encode("utf-8")).digest()

        # Use first 16 bytes in network byte order and apply UUID v4/variant bits.
        uuid_net_order = bytearray(hash_bytes[:16])
        uuid_net_order[6] = (uuid_net_order[6] & 0x0F) | 0x40
        uuid_net_order[8] = (uuid_net_order[8] & 0x3F) | 0x80

        # Convert network-order UUID bytes to the little-endian layout expected by .NET Guid(byte[]).
        guid_bytes = bytes(
            [
                uuid_net_order[3],
                uuid_net_order[2],
                uuid_net_order[1],
                uuid_net_order[0],
                uuid_net_order[5],
                uuid_net_order[4],
                uuid_net_order[7],
                uuid_net_order[6],
                *uuid_net_order[8:16],
            ]
        )
        return str(uuid.UUID(bytes_le=guid_bytes))

    def _load_schema(self) -> xmlschema.XMLSchema:
        if self._schema_cache is None:
            self._schema_cache = xmlschema.XMLSchema(self._schema_path)
        return self._schema_cache

    def validate_xml(self, xml_file: str | Path) -> None:
        """
        Ensure an XML document is valid for the Proligent Datawarehouse schema.

        Args:
            xml_file: Path to the XML document to validate before submission.
        """
        xml_path = Path(xml_file)
        schema = self._load_schema()
        schema.validate(xml_path)


# Create a Util instance for formatting datetime and generating UUIDs.
# Can be overridden on module level if needed.
UTIL = Util()
