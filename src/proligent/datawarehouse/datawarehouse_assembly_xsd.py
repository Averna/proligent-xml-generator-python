from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_component_unit import (
    ComponentUnitReferenceType,
)
from proligent.datawarehouse.datawarehouse_model import CustomDataType

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


class AssemblyActionKind(Enum):
    """
    :cvar ASSEMBLE: This action indicates that a component unit or
        product unit was assembled on a parent product.
    :cvar DISASSEMBLE: This action indicates that a component unit or
        product unit was disassembled from a parent product.
    :cvar SET_CURRENT: This action indicates that a component unit or
        product unit was assembled on a parent product after the fact.
        This will typically be used when you receive products that are
        already assembled and you are interested in tracking the
        resulting assembly.
    """

    ASSEMBLE = "ASSEMBLE"
    DISASSEMBLE = "DISASSEMBLE"
    SET_CURRENT = "SET_CURRENT"


@dataclass
class AssemblyRuleComponentChildType:
    """
    :ivar manufacturer: The name of the component manufacturer.  When
        the attribute is not specified, it means that it is possible to
        assemble the designed component coming from any manufacturer.
        Otherwise, only components coming from this specific
        manufacturer are allowed.
    :ivar manufacturer_part_number: The part number of the component as
        defined by the manufacturer.
    :ivar component_full_name: The component full name of the component
        as redefined by your manufacturing process on top of the part
        number defined by the component manufacturer. If none exist, the
        manufacturerPartNumber can be provided.
    """

    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 1950,
            "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
        },
    )
    manufacturer_part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerPartNumber",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 128,
        },
    )
    component_full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ComponentFullName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 1950,
            "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
        },
    )


@dataclass
class AssemblyRuleParentType:
    """
    :ivar product_full_name: The product full name of the parent product
        that is affected by the assembly rule.
    :ivar reference_designator: A string that identifies the instance or
        location of the child component that is affected by the assembly
        rule.
    """

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
    reference_designator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceDesignator",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )


@dataclass
class AssemblyRuleProductChildType:
    """
    :ivar product_full_name: The full name of the child product that can
        be assembled.
    """

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


