from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_failure import FailureReferenceType
from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
    DocumentType,
    ExecutionStatusKind,
)
from proligent.datawarehouse.datawarehouse_step_run import StepRunType

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class SequenceRunReferenceType:
    """SequenceRun imported as StandaloneSequenceRunType element can have their
    process and operation context set with this reference.

    SequenceRunRefFact are unique by the ID of their parent Operation
    run and the ID of the referred sequence run.

    :ivar custom_data:
    :ivar id: The identifier of the related SequenceRun.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )


@dataclass
class SequenceRunType:
    """A sequence run is a time-bound logical container for a set of step runs.

    Sequence runs are globaly unique by their SequenceRunId property.
    SequenceRunType defines a sequence run when it is executed in the
    context of a process and an operation.

    :ivar step_run: Defines a step run, a container for the execution of
        a step that contains measures.
    :ivar characteristic: Defines a characteristic, a key/value pair
        used to store arbitrary information associated to this sequence
        run.
    :ivar document:
    :ivar failure_reference:
    :ivar custom_data:
    :ivar start_date: Defines the actual date where the sequence run
        started.
    :ivar end_date: Defines the actual date where the sequence run
        ended. If 'SequenceExecutionStatus' is equal to 'NOT_COMPLETED'
        this value must be ommited. SequenceRunId must have been
        provided to allow sequence run updates through DIT increment.
        This value must be greater or equal than StartDate. Note that
        the if the Data Warehouse already contains this sequence run but
        it is not already closed, the EndDate written in the Data
        Warehouse will be set according to the following rule:
        EndDate(in database) = StartDate(in database) + (EndDate(from
        xml) - StartDate(from xml)).
    :ivar sequence_execution_status: Defines the latest execution status
        of the sequence run.
    :ivar sequence_run_id: Defines a Sequence Run identifier, used to
        update sequence runs when results are generated partially, i.e.
        without an end date. If this ID is not specified, the current
        run is considered as anonymous and will not be updateable once
        inserted in the proligent.datawarehouse. This ID must be unique across
        operation runs.
    :ivar sequence_full_name: Defines the full name of the sequence
        executed in this sequence run. This attribute cannot be updated.
    :ivar sequence_version: Defines the sequence's version for this
        sequence run. This field is optional to support non-versionable
        Sequences. The version string must be string-comparable to
        support ordering by version.
    :ivar station_full_name: Defines the station where the sequence run
        was executed. This attribute cannot be updated.
    :ivar user: Defines the user that executed the sequence run. This
        attribute cannot be updated.
    """

    step_run: List[StepRunType] = field(
        default_factory=list,
        metadata={
            "name": "StepRun",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    characteristic: List[CharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "Characteristic",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    document: List[DocumentType] = field(
        default_factory=list,
        metadata={
            "name": "Document",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    failure_reference: List[FailureReferenceType] = field(
        default_factory=list,
        metadata={
            "name": "FailureReference",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    start_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "StartDate",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    end_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EndDate",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    sequence_execution_status: Optional[ExecutionStatusKind] = field(
        default=None,
        metadata={
            "name": "SequenceExecutionStatus",
            "type": "Attribute",
            "required": True,
        },
    )
    sequence_run_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SequenceRunId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    sequence_full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SequenceFullName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 1986,
            "pattern": r"([^/\s][^/]{0,263}){0,1}[^/\s](/([^/\s][^/]{0,263}){0,1}[^/\s])*",
        },
    )
    sequence_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "SequenceVersion",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 64,
        },
    )
    station_full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "StationFullName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 1950,
            "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
        },
    )
    user: Optional[str] = field(
        default=None,
        metadata={
            "name": "User",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )


@dataclass
class StandaloneSequenceRunType(SequenceRunType):
    """A stand alone sequence run is a time-bound logical container for a set of
    step runs.

    Stand alone sequence runs are globaly unique by their SequenceRunId
    property. StandaloneSequenceRunType defines a sequence run when the
    process and an operation context cannot be provided. The process and
    operation context can be set by having a OperationRunId in the
    optional OperationRunId property. If the process and operation
    context is not provided with this stand alone sequence run, it can
    be later made by providing a SequenceRunReference to this
    SequenceRunId in the OperationRun element. If the SequenceRunId is
    not provided in this stand alone sequence run, it will be impossible
    to set the process and operation context using the
    SequenceRunReference.

    :ivar product_unit_identifier: Defines the product unit identifier
        on which the sequence is ran. This attribute cannot be updated.
    :ivar product_full_name: Defines the name the product for the
        current sequence run. This attribute cannot be updated.
    :ivar operation_run_id: Defines the process and operation context.
        The refered OperationRun can be imported before or after this
        result. The reference is optional. A SequenceRun can exists
        without a process and operation context The process and
        operation context can also be provided when importing the
        OperationRun Once specified, this attribute cannot be updated.
    """

    product_unit_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProductUnitIdentifier",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    product_full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProductFullName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 1950,
            "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
        },
    )
    operation_run_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OperationRunId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
