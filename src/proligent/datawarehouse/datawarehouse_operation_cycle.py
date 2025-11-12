from dataclasses import dataclass, field
from typing import Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_model import (
    CustomDataType,
    ExecutionStatusKind,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class OperationCycleType:
    """Defines the operation cycle, which maps the high-level movement (MES level)
    of a unit within a manufacturing process.

    It is used to provide more up-to-date information on WIP. Operation
    Cycles are globaly unique by their OperationCycleId property.

    :ivar custom_data:
    :ivar process_full_name: Defines the name of the current process in
        which this operation cycle is defined.  This may be different
        from the 'ProcessFullName' of the parent 'TopProcessRun' if the
        current operation is in a sub-process of the top parent. This
        attribute cannot be updated.
    :ivar process_version: Defines the process version of the process in
        which this operation run is defined. This field is optional to
        support non-versionable processes. The version string must be
        string-comparable to support ordering by version. This attribute
        cannot be updated.
    :ivar operation_cycle_id: Defines an ID for this operation cycle.
        This ID should be reused when providing results for an operation
        cycle spanned over multiple files. If no OperationCycleId is
        provided, all the results of this operation cycle must be
        provided in the context of a single OperationCycle. The
        OperationCycleId must be unique across process runs.
    :ivar operation_name: Defines the name of the operation for this
        operation cycle. This attribute cannot be updated.
    :ivar location: Defines the location where the operation cycle was
        executed.(node/category of the full station name (site where the
        station is located)) This attribute cannot be updated.
    :ivar user: Defines the user that initiated the operation cycle.
        This attribute cannot be updated.
    :ivar operation_cycle_status: Defines the last known status of the
        operation cycle. This attribute can only be updated when closing
        the operation cycle (i.e. when providing a value for
        'OperationCycleEndTime').
    :ivar operation_cycle_start_time: Defines the start date of the
        operation cycle, i.e. when the unit was routed in the operation.
        This attribute cannot be updated.
    :ivar operation_cycle_end_time: Defines the end date of the
        operation cycle, i.e. when the unit was routed out of the
        operation.  If 'OperationCycleStatus' is equal to
        'NOT_COMPLETED' this value must be ommited. This value must be
        greater or equal than OperationCycleEndTime. Note that the if
        the Data Warehouse already contains this operation cycle but it
        is not already closed, the OperationCycleEndTime written in the
        Data Warehouse will be set according to the following rule:
        OperationCycleEndTime(in database) = OperationCycleStartTime(in
        database) + (OperationCycleEndTime(from xml) -
        OperationCycleStartTime(from xml)). This attribute cannot be
        updated.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
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
    operation_cycle_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "OperationCycleId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
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
    location: Optional[str] = field(
        default=None,
        metadata={
            "name": "Location",
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
    operation_cycle_status: Optional[ExecutionStatusKind] = field(
        default=None,
        metadata={
            "name": "OperationCycleStatus",
            "type": "Attribute",
            "required": True,
        },
    )
    operation_cycle_start_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "OperationCycleStartTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    operation_cycle_end_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "OperationCycleEndTime",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
