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
class RmacloseType:
    """
    Represents the closing event of a return merchandise authorization (RMA).

    :ivar custom_data:
    :ivar reason: The actual reason for closing the RMA. Ex: Shipped
        Replacement, Upgrade Performed, Repaired, No Fault Found, ...
        This attribute cannot be updated.
    :ivar comment: Free-text comment that complements the closing
        reason. This attribute cannot be updated.
    :ivar close_time: The time at which the RMA was closed. Note that
        the if the Data Warehouse already contains this product unit
        return but it is not already closed, the CloseTime written in
        the Data Warehouse will be set according to the following rule:
        CloseTime(in database) = ReceivedTime(in database) +
        (CloseTime(from xml) - ReceivedTime(from xml)). This attribute
        cannot be updated.
    """

    class Meta:
        name = "RMACloseType"

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reason",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
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


@dataclass
class ProductUnitReturnType:
    """Represents the event of a return merchandise authorization (RMA).

    Product unit returns are globally unique by their
    ProductUnitReturnId

    :ivar characteristic:
    :ivar document:
    :ivar close: When this attribute is not specified.  The RMA is
        considered opened. Once specified, the RMA is considered closed
        and can't be updated anymore.
    :ivar custom_data:
    :ivar product_unit_return_id: Globally unique id for identifying a
        RMA event.  Note that in a single RMA, multiple product units
        can be returned.  So, there will be one RMA (identified by
        'RmaNumber') for multiple returns (identified by
        'ProductUnitReturnId'). This attribute cannot be updated.
    :ivar product_unit_identifier: Defines the unique identifier for the
        product unit return.  The Serial Number is often used for this
        purpose. Note that ProductUnitIdentifiers must be unique for
        each ProductFullName. This attribute cannot be updated.
    :ivar product_full_name: Full name of the product. If a hierarchy
        exists, the full name must contain the fully qualified name,
        each level being separated by a forward slash ("/"). This
        attribute cannot be updated.
    :ivar customer_id: Reference to the information on the customer for
        which the RMA was issued. The full customer's details must be
        provided in a separate xml entity (Customer...) This attribute
        cannot be updated.
    :ivar by_manufacturer: Name of the original EMS provider or
        manufacturing site. This attribute cannot be updated.
    :ivar issuer_user: Customer support agent that issue the RMA. This
        attribute cannot be updated.
    :ivar receiver_user: The operator that received and registered the
        actual product unit after the RMA has been issued. This
        attribute cannot be updated.
    :ivar rma_number: The public identifier for the RMA that contains
        the current product unit return.  A single RMA can contain
        multiple product unit returns. Note that this number is also
        used to link failures to the RMA. This attribute cannot be
        updated.
    :ivar return_reason: The reason for which the product unit was
        returned. ex: Upgrade, Operation failure, ... This attribute
        cannot be updated.
    :ivar return_comment: Free-text comment that complements the return
        reason. This attribute cannot be updated.
    :ivar shipped_time: The original shipment time of the product unit
        to the customer. This attribute cannot be updated.
    :ivar received_time: The time at which the product unit was received
        for diagnostic after the RMA. This attribute cannot be updated.
    :ivar is_warranty: Defines whether the unit is under warranty at the
        time of the RMA issue. When not provided, default value is {Not
        available}. This attribute cannot be updated.
    :ivar process_run_id: Defines the id of the execution of the RMA
        process of the product unit. This attribute cannot be updated.
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
    close: Optional[RmacloseType] = field(
        default=None,
        metadata={
            "name": "Close",
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
    product_unit_return_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProductUnitReturnId",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
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
    customer_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "CustomerId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
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
    issuer_user: Optional[str] = field(
        default=None,
        metadata={
            "name": "IssuerUser",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    receiver_user: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReceiverUser",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    rma_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "RmaNumber",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    return_reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReturnReason",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    return_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReturnComment",
            "type": "Attribute",
        },
    )
    shipped_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ShippedTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    received_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ReceivedTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    is_warranty: Optional[bool] = field(
        default=None,
        metadata={
            "name": "IsWarranty",
            "type": "Attribute",
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
