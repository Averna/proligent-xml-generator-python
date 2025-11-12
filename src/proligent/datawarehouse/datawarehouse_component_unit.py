from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
    ProductUnitUniqueIdentifierType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class ComponentUnitIdentifierType:
    """
    This type groups all the fields that can participate in the identification of a
    component unit.

    :ivar custom_data:
    :ivar manufacturer: The name of the original manufacturer of the
        component without considering any intermediate distributor. For
        example, if you buy a component manufactured by company X but
        distributed by company Y, the manufacturer will be X. This
        attribute can't be updated.
    :ivar manufacturer_part_number: The part number of the component as
        defined by the supplier. This attribute can't be updated.
    :ivar manufacturer_lot: The lot number in which the component unit
        was included as defined by the supplier. This attribute can't be
        updated.
    :ivar manufacturer_serial_number: The serial number of the component
        unit as defined by the supplier. This attribute is optional
        because not all components have a serial number.  For example,
        individual resistors don't typically have a serial number. This
        attribute can't be updated.
    :ivar component_full_name: The component full name of the component
        as redefined by your manufacturing process on top of the part
        number defined by the component manufacturer. If none exist, the
        ManufacturerPartNumber can be provided. This attribute can't be
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
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Attribute",
            "required": True,
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
    manufacturer_lot: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerLot",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    manufacturer_serial_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "ManufacturerSerialNumber",
            "type": "Attribute",
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
class ComponentUnitReferenceType:
    """This type groups all the fields that can participate in the identification
    of a component unit when referenced in another context (defect, assembly,
    etc.).

    A component unit reference can be one of three things :
    - A product unit
    - A component unit to which a product unit was associated. In this case, any of the two identifiers can be provided
    - A component unit that has no corresponding product unit.
    Providing a product unit unique identifier to identify a component unit means that the referred component unit is a part produced in-house
    or a tracked component unit (a component unit manufactured by a supplier to which a product full name and product unit identifier was given).
    Providing a component unit identifier is necessary when the part is produced by an external manufacturer and when it has no in-house
    product full name and product unit identifier associated.
    """

    product_unit_unique_identifier: Optional[
        ProductUnitUniqueIdentifierType
    ] = field(
        default=None,
        metadata={
            "name": "ProductUnitUniqueIdentifier",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    component_unit_identifier: Optional[ComponentUnitIdentifierType] = field(
        default=None,
        metadata={
            "name": "ComponentUnitIdentifier",
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
class ComponentUnitType:
    """A component unit is very similar to a product unit (see ProductUnitType)
    except that it is a part that you don't manufacture yourself.

    For example, if you buy microprocessors and assemble them in your
    products, then each instance of a microprocessor that you assemble
    becomes a component unit that has a part number and serial/lot
    number. Note that if your manufacturing process generates assemblies
    (child assemblies) that are packaged later in larger assemblies
    (parent assemblies), then the child assemblies should not be sent to
    the DIT as component units.  They should be sent as product units. A
    Component Unit can be assigned a product full name and a product
    unit identifier to be able to track it and run tests on it. This can
    be done when providing ProductUnit information (see
    ProductUnitType).

    :ivar characteristic:
    :ivar component_unit_identifier:
    :ivar custom_data:
    :ivar manufacturing_date: The manufacturing date of the component
        unit. This attribute can't be updated after having been provided
        once.
    :ivar distributor: The distributor of the component unit. This
        attribute can't be updated after having been provided once.
    """

    characteristic: List[CharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "Characteristic",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    component_unit_identifier: Optional[ComponentUnitIdentifierType] = field(
        default=None,
        metadata={
            "name": "ComponentUnitIdentifier",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
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
    manufacturing_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ManufacturingDate",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    distributor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Distributor",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 128,
        },
    )
