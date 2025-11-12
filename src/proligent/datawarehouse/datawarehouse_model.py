from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class CustomDataType:
    """The values defined under this element will not be interpreted by the DIT.

    It can be used to store data that will be used by another system.
    """

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "process_contents": "skip",
        },
    )


class ExecutionStatusKind(Enum):
    """
    :cvar PASS: The execution completed successfully.
    :cvar FAIL: The execution completed and failures were detected.
    :cvar NOT_COMPLETED: The execution is not completed.  It is still in
        progress.  In that situation, the end time of the execution must
        be ommited.
    :cvar ABORTED: The execution was aborted.
    """

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_COMPLETED = "NOT_COMPLETED"
    ABORTED = "ABORTED"


class MeasureKind(Enum):
    REAL = "REAL"
    BOOL = "BOOL"
    INTEGER = "INTEGER"
    STRING = "STRING"
    DATETIME = "DATETIME"


@dataclass
class AddressType:
    """
    Represents a physical address.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    street: Optional[str] = field(
        default=None,
        metadata={
            "name": "Street",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    state: Optional[str] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    zip: Optional[str] = field(
        default=None,
        metadata={
            "name": "Zip",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )


@dataclass
class CharacteristicType:
    """A characteristic is a generic container of information that can be attached
    to many elements of the model.

    Each characteristic is identified by a FullName that must be unique
    for its owner. It stores its value in a Value element.
    Characteristics are unique among siblings by their FullName
    property. A characteristic is uniquely identified by the combination
    of its owner’s identifier and its FullName
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    full_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FullName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 434,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
            "max_length": 2000,
        },
    )


@dataclass
class DocumentType:
    """A document defines a link to an external file.

    This document is uniquely identified by its Identifier. The document
    also has an optional Name attribute which is meant to contain a
    human-friendly identifier, and a FileName attribute. The FileName is
    used to identify the type of document and should contain an
    extension so that the appropriate application is launched when the
    user requests to view the document content. An optional Description
    can also be specified. Documents are unique among siblings by their
    Identifier property.  This makes it possible for two different
    entities (ex: two different product units) to refer to the same
    document.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Identifier",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
            "max_length": 600,
        },
    )


@dataclass
class ProductUnitUniqueIdentifierType:
    """
    This type contains all the fields required to uniquely identify a product unit.

    :ivar custom_data:
    :ivar product_full_name: The product full name of the product unit.
    :ivar product_unit_identifier: The product unit identifier of the
        product unit.
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


@dataclass
class UserCommentType:
    """Represents a comment made by a user at a given time.

    Note that a user comment is considered unique when the comment, user
    and time are equal for a given associated fact.  For example, if two
    failures have the same comment, user and time, they will be
    considered as two different comments because they are not attached
    to the same failure.  But if two xmls are received by the DIT and
    they contain the same comment, user and time for the same failure
    ID, then they will be considered the same comment and the second
    comment will be discarded silently by the DIT.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
            "required": True,
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
    time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Time",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )


@dataclass
class CustomerType:
    """Represents customer's informations.

    A customer is uniquely identified by its CustomerId.
    """

    address: Optional[AddressType] = field(
        default=None,
        metadata={
            "name": "Address",
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
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        },
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        },
    )
    phone_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PhoneNumber",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 30,
        },
    )
    email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "EmailAddress",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )
    company_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CompanyName",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 50,
        },
    )
