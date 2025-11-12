from datawarehouse.datawarehouse import ProligentDatawarehouse
from datawarehouse.datawarehouse_process_run import ProcessRunType
from datawarehouse.datawarehouse_operation_run import OperationRunType
from datawarehouse.datawarehouse_sequence_run import SequenceRunType
from datawarehouse.datawarehouse_step_run import StepRunType
from datawarehouse.datawarehouse_measure import MeasureType
from datawarehouse.datawarehouse_model import (
    ExecutionStatusKind,
    MeasureKind,
    CustomDataType,
)
from datawarehouse.datawarehouse_product_unit import ProductUnitType
import datetime
import pytz
import uuid
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from enum import Enum


class ProligentProcessor:

    def __init__(self, timezone: str = "Europe/Paris"):
        """
        Initializes a new instance of the ProligentProcessor class.

        Args:
            dataset_metadata (str, optional): Metadata for the dataset. Defaults to None.
        """
        self.timezone = timezone
        self.dataset = ProligentDatawarehouse()
        self.dataset.generation_time = self.format_datetime()
        self.dataset.data_source_fingerprint = str(uuid.uuid4())
        self.dataset.top_process_run = []
        self.dataset.product_unit = []

    def format_datetime(self, date_time: datetime = None) -> str:
        """
        Formats the given datetime object to a string representation with microseconds and timezone offset.

        Args:
            datetime (datetime, optional): The datetime object to be formatted. If not provided, the current time will be used.

        Returns:
            str: The formatted datetime string.

        """
        if date_time is None:
            date_time = datetime.datetime.now()
        # Define the timezone you want to use, e.g., 'Europe/Paris' for +02:00
        timezone = pytz.timezone(self.timezone)
        # Localize the current time to the specified timezone
        localized_time = timezone.localize(date_time)
        # Format the time string to include microseconds and timezone offset
        formatted_time = localized_time.isoformat()
        return formatted_time

    def create_process_run(self) -> ProcessRunType:
        """
        Creates a new process run.

        Returns:
            ProcessRunType: The newly created process run.
        """
        process_run = ProcessRunType()
        return process_run

    def update_process_run_properties(
        self,
        process_run: ProcessRunType,
        name: str = "Generic_Process",
        version: str = "1.0.0",
        product_unit_identifier: str = "Generic_Product_Unit",
        product_full_name: str = "Generic_Product",
        status: ExecutionStatusKind = ExecutionStatusKind.PASS,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        mode: str = "Generic_Process_Mode",
    ):
        """
        Updates the properties of a process run.

        Args:
            process_run (ProcessRunType): The process run object to update.
            name (str, optional): The name of the process. Defaults to "Generic_Process".
            version (str, optional): The version of the process. Defaults to "1.0.0".
            product_unit_identifier (str, optional): The identifier of the product unit. Defaults to "Generic_Product_Unit".
            product_full_name (str, optional): The full name of the product. Defaults to "Generic_Product".
            status (ExecutionStatusKind, optional): The execution status of the process run. Defaults to ExecutionStatusKind.PASS.
            start_time (datetime.datetime, optional): The start time of the process run. Defaults to None.
            end_time (datetime.datetime, optional): The end time of the process run. Defaults to None.
            mode (str, optional): The mode of the process. Defaults to "Generic_Process_Mode".
        """
        if start_time is None:
            start_time = self.format_datetime()
        else:
            start_time = self.format_datetime(start_time)
        if end_time is None:
            end_time = self.format_datetime()
        else:
            end_time = self.format_datetime(end_time)
        process_run.process_run_id = str(uuid.uuid4())
        process_run.process_full_name = name
        process_run.process_version = version
        process_run.product_unit_identifier = product_unit_identifier
        process_run.product_full_name = product_full_name
        process_run.process_run_status = status
        process_run.process_run_start_time = start_time
        process_run.process_run_end_time = end_time
        process_run.process_mode = mode
        process_run.operation_run = []

    def append_top_process_run_to_dataset(self, process_run: ProcessRunType):
        """
        Adds the given process_run as the top_process_run in the dataset.

        Args:
            process_run (ProcessRunType): The process_run to be added.

        Returns:
            None
        """
        self.dataset.top_process_run.append(process_run)

    def create_operation_run(self) -> OperationRunType:
        """
        Creates and returns an instance of OperationRunType.

        Returns:
            An instance of OperationRunType.
        """
        operation_run = OperationRunType()
        return operation_run

    def update_operation_run_properties(
        self,
        operation_run: OperationRunType,
        name: str = "Generic_Operation",
        process_full_name: str = "Generic_Process",
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        user: str = "Generic_User",
        status: ExecutionStatusKind = ExecutionStatusKind.PASS,
        station_full_name: str = "Generic_Station",
        process_version: str = "1.0.0",
    ):
        """
        Updates the properties of an operation run.

        Args:
            operation_run (OperationRunType): The operation run to update.
            name (str, optional): The name of the operation. Defaults to "Generic_Operation".
            process_full_name (str, optional): The full name of the process. Defaults to "Generic_Process".
            start_time (datetime.datetime, optional): The start time of the operation run. Defaults to None.
            end_time (datetime.datetime, optional): The end time of the operation run. Defaults to None.
            user (str, optional): The user associated with the operation run. Defaults to "Generic_User".
            status (ExecutionStatusKind, optional): The status of the operation run. Defaults to ExecutionStatusKind.PASS.
            station_full_name (str, optional): The full name of the station. Defaults to "Generic_Station".
            process_version (str, optional): The version of the process. Defaults to "1.0.0".
        """
        if start_time is None:
            start_time = self.format_datetime()
        else:
            start_time = self.format_datetime(start_time)
        if end_time is None:
            end_time = self.format_datetime()
        else:
            end_time = self.format_datetime(end_time)
        operation_run.process_full_name = process_full_name
        operation_run.operation_name = name
        operation_run.operation_run_start_time = start_time
        operation_run.operation_run_end_time = end_time
        operation_run.user = user
        operation_run.operation_status = status
        operation_run.calling_operation_run_id = str(uuid.uuid4())
        operation_run.station_full_name = station_full_name
        operation_run.process_version = process_version
        operation_run.sequence_run = []

    def append_operation_run_to_process_run(
        self, process_run: ProcessRunType, operation_run: OperationRunType
    ):
        """
        Appends an operation run to a process run.

        Args:
            process_run (ProcessRunType): The process run to which the operation run will be appended.
            operation_run (OperationRunType): The operation run to be appended.

        Returns:
            None
        """
        process_run.operation_run.append(operation_run)

    def create_sequence_run(self) -> SequenceRunType:
        """
        Creates a new sequence run.

        Returns:
            A SequenceRunType object representing the newly created sequence run.
        """
        sequence_run = SequenceRunType()
        return sequence_run

    def update_sequence_run_properties(
        self,
        sequence_run: SequenceRunType,
        name: str = "Generic_Sequence",
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        status: ExecutionStatusKind = ExecutionStatusKind.PASS,
        sequence_full_name: str = "Generic_Sequence",
        sequence_version: str = "1.0.0",
        sequence_mode: str = "Generic_Sequence_Mode",
        station_name: str = "Generic_Station",
    ):
        """
        Updates the properties of a sequence run.

        Args:
            sequence_run (SequenceRunType): The sequence run object to update.
            name (str, optional): The name of the sequence. Defaults to "Generic_Sequence".
            start_time (datetime.datetime, optional): The start time of the sequence run. Defaults to None.
            end_time (datetime.datetime, optional): The end time of the sequence run. Defaults to None.
            status (ExecutionStatusKind, optional): The status of the sequence run. Defaults to ExecutionStatusKind.PASS.
            sequence_full_name (str, optional): The full name of the sequence. Defaults to "Generic_Sequence".
            sequence_version (str, optional): The version of the sequence. Defaults to "1.0.0".
            sequence_mode (str, optional): The mode of the sequence. Defaults to "Generic_Sequence_Mode".
            station_name (str, optional): The name of the station. Defaults to "Generic_Station".
        """
        if start_time is None:
            start_time = self.format_datetime()
        else:
            start_time = self.format_datetime(start_time)
        if end_time is None:
            end_time = self.format_datetime()
        else:
            end_time = self.format_datetime(end_time)
        sequence_run.sequence_run_id = str(uuid.uuid4())
        sequence_run.sequence_execution_status = status
        sequence_run.sequence_full_name = name
        sequence_run.start_date = start_time
        sequence_run.station_full_name = station_name
        sequence_run.end_date = end_time
        sequence_run.sequence_full_name = sequence_full_name
        sequence_run.sequence_version = sequence_version
        sequence_run.sequence_mode = sequence_mode
        sequence_run.step_run = []

    def append_sequence_run_to_operation_run(
        self, operation_run: OperationRunType, sequence_run: SequenceRunType
    ):
        """
        Appends a sequence run to an operation run.

        Args:
            operation_run (OperationRunType): The operation run to which the sequence run will be appended.
            sequence_run (SequenceRunType): The sequence run to be appended.

        Returns:
            None
        """
        operation_run.sequence_run.append(sequence_run)

    def create_step_run(self) -> StepRunType:
        """
        Creates a new step run.

        Returns:
            StepRunType: The newly created step run.
        """
        step_run = StepRunType()
        return step_run

    def update_step_run_properties(
        self,
        step_run: StepRunType,
        name: str = "Generic_Step",
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        step_execution_status: ExecutionStatusKind = ExecutionStatusKind.PASS,
    ):
        """
        Updates the properties of a step run.

        Args:
            step_run (StepRunType): The step run object to update.
            name (str, optional): The name of the step. Defaults to "Generic_Step".
            start_time (datetime.datetime, optional): The start time of the step run. Defaults to None.
            end_time (datetime.datetime, optional): The end time of the step run. Defaults to None.
            step_execution_status (ExecutionStatusKind, optional): The execution status of the step run. Defaults to ExecutionStatusKind.PASS.
        """
        if start_time is None:
            start_time = self.format_datetime()
        else:
            start_time = self.format_datetime(start_time)
        if end_time is None:
            end_time = self.format_datetime()
        else:
            end_time = self.format_datetime(end_time)
        step_run.step_run_id = str(uuid.uuid4())
        step_run.step_name = name
        step_run.start_date = start_time
        step_run.end_date = end_time
        step_run.step_execution_status = step_execution_status
        step_run.measure = []

    def append_step_run_to_sequence_run(
        self, sequence_run: SequenceRunType, step_run: StepRunType
    ):
        """
        Appends a step run to a sequence run.

        Args:
            sequence_run (SequenceRunType): The sequence run to which the step run will be appended.
            step_run (StepRunType): The step run to be appended.

        Returns:
            None
        """
        sequence_run.step_run.append(step_run)

    def create_measure(self):
        """
        Creates a new measure.

        Returns:
            MeasureType: The newly created measure.
        """
        measure = MeasureType()
        return measure

    def update_measure_properties(
        self,
        measure: MeasureType,
        unit: str = None,
        symbol: str = None,
        measure_time: datetime.datetime = None,
        measure_execution_status: ExecutionStatusKind = ExecutionStatusKind.PASS,
        comments="Generic_Comments",
    ):
        """
        Update the properties of a measure.

        Args:
            measure (MeasureType): The measure object to update.
            unit (str, optional): The unit of measurement. Defaults to "Generic_Unit".
            measure_time (datetime.datetime, optional): The time of the measurement. If not provided, the current time will be used. Defaults to None.
            measure_execution_status (ExecutionStatusKind, optional): The execution status of the measurement. Defaults to ExecutionStatusKind.PASS.
            comments (str, optional): Additional comments about the measurement. Defaults to "Generic_Comments".
        """
        if measure_time is None:
            measure_time = self.format_datetime()
        else:
            measure_time = self.format_datetime(measure_time)
        measure.measure_id = str(uuid.uuid4())
        measure.measure_time = measure_time
        measure.unit = unit
        measure.symbol = symbol
        measure.measure_execution_status = measure_execution_status
        measure.comments = comments
        measure.value = MeasureType.Value
        measure.limit = MeasureType.Limit

    def append_measure_to_step_run(self, step_run: StepRunType, measure: MeasureType):
        """
        Appends a measure to a step run.

        Args:
            step_run (StepRunType): The step run to which the measure will be appended.
            measure (MeasureType): The measure to be appended.

        Returns:
            None
        """
        step_run.measure.append(measure)

    def create_real_value(self, value: str):
        """
        Creates a new real value.

        Returns:
            ValueType: The newly created value.
        """

        meas_value = MeasureType.Value()
        meas_value.value = str(value)
        meas_value.type_value = MeasureKind.REAL
        return meas_value

    def create_bool_value(self, value: str):
        """
        Creates a new bool value.

        Returns:
            ValueType: The newly created value.
        """

        meas_value = MeasureType.Value()
        meas_value.value = str(value)
        meas_value.type_value = MeasureKind.BOOL
        return meas_value

    def create_integer_value(self, value: str):
        """
        Creates a new integer value.

        Returns:
            ValueType: The newly created value.
        """

        meas_value = MeasureType.Value()
        meas_value.value = str(value)
        meas_value.type_value = MeasureKind.INTEGER
        return meas_value

    def create_string_value(self, value: str):
        """
        Creates a new string value.

        Returns:
            ValueType: The newly created value.
        """

        meas_value = MeasureType.Value()
        meas_value.value = str(value)
        meas_value.type_value = MeasureKind.STRING
        return meas_value

    def create_datetime_value(self, value: str):
        """
        Creates a new datetime value.

        Returns:
            ValueType: The newly created value.
        """

        meas_value = MeasureType.Value()
        meas_value.value = str(value)
        meas_value.type_value = MeasureKind.DATETIME
        return meas_value

    def update_value_in_measure(self, measure: MeasureType, value: MeasureType.Value):
        """
        Updates a value in a measure.

        Args:
            measure (MeasureType): The measure to which the value will be appended.
            value (ValueType): The value to be appended.

        Returns:
            None
        """
        measure.value = value

    class LimitExpression(Enum):
        """
        Enumeration of limit expressions.
        """

        LOWERBOUND_LEQ_X_LEQ_HIGHER_BOUND = "LowerBound <= X <= HigherBound"
        LOWERBOUND_LE_X_LEQ_HIGHER_BOUND = "LowerBound < X <= HigherBound"
        LOWERBOUND_LEQ_X_LE_HIGHER_BOUND = "LowerBound <= X < HigherBound"
        LOWERBOUND_LE_X_LE_HIGHER_BOUND = "LowerBound < X < HigherBound"
        LOWERBOUND_LEQ_X = "LowerBound <= X"
        LOWERBOUND_LE_X = "LowerBound < X"
        X_LEQ_HIGHER_BOUND = "X <= HigherBound"
        X_LE_HIGHER_BOUND = "X < HigherBound"
        X_EQ_HIGHER_BOUND = "X == HigherBound"
        X_NEQ_HIGHER_BOUND = "X != HigherBound"
        X_LEQ_LOWERBOUND_OR_HIGHERBOUND_LEQ_X = "X <= LOWERBOUND OR HIGHERBOUND <= X"
        X_LE_LOWERBOUND_or_HIGHERBOUND_LEQ_X = "X < LOWERBOUND or HIGHERBOUND <= X"
        X_LEQ_LOWERBOUND_or_HIGHERBOUND_LE_X = "X <= LOWERBOUND or HIGHERBOUND < X"
        X_LE_LOWERBOUND_or_HIGHERBOUND_LE_X = "X < LOWERBOUND or HIGHERBOUND < X"

    def create_limit(
        self,
        lower_bound: object = None,
        higher_bound: object = None,
        limit_expression: LimitExpression = LimitExpression.LOWERBOUND_LEQ_X_LEQ_HIGHER_BOUND,
    ):
        """
        Creates a new limit.

        Returns:
            LimitType: The newly created limit.
        """
        limit = MeasureType.Limit()
        if limit_expression == self.LimitExpression.LOWERBOUND_LEQ_X_LEQ_HIGHER_BOUND:
            limit.limit_expression = f"{lower_bound} <= X <={higher_bound}"
        elif limit_expression == self.LimitExpression.LOWERBOUND_LE_X_LEQ_HIGHER_BOUND:
            limit.limit_expression = f"{lower_bound} < X <={higher_bound}"
        elif limit_expression == self.LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND:
            limit.limit_expression = f"{lower_bound} <= X < {higher_bound}"
        elif limit_expression == self.LimitExpression.LOWERBOUND_LE_X_LE_HIGHER_BOUND:
            limit.limit_expression = f"{lower_bound} < X < {higher_bound}"
        elif limit_expression == self.LimitExpression.LOWERBOUND_LEQ_X:
            limit.limit_expression = f"{lower_bound} <= X"
        elif limit_expression == self.LimitExpression.LOWERBOUND_LE_X:
            limit.limit_expression = f"{lower_bound} < X"
        elif limit_expression == self.LimitExpression.X_LEQ_HIGHER_BOUND:
            limit.limit_expression = f"X <= {higher_bound}"
        elif limit_expression == self.LimitExpression.X_LE_HIGHER_BOUND:
            limit.limit_expression = f"X < {higher_bound}"
        elif limit_expression == self.LimitExpression.X_EQ_HIGHER_BOUND:
            limit.limit_expression = f"X == {higher_bound}"
        elif limit_expression == self.LimitExpression.X_NEQ_HIGHER_BOUND:
            limit.limit_expression = f"X != {higher_bound}"
        elif (
            limit_expression
            == self.LimitExpression.X_LEQ_LOWERBOUND_OR_HIGHERBOUND_LEQ_X
        ):
            limit.limit_expression = f"X <= {lower_bound} OR {higher_bound} <= X"
        elif (
            limit_expression
            == self.LimitExpression.X_LE_LOWERBOUND_or_HIGHERBOUND_LEQ_X
        ):
            limit.limit_expression = f"X < {lower_bound} or {higher_bound} <= X"
        elif (
            limit_expression
            == self.LimitExpression.X_LEQ_LOWERBOUND_or_HIGHERBOUND_LE_X
        ):
            limit.limit_expression = f"X <= {lower_bound} or {higher_bound} < X"
        elif (
            limit_expression == self.LimitExpression.X_LE_LOWERBOUND_or_HIGHERBOUND_LE_X
        ):
            limit.limit_expression = f"X < {lower_bound} or {higher_bound} < X"
        else:
            raise ValueError("Invalid limit expression")
        return limit

    def update_limit_in_measure(self, measure: MeasureType, limit: MeasureType.Limit):
        """
        Updates a limit in a measure.

        Args:
            measure (MeasureType): The measure to which the limit will be appended.
            limit (LimitType): The limit to be appended.

        Returns:
            None
        """
        measure.limit = limit

    def create_product_unit(self) -> ProductUnitType:
        """
        Creates a new product unit.

        Returns:
            ProductUnitType: The newly created product unit.
        """
        product_unit = ProductUnitType()
        return product_unit

    def update_product_unit_properties(
        self,
        product_unit: ProductUnitType,
        product_unit_identifier: str,
        product_full_name: str,
        scrapped: bool = False,
        scrapped_time: datetime.datetime = None,
        creation_time: datetime.datetime = None,
        manufacturing_time: datetime.datetime = None,
        by_manufacturer: str = "Generic_Manufacturer",
    ):
        """
        Updates the properties of a product unit.

        Args:
            product_unit (ProductUnitType): The product unit object to update.
            product_unit_identifier (str): The identifier of the product unit.
            product_full_name (str): The full name of the product.
            scrapped (bool): A boolean value indicating whether the product unit has been scrapped.
            scrapped_time (datetime.datetime): The time at which the product unit was scrapped.
            creation_time (datetime.datetime): The time at which the product unit was created.
            manufacturing_time (datetime.datetime): The time at which the product unit was manufactured
            by_manufacturer (str): The manufacturer of the product unit.
        """
        if scrapped_time is None:
            scrapped_time = self.format_datetime()
        else:
            scrapped_time = self.format_datetime(scrapped_time)
        if creation_time is None:
            creation_time = self.format_datetime()
        else:
            creation_time = self.format_datetime(creation_time)
        if manufacturing_time is None:
            manufacturing_time = self.format_datetime()
        else:
            manufacturing_time = self.format_datetime(manufacturing_time)
        product_unit.product_unit_identifier = product_unit_identifier
        product_unit.product_full_name = product_full_name
        product_unit.scrapped = scrapped
        product_unit.scrapped_time = scrapped_time
        product_unit.creation_time = creation_time
        product_unit.manufacturing_time = manufacturing_time
        product_unit.by_manufacturer = by_manufacturer

    def append_product_unit_to_dataset(self, product_unit: ProductUnitType):
        """
        Appends a product unit to the dataset's product_unit list.

        Args:
            product_unit (ProductUnitType): The product unit to append.

        Returns:
            None
        """
        self.dataset.product_unit.append(product_unit)

    def save_data_warehouse(self):

        # Initialize the context, parser, and serializer
        context = XmlContext()
        serializer = XmlSerializer(context=context)

        # Serialize the dataclass instance to an XML string
        xml_string = serializer.render(self.dataset)

        print(xml_string)

        # Save the XML string to a file
        filename = "Proligent_" + str(uuid.uuid4()) + ".xml"
        with open(filename, "w") as file:
            file.write(xml_string)
