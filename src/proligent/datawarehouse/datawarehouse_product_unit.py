from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
    DocumentType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class ProductUnitType:
    """Defines a product unit.

    Product units are globaly unique by the combinaison of their
    ProductFullName and ProductUnitIdentifier properties.

    :ivar characteristic:
    :ivar document:
    :ivar custom_data:
    :ivar product_unit_identifier: Defines the unique identifier for the
        product unit.  The Serial Number is often used for this purpose.
        Note that ProductUnitIdentifiers must be unique for each
        ProductFullName.
    :ivar product_full_name: Full name of the product. If a hierarchy
        exists, the full name must contain the fully qualified name,
        each level being separated by a forward slash ("/").
    :ivar scrapped: Flag representing whether the product unit has been
        scrapped or not.  When not specified, it is assumed that the
        product unit is not scrapped.
    :ivar scrapped_time: Scrap date and time of the product unit.  If
        the 'Scrapped' attribute is set to 'True', the 'ScrappedTime'
        attribute has to be specified.
    :ivar creation_time: Creation date and time of the product unit.
        This attribute can't be updated after having been provided once.
    :ivar manufacturing_time: Date and time at which the product unit
        was manufactured. This attribute can't be updated after having
        been provided once.
    :ivar by_manufacturer: Name of the original EMS provider or
        manufacturing site. This attribute can't be updated after having
        been provided once.
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
    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
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
    scrapped: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Scrapped",
            "type": "Attribute",
        },
    )
    scrapped_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ScrappedTime",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    creation_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "CreationTime",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    manufacturing_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ManufacturingTime",
            "type": "Attribute",
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
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
