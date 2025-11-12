from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class ShipmentType:
    """Defines a shipment of product units.

    Shipments are globally unique by CustomerId, ProductFullName,
    ByManufacturer, ShippedDate and IsRefurbished This fact cannot be
    updated.

    :ivar characteristic:
    :ivar custom_data:
    :ivar customer_id: Reference to the informations on the customer for
        which the RMA was issued. The full customer's details must be
        provided in a separate xml entity (Customer...)
    :ivar sales_order_number: The sales order number that this shipment
        is associated with.
    :ivar by_manufacturer: Name of the original EMS provider or
        manufacturing site.
    :ivar is_refurbished: Defines whether the shipment contains new or
        refurbished units.
    :ivar shipped_date: The original shipment time of the product unit
        to the customer.
    :ivar quantity: Represents the number of items shipped.
    :ivar product_full_name: Full name of the product. If a hierarchy
        exists, the full name must contain the fully qualified name,
        each level being separated by a forward slash ("/").
    """

    characteristic: List[CharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "Characteristic",
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
    customer_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CustomerId",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    sales_order_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "SalesOrderNumber",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        },
    )
    by_manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "name": "ByManufacturer",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    is_refurbished: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsRefurbished",
            "type": "Attribute",
            "required": True,
        },
    )
    shipped_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ShippedDate",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    quantity: Optional[int] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Attribute",
            "required": True,
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
