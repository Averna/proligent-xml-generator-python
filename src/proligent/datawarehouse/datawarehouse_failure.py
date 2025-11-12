from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_component_unit import (
    ComponentUnitReferenceType,
)
from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
    DocumentType,
    UserCommentType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class FailureReferenceType:
    """A minimal set of information can be directly attached to a failure (see
    'FailureType') when it is created.

    For example, it is possible to specify the UUT that failed, the user
    that was testing it and the station where the failure was found.  It
    is not possible to specify a more detailed failure context on the
    failure itself. If you need more context on the failure (ex:
    sequence, step, mesure, etc), you can attach this information to the
    failure by adding a 'FailureReferenceType' to the execution element
    that detected the failure. For example, if the failure was deteced
    on a sequence, then add a 'FailureReferenceType' on the sequence.
    Note that this information is not required for a failure to be
    valid.  But if provided, it can't be updated. If an XML tries to
    change the value already contained in the data warehouse, the XML
    will be rejected.

    :ivar custom_data:
    :ivar id: The identifier of the related failure.
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
class MeasureFailureContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the measure that caused the failure to
        be detected.
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
class OperationRunFailureContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the operation run that caused the
        failure to be detected.
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
class RepairType:
    """
    Defines how a defect was repaired.

    :ivar custom_data:
    :ivar repair_technician: The name of the technician that executed
        the reparation. This attribute cannot be updated.
    :ivar repair_type_name: The exact type of reparation on the UUT (ex:
        replaced component, added solder, etc.) This attribute cannot be
        updated.
    :ivar close_time: The time when the defect was repaired. Note that
        the if the Data Warehouse already contains this defect but it is
        not already closed, the CloseTime written in the Data Warehouse
        will be set according to the following rule: CloseTime(in
        database) = OpenTime(in database) + (CloseTime(from xml) -
        OpenTime(from xml)) This attribute cannot be updated.
    :ivar repair_duration: Repair duration in seconds. This attribute
        cannot be updated.
    :ivar has_closed_failure: Identifies if repairing the current defect
        has closed the failure on the unit under test. This attribute
        can be updated.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    repair_technician: Optional[str] = field(
        default=None,
        metadata={
            "name": "RepairTechnician",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    repair_type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "RepairTypeName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        },
    )
    close_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "CloseTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    repair_duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "RepairDuration",
            "type": "Attribute",
        },
    )
    has_closed_failure: Optional[bool] = field(
        default=None,
        metadata={
            "name": "HasClosedFailure",
            "type": "Attribute",
        },
    )


