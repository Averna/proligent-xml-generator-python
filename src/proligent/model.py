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
    Helper functions.
    """
    def __init__(
        self,
        timezone: str | datetime.tzinfo | None = None,
        destination_dir: str = r"C:\Proligent\IntegrationService\Acquisition",
        schema_path: str | Path | None = None,
    ) -> None:
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
        Formats the given datetime object to a string representation with microseconds and timezone offset.

        Args:
            date_time (datetime, optional): The datetime object to be formatted. If not provided, the current time will
            be used.

        Returns:
            str: The formatted datetime string.

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

    def _machine_timezone(self) -> datetime.tzinfo:
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
        return str(uuid.uuid4())

    def _load_schema(self) -> xmlschema.XMLSchema:
        if self._schema_cache is None:
            self._schema_cache = xmlschema.XMLSchema(self._schema_path)
        return self._schema_cache

    def validate_xml(self, xml_file: str | Path) -> None:
        """Validate the provided XML file against the Proligent DataWarehouse schema."""
        xml_path = Path(xml_file)
        schema = self._load_schema()
        schema.validate(xml_path)


# Create a Util instance for formatting datetime and generating UUIDs.
# Can be overridden on module level if needed.
UTIL = Util()


class Buildable:
    """Parent class that allows generic conversion to XML."""
    def build(self) -> Any:
        """Parent method without implementation."""
        return None

    def to_xml(self) -> str:
        """Convert object to a xml string."""
        # Initialize the context, parser, and serializer
        context = XmlContext()
        serializer = XmlSerializer(context=context)

        # Serialize the dataclass instance to an XML string
        return serializer.render(self.build())

    def save_xml(self, destination: str = ''):
        """Save object to a xml file."""
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
    Enumeration of limit expressions.
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
    Represents a limit expression with a lower and/or higher bound.
    """
    expression: LimitExpression
    lower_bound: Any = field(default='')
    higher_bound: Any = field(default='')

    def __str__(self) -> str:
        return self.expression.value.replace('LOWERBOUND', str(self.lower_bound)).replace('HIGHERBOUND', str(self.higher_bound))


