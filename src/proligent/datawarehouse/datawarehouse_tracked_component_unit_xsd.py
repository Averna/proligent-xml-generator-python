from dataclasses import dataclass, field
from typing import Optional

from proligent.datawarehouse.datawarehouse_component_unit import (
    ComponentUnitIdentifierType,
)
from proligent.datawarehouse.datawarehouse_model import (
    CustomDataType,
    ProductUnitUniqueIdentifierType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class TrackedComponentUnitType:
    """A tracked component unit is a component manufactured by a supplier to which
    we assign a product unit to be able to track it, run tests on it, etc.

    Adding a tracked component unit links the product unit to the
    provided component unit. Many product unit may link to the same
    component unit (this can be the case when a component unit represent
    a lot of component units to which the manufacturer gave no unique
    identity). However, a product unit can only be associated to one
    component unit. Tracked component units can't be updated (we can't
    modify the component unit associated to a product unit). Tracked
    component units are unique by their ProductUnitUniqueIdentifier.

    :ivar product_unit_unique_identifier: The identify of the product
        unit to which we want to associate the component unit.
    :ivar component_unit_identifier: The identify of the component unit
        we want to associate to the mentioned product unit.
    :ivar custom_data:
    """

    product_unit_unique_identifier: Optional[
        ProductUnitUniqueIdentifierType
    ] = field(
        default=None,
        metadata={
            "name": "ProductUnitUniqueIdentifier",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
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