@dataclass
class AssemblyRuleChildType:
    """
    :ivar product:
    :ivar component:
    :ivar is_alternative: You usually have a preferred child for an
        assembly.  But even if you have preferences, you may be willing
        to accept using alternative childs.  For example, you may prefer
        the CPU coming from manufacturer 'X' but if he is running out of
        stock, you may be willing to use the CPU coming from
        manufacturer 'Y'.  In that case, you would have two assembly
        rules.  The first one would set 'IsAlternative' to 'false' for
        manufacturer 'X' while you would set 'IsAlternative' to 'true'
        for any other allowed manufacturer. Note that the DIT will not
        do any validation on that field.  So if you provide multiple
        rules that cause a given product to have multiple rules with
        'IsAlternative' to 'false', no errors will be flagged.
    """

    product: Optional[AssemblyRuleProductChildType] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    component: Optional[AssemblyRuleComponentChildType] = field(
        default=None,
        metadata={
            "name": "Component",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    is_alternative: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsAlternative",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AssemblyTraceParentType:
    """
    :ivar custom_data:
    :ivar product_full_name: The product full name of the parent product
        unit that contains a new assembled child.
    :ivar product_unit_identifier: The product unit identifier of the
        parent product unit that contains a new assembled child.
    :ivar reference_designator: A string that identifies the instance or
        location of the component that was assembled or disassembled.
        For example, if you have two instances of a given product unit
        or component unit on your parent product, then the reference
        designator can be used to associate a name with each of these
        instances.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
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
    reference_designator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceDesignator",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )


@dataclass
class OperationRunAssemblyContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the operation run where the
        assembly/disassembly was performed.
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
class SequenceRunAssemblyContextType:
    """
    :ivar custom_data:
    :ivar id: The identifier of the sequence run where the
        assembly/disassembly was performed.
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
class AssemblyContextType:
    """Used to indicate in which execution context the assembly/disassembly was
    performed.

    It can be either executed in a sequence run or operation run.  If
    your assembly/disassembly is performed outside of an execution
    context, simply don't provide an assembly context.
    """

    sequence_run: Optional[SequenceRunAssemblyContextType] = field(
        default=None,
        metadata={
            "name": "SequenceRun",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    operation_run: Optional[OperationRunAssemblyContextType] = field(
        default=None,
        metadata={
            "name": "OperationRun",
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
class AssemblyRuleType:
    """************************ IMPORTANT NOTE ************************
    This type of fact exists in the XSD but is not processed by the
    DIT.  It is only here for discussion purposes.  No bridge should
    generate this kind of fact.
    ****************************************************************
    An assembly rule defines the rules that have to be respected when your products are assembled.
    For example, it can be used to say that at location 'U22' of your product 'X' you want to assemble
    product 'Y' of manufacturer 'Z'.
    If you support many alternative childs for a given parent/reference designator combination,
    you will need to send multiple 'AssemblyRuleType' to the DIT and use the attribute
    'IsAlternative' of 'AssemblyRuleChildType' to identify your preferred type of child.
    This type is fully updatable including 'IsDeleted' which makes it possible to undelete an
    assembly rule.

    :ivar parent:
    :ivar child:
    :ivar id: The unique identifier of the assembly rule.
    :ivar description: The description of the assembly rule.
    :ivar is_deleted: Can be used to flag an assembly rule as deleted.
        Once deleted, it is not possible to undelete an assembly rule.
        When the attribute is not specified, it is assumed that the rule
        is not deleted.
    """

    parent: Optional[AssemblyRuleParentType] = field(
        default=None,
        metadata={
            "name": "Parent",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
        },
    )
    child: Optional[AssemblyRuleChildType] = field(
        default=None,
        metadata={
            "name": "Child",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
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
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
            "required": True,
            "max_length": 255,
        },
    )
    is_deleted: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsDeleted",
            "type": "Attribute",
        },
    )


@dataclass
class AssemblyTraceType:
    """An assembly trace is used to track what is being assembled and dissasembled.
    In the case where you disassemble or assemble parts in reaction to a test
    failure, it is possible to link the assembly/dissasembly actions with the
    failure.

    An assembly trace is uniquely identified by:
    - the identity of the parent (including the reference designator)
    - the identity of the child
    - the assembly action
    - the assembly time
    An assembly trace is not updatable.

    :ivar parent:
    :ivar child:
    :ivar assembly_context:
    :ivar custom_data:
    :ivar action: The assembly action performed.
    :ivar action_time: The time when the assembly action was performed.
        When the 'Action' is equal to 'SET_CURRENT' it should be the
        time when the current assembly was identified and entered in the
        system.
    :ivar failure_id: When the assembly action is performed in the
        context of a failure, the 'FailureId' attribute can be used to
        link the action with the failure.
    :ivar station_full_name: The station where the assembly action was
        performed.
    :ivar operator: The operator that performed the assembly action.
    :ivar child_component_count: The count of identical components that
        were part of this assembly trace. Default value when not
        provided is 1. Must be a value greater or equal to 0. This
        attribute can't be updated.
    """

    parent: Optional[AssemblyTraceParentType] = field(
        default=None,
        metadata={
            "name": "Parent",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
        },
    )
    child: Optional[ComponentUnitReferenceType] = field(
        default=None,
        metadata={
            "name": "Child",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
        },
    )
    assembly_context: Optional[AssemblyContextType] = field(
        default=None,
        metadata={
            "name": "AssemblyContext",
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
    action: Optional[AssemblyActionKind] = field(
        default=None,
        metadata={
            "name": "Action",
            "type": "Attribute",
            "required": True,
        },
    )
    action_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ActionTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    failure_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "FailureId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
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
    operator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Operator",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    child_component_count: int = field(
        default=1,
        metadata={
            "name": "ChildComponentCount",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
