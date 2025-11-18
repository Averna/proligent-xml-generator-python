import datetime
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
import pytz
from typing import Any, List
import uuid
from xml.etree import ElementTree as ET
import xmlschema
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse import ProligentDatawarehouse
from proligent.datawarehouse.datawarehouse_process_run import ProcessRunType
from proligent.datawarehouse.datawarehouse_operation_run import OperationRunType
from proligent.datawarehouse.datawarehouse_sequence_run import SequenceRunType
from proligent.datawarehouse.datawarehouse_step_run import StepRunType
from proligent.datawarehouse.datawarehouse_measure import MeasureType
from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    DocumentType,
    ExecutionStatusKind as _ExecutionStatusKind,
    MeasureKind as _MeasureKind,
)
from proligent.datawarehouse.datawarehouse_product_unit import ProductUnitType

# Re-export ExecutionStatusKind so callers can import it from this namespace.
ExecutionStatusKind = _ExecutionStatusKind
MeasureKind = _MeasureKind


class Util:
    """
    Convenience helpers for building Datawarehouse payloads: time formatting,
    UUID generation, and XML validation.
    """
    def __init__(
        self,
        timezone: str | datetime.tzinfo | None = None,
        destination_dir: str = r"C:\Proligent\IntegrationService\Acquisition",
        schema_path: str | Path | None = None,
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


class Buildable:
    """
    Base class for objects that can produce Datawarehouse DTOs and XML payloads.
    """
    def build(self) -> Any:
        """
        Create the xsdata dataclass instance that mirrors the Datawarehouse
        schema element for this object.
        """
        return None

    def to_xml(self) -> str:
        """
        Serialize the built dataclass to an XML string ready for Proligent
        ingestion.
        """
        # Initialize the context, parser, and serializer
        context = XmlContext()
        serializer = XmlSerializer(context=context)

        # Serialize the dataclass instance to an XML string
        return serializer.render(self.build())

    def save_xml(self, destination: str = ''):
        """
        Write the XML representation to disk.

        If ``destination`` is not provided, the file is placed in the default
        Integration Service pickup directory with a generated name.
        """
        if destination == '':
            folder = Path(UTIL.destination_dir)
            name = 'Proligent_' + UTIL.uuid() + '.xml'
            destination: Path = folder / name
        else:
            destination = Path(destination)
        xml_string = self.to_xml()
        root = ET.fromstring(xml_string)
        if root.tag.startswith("{"):
            namespace = root.tag.split("}", 1)[0][1:]
            ET.register_namespace("", namespace)
        ET.indent(root, space='  ')
        tree = ET.ElementTree(root)
        with destination.open('wb') as file:
            tree.write(file, encoding='utf-8', xml_declaration=True)


class LimitExpression(Enum):
    """
    Expressions that describe how numeric limits should be interpreted when
    attached to a measurement value in the Datawarehouse model.
    """
    LOWERBOUND_LEQ_X_LEQ_HIGHER_BOUND = "LOWERBOUND <= X <= HIGHERBOUND"
    LOWERBOUND_LE_X_LEQ_HIGHER_BOUND = "LOWERBOUND < X <= HIGHERBOUND"
    LOWERBOUND_LEQ_X_LE_HIGHER_BOUND = "LOWERBOUND <= X < HIGHERBOUND"
    LOWERBOUND_LE_X_LE_HIGHER_BOUND = "LOWERBOUND < X < HIGHERBOUND"
    LOWERBOUND_LEQ_X = "LOWERBOUND <= X"
    LOWERBOUND_LE_X = "LOWERBOUND < X"
    X_LEQ_HIGHER_BOUND = "X <= HIGHERBOUND"
    X_LE_HIGHER_BOUND = "X < HIGHERBOUND"
    X_EQ_HIGHER_BOUND = "X == HIGHERBOUND"
    X_NEQ_HIGHER_BOUND = "X != HIGHERBOUND"
    X_LEQ_LOWERBOUND_OR_HIGHERBOUND_LEQ_X = "X <= LOWERBOUND OR HIGHERBOUND <= X"
    X_LE_LOWERBOUND_or_HIGHERBOUND_LEQ_X = "X < LOWERBOUND or HIGHERBOUND <= X"
    X_LEQ_LOWERBOUND_or_HIGHERBOUND_LE_X = "X <= LOWERBOUND or HIGHERBOUND < X"
    X_LE_LOWERBOUND_or_HIGHERBOUND_LE_X = "X < LOWERBOUND or HIGHERBOUND < X"


@dataclass
class Limit:
    """
    Numeric boundaries that accompany a measurement in the Datawarehouse model.

    The provided ``expression`` determines how ``lower_bound`` and
    ``higher_bound`` are compared against the measured value.
    """
    expression: LimitExpression
    lower_bound: Any = field(default='')
    higher_bound: Any = field(default='')

    def __str__(self) -> str:
        """Render the expression string with the current bounds inserted."""
        return self.expression.value.replace('LOWERBOUND', str(self.lower_bound)).replace('HIGHERBOUND', str(self.higher_bound))


@dataclass
class Measure(Buildable):
    """
    Measurement captured during a step run, mapped to the
    ``Measure`` element in the Datawarehouse schema.

    Args:
        value: Recorded measurement value; type determines the emitted
            ``MeasureKind``.
        id: Unique identifier written to ``measure_id``.
        limit: Optional boundary information serialized to the ``limit`` element.
        time: Timestamp applied to ``measure_time``.
        comments: Free-text note stored in ``comments``.
        unit: Engineering unit label stored in ``unit``.
        symbol: Symbol for the measurement (for example `%`), stored in
            ``symbol``.
        status: Execution status for the measurement stored in
            ``measure_execution_status``.
    """
    value: bool | str | int | float | datetime.datetime
    id: str = field(default_factory=UTIL.uuid)
    limit: Limit | None = field(default=None)
    time: datetime.datetime = field(default_factory=datetime.datetime.now)
    comments: str = field(default='')
    unit: str = field(default='')
    symbol: str = field(default='')
    status: ExecutionStatusKind | None = field(default=None)

    @staticmethod
    def _init_value(value: bool | str | int | float | datetime.datetime) -> MeasureType.Value:
        """Create a MeasureType.Value object based on the type of ``value``."""
        if type(value) is str:
            kind = MeasureKind.STRING
        elif type(value) is bool:
            kind = MeasureKind.BOOL
        elif type(value) is int:
            kind = MeasureKind.INTEGER
        elif type(value) is float:
            kind = MeasureKind.REAL
        elif type(value) is datetime.datetime:
            kind = MeasureKind.DATETIME
        else:
            raise ValueError('Incompatible value type.')
        return MeasureType.Value(str(value), kind)

    def build(self) -> MeasureType:
        """
        Build the Measure into the XML-ready ``MeasureType`` with value,
        timestamps, limits, and metadata populated.
        """
        measure_type = MeasureType(value=Measure._init_value(self.value),
                                   measure_id=self.id,
                                   measure_time=UTIL.format_datetime(self.time))
        if self.limit is not None:
            measure_type.limit = MeasureType.Limit(limit_expression=str(self.limit))
        if self.comments != '':
            measure_type.comments = self.comments
        if self.unit != '':
            measure_type.unit = self.unit
        if self.symbol != '':
            measure_type.symbol = self.symbol
        if self.status is not None:
            measure_type.measure_execution_status = self.status
        return measure_type


@dataclass
class Characteristic(Buildable):
    """
    Arbitrary key/value metadata serialized to ``Characteristic`` elements in
    the Datawarehouse model.

    Args:
        full_name: Name of the characteristic (``full_name`` in XML).
        value: Optional value for the characteristic.
    """
    full_name: str
    value: str = field(default='')

    def build(self) -> CharacteristicType:
        characteristic = CharacteristicType(full_name=self.full_name)
        if self.value != '':
            characteristic.value = self.value
        return characteristic


@dataclass
class Document(Buildable):
    """
    Reference to a document attached to a run or product unit.

    Args:
        file_name: Path or filename written to ``file_name`` for downstream
            retrieval.
        identifier: Unique ID stored in ``identifier``.
        name: Human-readable label for the document stored in ``name``.
        description: Optional details stored in ``description``.
    """
    file_name: str
    identifier: str = field(default_factory=UTIL.uuid)
    name: str = field(default='')
    description: str = field(default='')

    def build(self) -> DocumentType:
        """Build the Document instance into the Proligent DocumentType."""
        document_type = DocumentType(identifier=self.identifier, file_name=self.file_name)
        if self.name != '':
            document_type.name = self.name
        if self.description != '':
            document_type.description = self.description
        return document_type


@dataclass
class ManufacturingStep(Buildable):
    """
    Common attributes shared by the process/operation/sequence/step run types in
    the Datawarehouse model.

    Args:
        id: Identifier applied to the corresponding ``*_id`` element.
        name: Display name for the step (``*_name`` field).
        status: Execution status written to the step-specific status field.
        start_time: Timestamp when the run started.
        end_time: Timestamp when the run ended; filled when marked complete.
    """
    id: str = field(default_factory=UTIL.uuid)
    name: str = field(default='')
    status: ExecutionStatusKind = field(default=ExecutionStatusKind.NOT_COMPLETED)
    start_time: datetime.datetime = field(default_factory=datetime.datetime.now)
    end_time: datetime.datetime = field(default_factory=datetime.datetime.now)

    def complete(self,
                 status: ExecutionStatusKind,
                 end_time: datetime.datetime | None = None) -> None:
        """
        Mark the step as finished and set the execution status and end time that
        will be serialized to the Datawarehouse payload.
        """
        self.status = status
        self.end_time = end_time or datetime.datetime.now()


@dataclass
class VersionedManufacturingStep(ManufacturingStep):
    """
    Extension of ``ManufacturingStep`` that carries the process/sequence version
    number written to the ``*_version`` field.
    """
    version: str = field(default='')


@dataclass
class StepRun(ManufacturingStep):
    """
    Execution of a single manufacturing step, serialized to ``StepRun`` with
    measures, characteristics, and attached documents.

    Args:
        measure: Optional initial measurement for the step run.
        characteristics: Metadata records serialized under ``characteristic``.
        documents: Document references serialized under ``document``.
    """
    measure: Measure | None = field(default=None, repr=False)
    characteristics: List[Characteristic] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)
    _measures: List[Measure] = field(default_factory=list, init=False)

    def __post_init__(self):
        # Initialize the internal list and seed it with the provided measure (if any).
        self._measures = []
        if self.measure is not None:
            self._measures.append(self.measure)
        # Drop the constructor-only attribute to discourage direct access later on.
        self.measure = None

    def build(self) -> StepRunType:
        """
        Build the step run into the XML-ready ``StepRunType`` including measures,
        execution timestamps, status, characteristics, and documents.
        """
        step_run_type = StepRunType(step_run_id=self.id)
        step_run_type.measure = [measure.build() for measure in self._measures]
        step_run_type.start_date = UTIL.format_datetime(self.start_time)
        if self.status != ExecutionStatusKind.NOT_COMPLETED:
            step_run_type.end_date = UTIL.format_datetime(self.end_time)
        if self.name != '':
            step_run_type.step_name = self.name
        if self.status is not None:
            step_run_type.step_execution_status = self.status
        if self.characteristics:
            step_run_type.characteristic = [
                characteristic.build() for characteristic in self.characteristics
            ]
        if self.documents:
            step_run_type.document = [document.build() for document in self.documents]
        return step_run_type

    def add_measure(self, measure: Measure) -> Measure:
        """
        Attach a measurement that will be emitted inside this ``StepRun``'s
        ``measure`` collection.

        We don't recommend having more than one measure per ``StepRun``; some
        downstream reports may not handle multiples.
        """
        self._measures.append(measure)
        return measure

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Attach metadata that will be serialized under this step run."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Associate a document reference with this step run."""
        self.documents.append(document)
        return document

    AddMeasure = add_measure
    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class SequenceRun(VersionedManufacturingStep):
    """
    Ordered collection of step runs executed on a station/user, mapped to the
    ``SequenceRun`` element in the Datawarehouse model.

    Args:
        steps: Step runs executed in order for this sequence.
        station: Station where the sequence ran (``station_full_name``).
        user: Operator who executed the sequence.
        characteristics: Metadata serialized under ``characteristic``.
        documents: Document references serialized under ``document``.
    """
    steps: List[StepRun] = field(default_factory=list)
    station: str = field(default='')
    user: str = field(default='')
    characteristics: List[Characteristic] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)

    def build(self) -> SequenceRunType:
        """
        Build the sequence run into ``SequenceRunType`` with timing, execution
        status, station/user context, characteristics, documents, and nested
        step runs.
        """
        seq_run = SequenceRunType(sequence_run_id=self.id)
        seq_run.step_run = [step.build() for step in self.steps]
        seq_run.start_date = UTIL.format_datetime(self.start_time)
        if self.status != ExecutionStatusKind.NOT_COMPLETED:
            seq_run.end_date = UTIL.format_datetime(self.end_time)
        if self.name != '':
            seq_run.sequence_full_name = self.name
        if self.status is not None:
            seq_run.sequence_execution_status = self.status
        if self.version != '':
            seq_run.sequence_version = self.version
        if self.station != '':
            seq_run.station_full_name = self.station
        if self.user != '':
            seq_run.user = self.user
        if self.characteristics:
            seq_run.characteristic = [
                characteristic.build() for characteristic in self.characteristics
            ]
        if self.documents:
            seq_run.document = [document.build() for document in self.documents]
        return seq_run

    def add_step_run(self, step_run: StepRun) -> StepRun:
        """Append a step run that will be serialized within ``sequence_run``."""
        self.steps.append(step_run)
        return step_run

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Attach metadata that will be serialized under this sequence run."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Associate a document reference with this sequence run."""
        self.documents.append(document)
        return document

    AddStepRun = add_step_run
    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class OperationRun(ManufacturingStep):
    """
    Group of sequence runs executed within a process operation, mapped to the
    ``OperationRun`` element.

    Args:
        sequences: Sequence runs belonging to the operation.
        station: Station context written to ``station_full_name``.
        user: Operator who executed the operation.
        process_name: Parent process name; defaults to the owning ``ProcessRun``
            when omitted.
        characteristics: Metadata serialized under ``characteristic``.
        documents: Document references serialized under ``document``.
    """
    sequences: List[SequenceRun] = field(default_factory=list)
    station: str = field(default='')
    user: str = field(default='')
    process_name: str = field(default='')
    characteristics: List[Characteristic] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)

    def build(self) -> OperationRunType:
        """
        Build the operation run into ``OperationRunType`` with timing, execution
        status, process name, station/user context, characteristics, documents,
        and nested sequence runs.
        """
        operation_run = OperationRunType(operation_run_id=self.id)
        operation_run.sequence_run = [sequence.build() for sequence in self.sequences]
        operation_run.operation_run_start_time = UTIL.format_datetime(self.start_time)
        if self.status != ExecutionStatusKind.NOT_COMPLETED:
            operation_run.operation_run_end_time = UTIL.format_datetime(self.end_time)
        if self.name != '':
            operation_run.operation_name = self.name
        if self.status is not None:
            operation_run.operation_status = self.status
        if self.station != '':
            operation_run.station_full_name = self.station
        if self.user != '':
            operation_run.user = self.user
        if self.process_name != '':
            operation_run.process_full_name = self.process_name
        if self.characteristics:
            operation_run.characteristic = [
                characteristic.build() for characteristic in self.characteristics
            ]
        if self.documents:
            operation_run.document = [document.build() for document in self.documents]
        return operation_run

    def add_sequence_run(self, sequence_run: SequenceRun) -> SequenceRun:
        """Append a sequence run that will be serialized within ``operation_run``."""
        if not sequence_run.station:
            sequence_run.station = self.station
        self.sequences.append(sequence_run)
        return sequence_run

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Attach metadata that will be serialized under this operation run."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Associate a document reference with this operation run."""
        self.documents.append(document)
        return document

    AddSequenceRun = add_sequence_run
    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class ProcessRun(VersionedManufacturingStep):
    """
    Top-level execution of a process, mapped to ``ProcessRun`` with nested
    operation runs.

    Args:
        product_unit_identifier: Identifier linking the process to a product
            unit in ``product_unit_identifier``.
        product_full_name: Display name for the product, persisted to
            ``product_full_name``.
        operations: Operation runs executed within the process.
        process_mode: Optional mode string written to ``process_mode``.
    """
    product_unit_identifier: str = field(default_factory=UTIL.uuid)
    product_full_name: str = field(default='DUT')
    operations: List[OperationRun] = field(default_factory=list)
    process_mode: str = field(default='')

    def build(self) -> ProcessRunType:
        """
        Build the process run into ``ProcessRunType`` with execution timing,
        status, process metadata, and nested operation runs.
        """
        process_run = ProcessRunType(process_run_id=self.id,
                                     product_unit_identifier=self.product_unit_identifier,
                                     product_full_name=self.product_full_name)
        for operation in self.operations:
            if operation.process_name == '':
                operation.process_name = self.name
        process_run.operation_run = [operation.build() for operation in self.operations]
        process_run.process_run_start_time = UTIL.format_datetime(self.start_time)
        if self.status != ExecutionStatusKind.NOT_COMPLETED:
            process_run.process_run_end_time = UTIL.format_datetime(self.end_time)
        if self.name != '':
            process_run.process_full_name = self.name
        if self.status is not None:
            process_run.process_run_status = self.status
        if self.version != '':
            process_run.process_version = self.version
        if self.process_mode != '':
            process_run.process_mode = self.process_mode
        return process_run

    def add_operation_run(self, operation_run: OperationRun) -> OperationRun:
        """Append an operation run that will be serialized within ``operation_run``."""
        if operation_run.process_name == '' and self.name != '':
            operation_run.process_name = self.name
        self.operations.append(operation_run)
        return operation_run

    AddOperationRun = add_operation_run