@dataclass
class Measure(Buildable):
    """
    Wrapper for the MeasureType class
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
        """
        Create a MeasureType.Value object based on the type of the input value.
        """
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
        """Build the Measure instance into the Proligent MeasureType."""
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
    """Simple representation of a characteristic key/value pair."""
    full_name: str
    value: str = field(default='')

    def build(self) -> CharacteristicType:
        characteristic = CharacteristicType(full_name=self.full_name)
        if self.value != '':
            characteristic.value = self.value
        return characteristic


@dataclass
class Document(Buildable):
    """Representation of a document attachment."""
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
    """Generic class definition for processes, sequences, ... that contain these attributes."""
    id: str = field(default_factory=UTIL.uuid)
    name: str = field(default='')
    status: ExecutionStatusKind = field(default=ExecutionStatusKind.NOT_COMPLETED)
    start_time: datetime.datetime = field(default_factory=datetime.datetime.now)
    end_time: datetime.datetime = field(default_factory=datetime.datetime.now)

    def complete(self,
                 status: ExecutionStatusKind,
                 end_time: datetime.datetime | None = None) -> None:
        """Mark the step as completed, stamping the end time if not provided."""
        self.status = status
        self.end_time = end_time or datetime.datetime.now()


@dataclass
class VersionedManufacturingStep(ManufacturingStep):
    """Adds the version attribute to ManufacturingStep."""
    version: str = field(default='')


@dataclass
class StepRun(ManufacturingStep):
    """Wrapper for the StepRunType class."""
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
        """Build the StepRun instance into the Proligent MeasureType."""
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
        Append an existing measure to this step run.
        We don't recommend having more than one measure per StepRun. While it is supported there are reports that don't
        behave well with it.
        """
        self._measures.append(measure)
        return measure

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Append an existing characteristic to this step run."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Attach an existing document to this step run."""
        self.documents.append(document)
        return document

    AddMeasure = add_measure
    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class SequenceRun(VersionedManufacturingStep):
    """Wrapper for the SequenceRunType class."""
    steps: List[StepRun] = field(default_factory=list)
    station: str = field(default='')
    user: str = field(default='')
    characteristics: List[Characteristic] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)

    def build(self) -> SequenceRunType:
        """Build the SequenceRun instance into the Proligent SequenceRunType."""
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
        """Append an existing step run to this sequence."""
        self.steps.append(step_run)
        return step_run

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Append an existing characteristic to this sequence run."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Attach an existing document to this sequence run."""
        self.documents.append(document)
        return document

    AddStepRun = add_step_run
    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class OperationRun(ManufacturingStep):
    """Wrapper for the OperationRunType class."""
    sequences: List[SequenceRun] = field(default_factory=list)
    station: str = field(default='')
    user: str = field(default='')
    process_name: str = field(default='')
    characteristics: List[Characteristic] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)

    def build(self) -> OperationRunType:
        """Build the OperationRun instance into the Proligent OperationRunType."""
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
        """Append an existing sequence run to this operation."""
        if not sequence_run.station:
            sequence_run.station = self.station
        self.sequences.append(sequence_run)
        return sequence_run

    def add_characteristic(self, characteristic: Characteristic) -> Characteristic:
        """Append an existing characteristic to this operation run."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Attach an existing document to this operation run."""
        self.documents.append(document)
        return document

    AddSequenceRun = add_sequence_run
    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class ProcessRun(VersionedManufacturingStep):
    """Wrapper for the ProcessRunType class."""
    product_unit_identifier: str = field(default_factory=UTIL.uuid)
    product_full_name: str = field(default='DUT')
    operations: List[OperationRun] = field(default_factory=list)
    process_mode: str = field(default='')

    def build(self) -> ProcessRunType:
        """Build the ProcessRun instance into the Proligent ProcessRunType."""
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
        """Append an existing operation run to this process."""
        if operation_run.process_name == '' and self.name != '':
            operation_run.process_name = self.name
        self.operations.append(operation_run)
        return operation_run

    AddOperationRun = add_operation_run


@dataclass
class ProductUnit(Buildable):
    """Wrapper for the ProductUnitType class."""
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
        """Build the ProductUnit instance into the Proligent ProductUnitType."""
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
        """Append an existing characteristic to this product unit."""
        self.characteristics.append(characteristic)
        return characteristic

    def add_document(self, document: Document) -> Document:
        """Attach an existing document to this product unit."""
        self.documents.append(document)
        return document

    AddCharacteristic = add_characteristic
    AddDocument = add_document


@dataclass
class DataWareHouse(Buildable):
    """Wrapper for the ProligentDatawarehouse class."""
    top_process: ProcessRun | None = field(default=None)
    product_unit: ProductUnit | None = field(default=None)
    generation_time: datetime.datetime = field(default_factory=datetime.datetime.now)
    source_fingerprint: str = field(default_factory=UTIL.uuid)

    def build(self) -> ProligentDatawarehouse:
        """Build the DataWareHouse instance into the Proligent ProligentDatawarehouse."""
        warehouse = ProligentDatawarehouse(generation_time=UTIL.format_datetime(self.generation_time),
                                           data_source_fingerprint=self.source_fingerprint)
        if self.top_process is not None:
            warehouse.top_process_run = [self.top_process.build()]
        if self.product_unit is not None:
            warehouse.product_unit = [self.product_unit.build()]
        return warehouse

    def set_process_run(self, process_run: ProcessRun) -> ProcessRun:
        """Assign the top process run for this data warehouse."""
        self.top_process = process_run
        return process_run

    def set_product_unit(self, product_unit: ProductUnit) -> ProductUnit:
        """Assign the product unit associated with this data warehouse."""
        self.product_unit = product_unit
        return product_unit

    SetProcessRun = set_process_run
    SetProductUnit = set_product_unit