@dataclass
class SequenceRunFailureContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the sequence run that caused the failure
        to be detected.
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
class StepRunFailureContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the step run that caused the failure to
        be detected.
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
class TopProcessRunFailureContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the top process run that caused the
        failure to be detected.
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
class DefectType:
    """A defect represents a physical problem with a UUT.

    When a defect exist on a UUT, the UUT is considered defective and
    needs to be repaired.  A defect may be caused by a defective
    component, or by other causes (ex: component missing, solder
    missing, etc). A defect is uniquely identified by its DefectId.

    :ivar characteristic:
    :ivar comment:
    :ivar failed_component_unit: Identifies the component unit that
        caused the defect.  Note that if the defect is not caused by a
        defective component (ex: bad solder), there won't be any
        associated failed component for the defect. All the attributes
        of this element can't be updated.
    :ivar repair: Identifies how the defect was repaired.  Once a defect
        is repaired, the defect is considered closed and can't be
        updated anymore.
    :ivar custom_data:
    :ivar failure_id: A defect is always associated to a failure.  The
        current attribute identifies the related failure.  This
        attribute cannot be updated.
    :ivar defect_id: The ID of the current defect.  This attribute
        cannot be updated.
    :ivar defect_type_name: The exact type of defect on the UUT:
        defective component, missing component, inverted component,
        missing solder, short circuit, etc. This attribute cannot be
        updated.
    :ivar defect_code: A detailed descriptor for the root cause of a
        defect, usually designated by standard code identifiers. This
        attribute can be updated until the defect is repaired.
    :ivar state: The state of the defect. For example, it can be
        something like "New", "Open", "Fixed", "Rejected",
        "Cancelled"... This attribute can be updated until the defect is
        repaired.
    :ivar debug_technician: The name of the debug technician that
        identified the failed component. This attribute cannot be
        updated.
    :ivar reference_designator: A string that identifies the instance or
        location of the component that was defective on the product unit
        identified in the failure. For example, if you have two
        instances of a given component part number on your product, then
        the reference designator can be used to associate a name with
        each of these instances. This attribute cannot be updated.
    :ivar open_time: Defines the creation time of the defect. This
        attribute cannot be updated.
    :ivar troubleshooting_duration: Troubleshooting duration in seconds.
        This attribute cannot be updated.
    """

    characteristic: List[CharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "Characteristic",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    comment: List[UserCommentType] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    failed_component_unit: Optional[ComponentUnitReferenceType] = field(
        default=None,
        metadata={
            "name": "FailedComponentUnit",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    repair: Optional[RepairType] = field(
        default=None,
        metadata={
            "name": "Repair",
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
    failure_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "FailureId",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    defect_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefectId",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    defect_type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefectTypeName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 128,
        },
    )
    defect_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "DefectCode",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 128,
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )
    debug_technician: Optional[str] = field(
        default=None,
        metadata={
            "name": "DebugTechnician",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    reference_designator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceDesignator",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )
    open_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "OpenTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    troubleshooting_duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "TroubleshootingDuration",
            "type": "Attribute",
        },
    )


@dataclass
class FailureContextType:
    """When it is not possible to specify the failure context at the same time as
    execution result through 'FailureReferenceType', it is possible to set them
    with the failure through 'FailureContextType'.

    Depending on the granularity of the information that you have, you
    may attach the failure to a measure, step run, sequence run,
    operation run or top process run. Note that all the fields in
    'FailureContextType' are not updatable.
    """

    measure: Optional[MeasureFailureContextType] = field(
        default=None,
        metadata={
            "name": "Measure",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    step_run: Optional[StepRunFailureContextType] = field(
        default=None,
        metadata={
            "name": "StepRun",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    sequence_run: Optional[SequenceRunFailureContextType] = field(
        default=None,
        metadata={
            "name": "SequenceRun",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    operation_run: Optional[OperationRunFailureContextType] = field(
        default=None,
        metadata={
            "name": "OperationRun",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    top_process_run: Optional[TopProcessRunFailureContextType] = field(
        default=None,
        metadata={
            "name": "TopProcessRun",
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


@dataclass
class FailureType:
    """Defines a failure, a "yield event".

    A Failure indicates that a UUT was tested in production, and the
    test failed. A failure is uniquely identified by its FailureId.

    :ivar characteristic:
    :ivar document:
    :ivar comment:
    :ivar context:
    :ivar custom_data:
    :ivar failure_id: Defines the failure unique identifier.
    :ivar open_date: The date of when the failure was opened.  This
        attribute cannot be updated.
    :ivar close_date: The date of when the failure was closed.  Once
        this attribute is specified, the failure is considered closed
        and it won't be updatable afterward. Note that the if the Data
        Warehouse already contains this failure but it is not already
        closed, the CloseDate written in the Data Warehouse will be set
        according to the following rule: CloseDate(in database) =
        OpenDate(in database) + (CloseDate(from xml) - OpenDate(from
        xml))
    :ivar state: The state of the failure.  For example, it can be
        something like "Opened", "Assigned", "Closed", etc. This
        property can be updated until the failure is closed (i.e.
        'CloseDate' is specified).
    :ivar tracking_id: Through this the failure can be associated to a
        tracking id coming from an external system, such as a work order
        id or incident id. This attribute cannot be updated.
    :ivar product_full_name: Defines the full name of the product for
        the current failure.  This attribute cannot be updated.
    :ivar product_unit_identifier: Defines the identifier of the product
        unit that had a failure.  This attribute cannot be updated.
    :ivar station_full_name: The station where the failure was first
        detected.  This attribute is optional because it is possible to
        find failures outside the context of a station.  This attribute
        of the failure can't be updated.
    :ivar opening_user: The user that detected the failure.  This
        attribute is optional because the failure can be opened
        automatically by a tool.  This attribute cannot be updated.
    :ivar closing_user: The user that closed the failure.  This
        attribute is optional because the failure can be opened
        automatically by a tool. This attribute is not updatable and
        should only be set when 'CloseDate' is specified.
    :ivar failure_cause: A high-level descriptor for the root cause of a
        failure. This is used to broadly categorize failures. Examples
        are "Product Defect", "Software Error", "Operator Error",
        "Station Not Calibrated". This attribute is not updatable and
        should only be set when 'CloseDate' is specified.
    :ivar failure_code: A detailed descriptor for the root cause of a
        failure, usually designated by standard code identifier, such as
        "FSE001 - Software Error: User Interface Crash", "FSE002 - Boot-
        up Sequence Hang", "FOE003 - Operator Error: optical cabling
        error". This attribute is not updatable and should only be set
        when 'CloseDate' is specified.
    :ivar top_defect_id: When a failure is found on an assembly, it is
        possible that the defect comes from a sub-assembly.  In that
        case, it is possible to open a new defect on the sub-assembly so
        that it can have it's own fail and repair life cycle.  In that
        situation, if you want to have traceability between the failure
        on the sub-assembly and the defect on the parent assembly,
        specify the identifier of the defect on the parent assembly in
        the attribute 'TopDefectId' within the sub-assembly failure.
        Note that if you have multiple level of assemblies and you open
        a failure at each level until you have found the faulty sub-
        assembly, then all the failures opened on the sub assemblies
        should point to the identifier of the defect on the top level
        assembly.  It should not point to the defect on it's direct
        parent assembly. This attribute cannot be updated.
    :ivar rma_number: The public identifier for the RMA. This number is
        also used to link failures to the RMA event. This attribute
        cannot be updated.
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
    comment: List[UserCommentType] = field(
        default_factory=list,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    context: Optional[FailureContextType] = field(
        default=None,
        metadata={
            "name": "Context",
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
    failure_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "FailureId",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    open_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "OpenDate",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    close_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "CloseDate",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )
    tracking_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TrackingId",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 128,
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
    opening_user: Optional[str] = field(
        default=None,
        metadata={
            "name": "OpeningUser",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    closing_user: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClosingUser",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    failure_cause: Optional[str] = field(
        default=None,
        metadata={
            "name": "FailureCause",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    failure_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "FailureCode",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    top_defect_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TopDefectId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    rma_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RmaNumber",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
