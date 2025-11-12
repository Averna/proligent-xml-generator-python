from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_model import CustomDataType

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class EventContext:
    """Defines the context in which an event occured.

    This fact cannot be updated.

    :ivar custom_data:
    :ivar time: The timestamp at which the event occured
    :ivar station_full_name: Full name of the station where the event
        occured. If a hierarchy exists, the full name must contain the
        fully qualified name, each level being separated by a forward
        slash ("/").
    :ivar user: Defines the user that generated the event.
    :ivar host_name: Defines the host name (computer name) where the
        event occured.
    :ivar application: Defines the application that generated the event.
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
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
    user: Optional[str] = field(
        default=None,
        metadata={
            "name": "User",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    host_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "HostName",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )
    application: Optional[str] = field(
        default=None,
        metadata={
            "name": "Application",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 255,
        },
    )


@dataclass
class EventTarget:
    """
    Defines the business entity (target) of an event.
    """

    sequence: Optional["EventTarget.Sequence"] = field(
        default=None,
        metadata={
            "name": "Sequence",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    operation: Optional["EventTarget.Operation"] = field(
        default=None,
        metadata={
            "name": "Operation",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    process: Optional["EventTarget.Process"] = field(
        default=None,
        metadata={
            "name": "Process",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    product: Optional["EventTarget.Product"] = field(
        default=None,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    product_unit: Optional["EventTarget.ProductUnit"] = field(
        default=None,
        metadata={
            "name": "ProductUnit",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    station: Optional["EventTarget.Station"] = field(
        default=None,
        metadata={
            "name": "Station",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    user: Optional["EventTarget.User"] = field(
        default=None,
        metadata={
            "name": "User",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    failure: Optional["EventTarget.Failure"] = field(
        default=None,
        metadata={
            "name": "Failure",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )

    @dataclass
    class Sequence:
        """
        :ivar custom_data:
        :ivar sequence_full_name: Full name of the target sequence
            affected by the event. If a hierarchy exists, the full name
            must contain the fully qualified name, each level being
            separated by a forward slash ("/").
        :ivar sequence_version: Defines the sequence's version for this
            sequence run. This field is optional to support non-
            versionable Sequences. The version string must be string-
            comparable to support ordering by version.
        """

        custom_data: Optional[CustomDataType] = field(
            default=None,
            metadata={
                "name": "CustomData",
                "type": "Element",
                "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            },
        )
        sequence_full_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "SequenceFullName",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 1986,
                "pattern": r"([^/\s][^/]{0,263}){0,1}[^/\s](/([^/\s][^/]{0,263}){0,1}[^/\s])*",
            },
        )
        sequence_version: Optional[str] = field(
            default=None,
            metadata={
                "name": "SequenceVersion",
                "type": "Attribute",
                "min_length": 1,
                "max_length": 64,
            },
        )

    @dataclass
    class Operation:
        """
        :ivar custom_data:
        :ivar operation_name: Name of the target operation affected by
            the event.
        """

        custom_data: Optional[CustomDataType] = field(
            default=None,
            metadata={
                "name": "CustomData",
                "type": "Element",
                "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            },
        )
        operation_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "OperationName",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 255,
            },
        )

    @dataclass
    class Process:
        """
        :ivar custom_data:
        :ivar process_full_name: Full name of the target process
            affected by the event. If a hierarchy exists, the full name
            must contain the fully qualified name, each level being
            separated by a forward slash ("/").
        :ivar process_version: Version of the target process of the
            event.
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
                "max_length": 1950,
                "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
            },
        )
        process_version: Optional[str] = field(
            default=None,
            metadata={
                "name": "ProcessVersion",
                "type": "Attribute",
                "max_length": 65,
            },
        )

    @dataclass
    class Product:
        """
        :ivar custom_data:
        :ivar product_full_name: Full name of the target product
            affected by the event. If a hierarchy exists, the full name
            must contain the fully qualified name, each level being
            separated by a forward slash ("/").
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

    @dataclass
    class ProductUnit:
        """
        :ivar custom_data:
        :ivar product_full_name: Full name of the target product of the
            product unit affected by the event. If a hierarchy exists,
            the full name must contain the fully qualified name, each
            level being separated by a forward slash ("/").
        :ivar product_unit_identifier: Defines the unique identifier for
            the product unit affected by the event. The Serial Number is
            often used for this purpose.
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
    class Station:
        """
        :ivar custom_data:
        :ivar station_full_name: Full name of the target station
            affected by the event. If a hierarchy exists, the full name
            must contain the fully qualified name, each level being
            separated by a forward slash ("/").
        """

        custom_data: Optional[CustomDataType] = field(
            default=None,
            metadata={
                "name": "CustomData",
                "type": "Element",
                "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            },
        )
        station_full_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "StationFullName",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 1950,
                "pattern": r"([^/\s][^/]{0,64}){0,1}[^/\s](/([^/\s][^/]{0,64}){0,1}[^/\s])*",
            },
        )

    @dataclass
    class User:
        """
        :ivar custom_data:
        :ivar user_name: Name of the user affected by the event.
        """

        custom_data: Optional[CustomDataType] = field(
            default=None,
            metadata={
                "name": "CustomData",
                "type": "Element",
                "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            },
        )
        user_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "UserName",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 255,
            },
        )

    @dataclass
    class Failure:
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


@dataclass
class EventType:
    """
    Defines an occurence of an event.

    :ivar context: Defines the contextual information about the event.
    :ivar target: Defines the target (businness entity) of the event.
    :ivar detail:
    :ivar custom_data:
    :ivar event_id: Defines a globally unique identifier for the event.
        Any other events with the same EventId will be rejected.
    :ivar action: Defines the action applied to the target.
    :ivar comment: Defines the comment entered by the user when the
        event occured.
    """

    context: Optional[EventContext] = field(
        default=None,
        metadata={
            "name": "Context",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
        },
    )
    target: Optional[EventTarget] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
        },
    )
    detail: List["EventType.Detail"] = field(
        default_factory=list,
        metadata={
            "name": "Detail",
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
    event_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "EventId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    action: Optional[str] = field(
        default=None,
        metadata={
            "name": "Action",
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 4000,
        },
    )

    @dataclass
    class Detail:
        """
        :ivar value:
        :ivar property: Defines an affected property on the target of
            the event. (e.g.: Name, Description, Characteristic, etc...)
        """

        value: str = field(
            default="",
            metadata={
                "required": True,
                "min_length": 1,
                "max_length": 4000,
            },
        )
        property: Optional[str] = field(
            default=None,
            metadata={
                "name": "Property",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 30,
            },
        )
