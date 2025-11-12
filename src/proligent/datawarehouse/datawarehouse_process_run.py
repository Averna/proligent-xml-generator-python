from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_failure import FailureReferenceType
from proligent.datawarehouse.datawarehouse_model import (
    CustomDataType,
    ExecutionStatusKind,
)
from proligent.datawarehouse.datawarehouse_operation_cycle import OperationCycleType
from proligent.datawarehouse.datawarehouse_operation_run import OperationRunType

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class ProcessRunType:
    """Defines a process run, a logical container for the execution of operations.

    Process runs are globaly unique by their ProcessRunId property.

    :ivar operation_run:
    :ivar operation_cycle:
    :ivar failure_reference:
    :ivar custom_data:
    :ivar process_run_id: Defines an ID for this process run. This ID
        should be reused when providing results for a process run
        spanned over multiple files. If no ProcessRunId is provided, all
        the results of this process run must be provided in the context
        of a single ProcessRun.
    :ivar process_full_name: Defines the name of the process for this
        process run.
    :ivar process_version: Defines the process's version for this
        operation opportunity. This field is optional to support non-
        versionable process. The version string must be string-
        comparable to support ordering by version.
    :ivar product_unit_identifier: Defines the product unit identifier
        on which the process is ran. This attribute cannot be updated.
    :ivar product_full_name: Defines the name the product for the
        current process run. This attribute cannot be updated.
    :ivar process_run_status: Defines the last known status of the
        process run.
    :ivar process_run_start_time: Defines the start date of the process
        run.
    :ivar process_run_end_time: Defines the end date of the process run.
        If 'ProcessRunStatus' is equal to 'NOT_COMPLETED' this value
        must be ommited. This value must be greater or equal than
        ProcessRunStartTime. Note that the if the Data Warehouse already
        contains this process run but it is not already closed, the
        ProcessRunEndTime written in the Data Warehouse will be set
        according to the following rule: ProcessRunEndTime(in database)
        = ProcessRunStartTime(in database) + (ProcessRunEndTime(from
        xml) - ProcessRunStartTime(from xml)).
    :ivar process_mode: Defines the mode on which the process run has
        been ran, E.G. NPI, Production, etc.
    """

    operation_run: List[OperationRunType] = field(
        default_factory=list,
        metadata={
            "name": "OperationRun",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    operation_cycle: List[OperationCycleType] = field(
        default_factory=list,
        metadata={
            "name": "OperationCycle",
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
    process_run_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProcessRunId",
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
    process_run_status: Optional[ExecutionStatusKind] = field(
        default=None,
        metadata={
            "name": "ProcessRunStatus",
            "type": "Attribute",
            "required": True,
        },
    )
    process_run_start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ProcessRunStartTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    process_run_end_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ProcessRunEndTime",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    process_mode: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProcessMode",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 64,
        },
    )
