from dataclasses import dataclass, field
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime

from proligent.datawarehouse.datawarehouse_application_config_xsd import (
    ApplicationConfigType,
)
from proligent.datawarehouse.datawarehouse_assembly_xsd import (
    AssemblyRuleType,
    AssemblyTraceType,
)
from proligent.datawarehouse.datawarehouse_component_unit import ComponentUnitType
from proligent.datawarehouse.datawarehouse_event_xsd import EventType
from proligent.datawarehouse.datawarehouse_failure import (
    DefectType,
    FailureType,
)
from proligent.datawarehouse.datawarehouse_model import (
    CustomDataType,
    CustomerType,
)
from proligent.datawarehouse.datawarehouse_process_run import ProcessRunType
from proligent.datawarehouse.datawarehouse_product_unit import ProductUnitType
from proligent.datawarehouse.datawarehouse_product_unit_return import (
    ProductUnitReturnType,
)
from proligent.datawarehouse.datawarehouse_sequence_run import StandaloneSequenceRunType
from proligent.datawarehouse.datawarehouse_shipment import ShipmentType
from proligent.datawarehouse.datawarehouse_tracked_component_unit_xsd import (
    TrackedComponentUnitType,
)

__NAMESPACE__ = "http://www.averna.com/products/proligent/analytics/DIT/6.85"


@dataclass
class ProligentDatawarehouse:
    """
    :ivar defect:
    :ivar failure:
    :ivar top_process_run:
    :ivar product_unit:
    :ivar customer:
    :ivar product_unit_return:
    :ivar component_unit:
    :ivar shipment:
    :ivar assembly_trace:
    :ivar assembly_rule:
    :ivar event:
    :ivar sequence_run:
    :ivar tracked_component_unit:
    :ivar application_config:
    :ivar custom_data:
    :ivar generation_time: Defines the time at which the data was
        generated.  The DIT uses this information to discard information
        if canonical files are processed or received out of order.  For
        example, if file A is generated before file B but B is processed
        before A, in case of conflicting information the data coming
        from B is preserved.  A concrete example is a product unit
        characteristic that would change in both files.
    :ivar data_source_fingerprint: The information contained in this
        attribute is used to protect the data warehouse from the
        injection of the same file more than once.  The rule is that all
        files that contain the same fingerprint as a file that has
        already been processed successfully by the DIT will be rejected.
        For example, if the file contains information about a product
        unit, a good value for the fingerprint would be the product unit
        serial number followed by the generation date of the XSD. If the
        attribute is ommited, the DIT will generate a random
        fingerprint.  The result is that it will now be possible to
        inject the same file more than once.
    :ivar integration_meta_data: The information contained in this
        attribute is saved in the data warehouse as is.  It can be used
        by the integrator to add some meta data that will help him later
        to troubleshoot his integration.  This meta data is stored in
        the F_INTEGRATION_METADATA column of the T_FACT_DELIVERY_SOURCE
        table.
    """

    class Meta:
        name = "Proligent.Datawarehouse"
        namespace = "http://www.averna.com/products/proligent/analytics/DIT/6.85"

    defect: List[DefectType] = field(
        default_factory=list,
        metadata={
            "name": "Defect",
            "type": "Element",
        },
    )
    failure: List[FailureType] = field(
        default_factory=list,
        metadata={
            "name": "Failure",
            "type": "Element",
        },
    )
    top_process_run: List[ProcessRunType] = field(
        default_factory=list,
        metadata={
            "name": "TopProcessRun",
            "type": "Element",
        },
    )
    product_unit: List[ProductUnitType] = field(
        default_factory=list,
        metadata={
            "name": "ProductUnit",
            "type": "Element",
        },
    )
    customer: List[CustomerType] = field(
        default_factory=list,
        metadata={
            "name": "Customer",
            "type": "Element",
        },
    )
    product_unit_return: List[ProductUnitReturnType] = field(
        default_factory=list,
        metadata={
            "name": "ProductUnitReturn",
            "type": "Element",
        },
    )
    component_unit: List[ComponentUnitType] = field(
        default_factory=list,
        metadata={
            "name": "ComponentUnit",
            "type": "Element",
        },
    )
    shipment: List[ShipmentType] = field(
        default_factory=list,
        metadata={
            "name": "Shipment",
            "type": "Element",
        },
    )
    assembly_trace: List[AssemblyTraceType] = field(
        default_factory=list,
        metadata={
            "name": "AssemblyTrace",
            "type": "Element",
        },
    )
    assembly_rule: List[AssemblyRuleType] = field(
        default_factory=list,
        metadata={
            "name": "AssemblyRule",
            "type": "Element",
        },
    )
    event: List[EventType] = field(
        default_factory=list,
        metadata={
            "name": "Event",
            "type": "Element",
        },
    )
    sequence_run: List[StandaloneSequenceRunType] = field(
        default_factory=list,
        metadata={
            "name": "SequenceRun",
            "type": "Element",
        },
    )
    tracked_component_unit: List[TrackedComponentUnitType] = field(
        default_factory=list,
        metadata={
            "name": "TrackedComponentUnit",
            "type": "Element",
        },
    )
    application_config: List[ApplicationConfigType] = field(
        default_factory=list,
        metadata={
            "name": "ApplicationConfig",
            "type": "Element",
        },
    )
    custom_data: Optional[CustomDataType] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
        },
    )
    generation_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "GenerationTime",
            "type": "Attribute",
            "required": True,
            "min_inclusive": XmlDateTime(1900, 1, 1, 0, 0, 0, 0, 0),
            "max_exclusive": XmlDateTime(2100, 1, 1, 0, 0, 0, 0, 0),
        },
    )
    data_source_fingerprint: Optional[str] = field(
        default=None,
        metadata={
            "name": "DataSourceFingerprint",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 448,
        },
    )
    integration_meta_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "IntegrationMetaData",
            "type": "Attribute",
            "max_length": 2000,
        },
    )
