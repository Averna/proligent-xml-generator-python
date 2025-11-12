from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from proligent.datawarehouse.datawarehouse_model import CustomDataType

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


class CharacteristicKind(Enum):
    PRODUCT_UNIT = "ProductUnit"
    OPERATION_RUN = "OperationRun"
    SEQUENCE_RUN = "SequenceRun"
    STEP_RUN = "StepRun"
    FAILURE = "Failure"
    DEFECT = "Defect"


@dataclass
class MappedCharacteristicsType:
    """
    :ivar custom_data:
    :ivar type_value: The Model element type to which the Mapping is
        created
    :ivar dwcharacteristic_name: The characteristic name to include in
        the CUBE as a dimension
    """

    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
    type_value: Optional[CharacteristicKind] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "required": True,
        },
    )
    dwcharacteristic_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DWCharacteristicName",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 434,
        },
    )


@dataclass
class CubeCharacteristicsMappingType:
    """The Proligent OLAP database only support slicing and dicing on a finite
    number of characteristics for each known kind.

    The available number is determined prior to installation. It can be
    looked up in the T_APPLICATION_CHARACTERISTIC_CONFIG table. For each
    CharacteristicKind a enumeration of specified Characteristic name
    can be provide to include them in the OLAP database as dimension
    making the slicable and diceable.

    :ivar mapped_characteristics: Defines a characteristic name to Map
        and make accessible in the CUBE filters database.
    :ivar custom_data:
    """

    mapped_characteristics: List[MappedCharacteristicsType] = field(
        default_factory=list,
        metadata={
            "name": "MappedCharacteristics",
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
class ApplicationConfigType:
    """
    :ivar cube_characteristics_mapping: Proligent configurable
        parameters.
    :ivar custom_data:
    """

    cube_characteristics_mapping: Optional[CubeCharacteristicsMappingType] = (
        field(
            default=None,
            metadata={
                "name": "CubeCharacteristicsMapping",
                "type": "Element",
                "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
            },
        )
    )
    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.averna.com/products/proligent/analytics/DIT/6.85",
        },
    )