@dataclass
class ProductUnit(Buildable):
    """
    Description of the product unit involved in a process, mapped to the
    ``ProductUnit`` element.

    Args:
        product_unit_identifier: Unique identifier for the unit.
        product_full_name: Display name written to ``product_full_name``.
        characteristics: Metadata serialized under ``characteristic``.
        documents: Document references serialized under ``document``.
        manufacturer: Manufacturer name written to ``by_manufacturer``.
        creation_time: Timestamp for when the unit was created.
        manufacturing_time: Timestamp for when the unit was manufactured.
        scrapped: Flag indicating the unit was scrapped.
        scrap_time: Time when scrapping occurred.
    """
    product_unit_identifier: str = field(default_factory=UTIL.uuid)
    product_full_name: str = field(default='')
    characteristics: List[Characteristic] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)
    manufacturer: str = field(default=None)
    creation_time: datetime.datetime = field(default=None)
    manufacturing_time: datetime.datetime = field(default=None)
    scrapped: bool = field(default=None)
    scrap_time: datetime.datetime = field(default=None)

    def build(self) -> ProductUnitType:
        """
        Build the product unit into ``ProductUnitType`` with identifiers,
        timestamps, manufacturer information, characteristics, and documents.
        """
        product_unit_type = ProductUnitType(
            product_unit_identifier=self.product_unit_identifier,
            product_full_name=self.product_full_name,
        )
        if self.manufacturer:
            product_unit_type.by_manufacturer = self.manufacturer
        if self.creation_time:
            product_unit_type.creation_time = UTIL.format_datetime(self.creation_time)
        if self.manufacturing_time:
            product_unit_type.manufacturing_time = UTIL.format_datetime(self.manufacturing_time)
        if self.scrapped:
            product_unit_type.scrapped = self.scrapped
        if self.scrap_time:
            product_unit_type.scrapped_time = UTIL.format_datetime(self.scrap_time)
        if self.characteristics:
            product_unit_type.characteristic = [
                characteristic.build() for characteristic in self.characteristics
            ]
        if self.documents:
            product_unit_type.document = [document.build() for document in self.documents]
        return product_unit_type

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Attach metadata that will be serialized under this product unit."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Associate a document reference with this product unit."""
        self.documents.append(document)
        return document

    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class DataWareHouse(Buildable):
    """
    Container for the full Datawarehouse payload, including the top process run
    and optional product unit details.

    Args:
        top_process: The process run serialized to ``top_process_run``.
        product_unit: Optional product unit serialized to ``product_unit``.
        generation_time: Timestamp written to ``generation_time`` for the export.
        source_fingerprint: Identifier for the data source, stored in
            ``data_source_fingerprint``.
    """
    top_process: ProcessRun | None = field(default=None)
    product_unit: ProductUnit | None = field(default=None)
    generation_time: datetime.datetime = field(default_factory=datetime.datetime.now)
    source_fingerprint: str = field(default_factory=UTIL.uuid)

    def build(self) -> ProligentDatawarehouse:
        """
        Build the warehouse into ``ProligentDatawarehouse`` with generation
        time, data source fingerprint, and nested process/product information.
        """
        warehouse = ProligentDatawarehouse(generation_time=UTIL.format_datetime(self.generation_time),
                                           data_source_fingerprint=self.source_fingerprint)
        if self.top_process is not None:
            warehouse.top_process_run = [self.top_process.build()]
        if self.product_unit is not None:
            warehouse.product_unit = [self.product_unit.build()]
        return warehouse

    def set_process_run(self, process_run: ProcessRun) -> ProcessRun:
        """Assign the ``ProcessRun`` that will populate ``top_process_run``."""
        self.top_process = process_run
        return process_run

    def set_product_unit(self, product_unit: ProductUnit) -> ProductUnit:
        """Assign the ``ProductUnit`` that will populate ``product_unit``."""
        self.product_unit = product_unit
        return product_unit

    SetProcessRun = set_process_run
    SetProductUnit = set_product_unit
