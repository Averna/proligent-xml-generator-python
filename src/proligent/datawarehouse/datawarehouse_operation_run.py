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
from proligent.datawarehouse.datawarehouse_sequence_run import (
    SequenceRunReferenceType,
    SequenceRunType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class OperationRunType:
    """Defines the operation run, a logical container for the execution of
    sequences and processes.

    Operation runs are globaly unique by their OperationRunId property.

    :ivar characteristic:
    :ivar document:
    :ivar sequence_run:
    :ivar failure_reference:
    :ivar sequence_run_reference:
    :ivar custom_data:
    :ivar operation_run_id: Defines an ID for this opportunity. This ID
        should be reused when providing results for an operation run
        spanned over multiple files. If no OperationRunId is provided,
        all the results of this operation run must be provided in the
        context of a single OperationRun. The OperationRunId must be
        unique across process runs.
    :ivar process_full_name: Defines the name of the current process in
        which this operation run is defined.  This may be different from
        the 'ProcessFullName' of the parent 'TopProcessRun' if the
        current operation is in a sub-process of the top parent. This
        attribute cannot be updated.
    :ivar process_version: Defines the process version of the process in
        which this operation run is defined. This field is optional to
        support non-versionable processes. The version string must be
        string-comparable to support ordering by version. This attribute
        cannot be updated.
    :ivar operation_name: Defines the name of the operation for this
        operation run. This attribute cannot be updated.
    :ivar station_full_name: Defines the station where the operation run
        was executed. This attribute cannot be updated.
    :ivar user: Defines the user that executed the operation run. This
        attribute cannot be updated.
    :ivar calling_operation_run_id: Defines the id of the operation run
        that launched the current operation run. Consider specifying a
        value when the process full name of the current operation run is
        different than the process full name of its process run. Setting
        this value will enable the ability to track the operation run
        call stack.
    :ivar operation_status: Defines the last known status of the
        operation run. This attribute can only be updated when closing
        the operation run (i.e. when providing a value for
        'OperationRunEndTime').
    :ivar operation_run_start_time: Defines the start date of the
        operation run. This attribute cannot be updated.
    :ivar operation_run_end_time: Defines the end date of the operation
        run.  If 'OperationStatus' is equal to 'NOT_COMPLETED' this
        value must be ommited. This value must be greater or equal than
        OperationRunEndTime. Note that the if the Data Warehouse already
        contains this operation run but it is not already closed, the
        OperationRunEndTime written in the Data Warehouse will be set
        according to the following rule: OperationRunEndTime(in
        database) = OperationRunStartTime(in database) +
        (OperationRunEndTime(from xml) - OperationRunStartTime(from
        xml)). This attribute cannot be updated.
    """

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
    sequence_run: List[SequenceRunType] = field(
        default_factory=list,
        metadata={
            "name": "SequenceRun",
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
    sequence_run_reference: List[SequenceRunReferenceType] = field(
        default_factory=list,
        metadata={
            "name": "SequenceRunReference",
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
    operation_run_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OperationRunId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    process_full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProcessFullName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 1900,
            "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
        },
    )
    process_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProcessVersion",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 64,
        },
    )
    operation_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "OperationName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 65,
        },
    )
    station_full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "StationFullName",
            "type": "Attribute",
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
    calling_operation_run_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CallingOperationRunId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    operation_status: Optional[ExecutionStatusKind] = field(
        default=None,
        metadata={
            "name": "OperationStatus",
            "type": "Attribute",
            "required": True,
        },
    )
    operation_run_start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "OperationRunStartTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    operation_run_end_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "OperationRunEndTime",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
