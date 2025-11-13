from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_failure import FailureReferenceType
from proligent.datawarehouse.datawarehouse_model import (
    CharacteristicType,
    CustomDataType,
    ExecutionStatusKind,
    MeasureKind,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class MeasureType:
    """
    :ivar value: ​Defines the value acquired by the measure. An empty
        value of type STRING will always get stored as NULL, even if the
        empty value is provided. An empty value of any other type is
        invalid. Measures are globaly unique by their MeasureId
        property. Measures are not updatable.
    :ivar limit:
    :ivar characteristic: Defines a characteristic, a key/value pair
        used to store arbitrary information associated to this measure.
        Characteristics are updatable even though the measure itself
        can't be updated.
    :ivar failure_reference:
    :ivar custom_data:
    :ivar measure_id: Defines the measure unique identifier. This ID
        must be unique across step runs.
    :ivar measure_time: Defines the date when the measure was acquired.
    :ivar comments: ​​Defines a comment associated to the measure.
    :ivar unit: ​Defines the name of the unit of the measure value (Ex:
        Kilometer).  When a symbol is provided, the unit becomes
        required.
    :ivar symbol: ​Defines the symbol of the unit for the measure value
        (ex: KM).  When a unit is provided, the symbol becomes required.
    :ivar measure_execution_status: Define the execution status of the
        measure
    """

    value: Optional["MeasureType.Value"] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            "required": True,
        },
    )
    limit: Optional["MeasureType.Limit"] = field(
        default=None,
        metadata={
            "name": "Limit",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    characteristic: List[CharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "Characteristic",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    failure_reference: List[FailureReferenceType] = field(
        default_factory=list,
        metadata={
            "name": "FailureReference",
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
    measure_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeasureId",
            "type": "Attribute",
            "min_length": 1,
            "pattern": r"[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}|\{[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\}|\([A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}\)",
        },
    )
    measure_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "MeasureTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Attribute",
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 30,
        },
    )
    symbol: Optional[str] = field(
        default=None,
        metadata={
            "name": "Symbol",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 20,
        },
    )
    measure_execution_status: Optional[ExecutionStatusKind] = field(
        default=None,
        metadata={
            "name": "MeasureExecutionStatus",
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Value:
        """
        :ivar value:
        :ivar type_value: ​Defines the data type of the value acquired
            by the measure.
        :ivar precision: ​​Defines the numeric precision of the measure
            value. Only valid for values of type REAL.
        """

        value: str = field(
            default="",
            metadata={
                "required": True,
                "max_length": 4000,
            },
        )
        type_value: Optional[MeasureKind] = field(
            default=None,
            metadata={
                "name": "Type",
                "type": "Attribute",
                "required": True,
            },
        )
        precision: Optional[int] = field(
            default=None,
            metadata={
                "name": "Precision",
                "type": "Attribute",
            },
        )

    @dataclass
    class Limit:
        """
        :ivar custom_data:
        :ivar limit_expression: The limit expression associated with the
            measure.  If the expression matches one of the following
            patterns, the lower and higher limits will be extracted and
            stored in the datawarehouse for the reports that use limits.
            Limits not matching the types and patterns below will cause
            a rejection to occur.
            1)  lower_bound &lt;= X &lt;= higher_bound
            2)  lower_bound &lt; X &lt;= higher_bound
            3) lower_bound &lt;= X &lt; higher_bound
            4)  lower_bound &lt; X
            &lt; higher_bound
            5)  lower_bound &lt;= X
            6)  lower_bound &lt; X
            7)  X &lt;= higher_bound
            8)  X &lt; higher_bound
            9)  X == higher_bound
            10) X != higher_bound
            12) X &lt;= lower_bound OR higher_bound &lt;= X
            13) X &lt; lower_bound OR higher_bound &lt;= X
            14) X &lt;= lower_bound OR higher_bound &lt; X
            15) X &lt; lower_bound OR higher_bound

            &lt; X X can be an integer e.g. 3 X can be a real e.g. 3.5 X
            can be a real not a number e.g. NaN X can be a scientific
            int e.g. 2e3 X can be a scientific real e.g. 3.5e-3 X can be
            a DateTime X can be a boolean e.g. 1, true A limit
            expression can also be a string.
        """

        custom_data: Optional[CustomDataType] = field(
            default=None,
            metadata={
                "name": "CustomData",
                "type": "Element",
                "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            },
        )
        limit_expression: Optional[str] = field(
            default=None,
            metadata={
                "name": "LimitExpression",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 2000,
            },
        )
