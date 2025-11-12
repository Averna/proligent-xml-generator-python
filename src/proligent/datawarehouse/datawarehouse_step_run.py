from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_failure import FailureReferenceType
from proligent.datawarehouse.datawarehouse_measure import MeasureType
from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
    DocumentType,
    ExecutionStatusKind,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class StepRunType:
    """A step run is a time-bound logical container for a set of measures.

    A step run is uniquely identified by its StepRunId. A step run is
    not updatable.

    :ivar measure:
    :ivar failure_reference:
    :ivar characteristic:
    :ivar document:
    :ivar custom_data:
    :ivar step_execution_status: Defines the latest status for the
        current step run.
    :ivar step_run_id: Defines the step run unique identifier. This ID
        must be unique across sequence runs.
    :ivar step_name: Defines the step name for the current step run.
    :ivar start_date: Defines the actual date where the step run
        started.
    :ivar end_date: Defines the actual date where the step run ended.
        If 'StepExecutionStatus' is equal to 'NOT_COMPLETED' this value
        must be ommited.  StepRunId must have been provided to allow
        step run updates through DIT increment.
    """

    measure: List[MeasureType] = field(
        default_factory=list,
        metadata={
            "name": "Measure",
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
    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    step_execution_status: Optional[ExecutionStatusKind] = field(
        default=None,
        metadata={
            "name": "StepExecutionStatus",
            "type": "Attribute",
            "required": True,
        },
    )
    step_run_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepRunId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    step_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "StepName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 255,
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
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
