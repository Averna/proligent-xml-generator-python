from __future__ import annotations

import datetime
from pathlib import Path

import pytz

from proligent import model
from proligent.model import (
    DataWareHouse,
    ExecutionStatusKind,
    Measure,
    OperationRun,
    ProcessRun,
    ProductUnit,
    SequenceRun,
    StepRun,
    Util,
)


def _default_tz_datetime(start_timestamp: datetime.datetime, hour: int, minute: int, second: int = 0) -> datetime.datetime:
    return start_timestamp + datetime.timedelta(hours=hour, minutes=minute, seconds=second)


def generate_partial_operation_run(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:
    tz = pytz.timezone("America/Chicago")
    default_start_timestamp = start_timestamp or tz.localize(datetime.datetime(2024, 5, 5, 0, 0, 0))
    generation_time = start_timestamp or _default_tz_datetime(default_start_timestamp, 15, 0)
    start_timestamp = start_timestamp or default_start_timestamp

    util_original = model.UTIL
    model.UTIL = Util(timezone="America/Chicago")
    try:
        process_start = _default_tz_datetime(start_timestamp, 14, 0)

        warehouse = DataWareHouse(
            generation_time=generation_time,
        )

        product_unit = ProductUnit(
            product_unit_identifier="PU-PARTIAL-01",
            product_full_name="PythonLibrary/Product/partial_operation_flow",
        )
        warehouse.set_product_unit(product_unit)

        process = ProcessRun(
            name="PythonLibrary/Process/partial_operation_flow",
            process_mode="AUTO",
            product_unit_identifier="PU-PARTIAL-01",
            product_full_name="PythonLibrary/Product/partial_operation_flow",
            status=ExecutionStatusKind.NOT_COMPLETED,
            start_time=process_start,
        )
        process = warehouse.set_process_run(process)

        operation = OperationRun(
            name="Operation/Partial",
            station="PythonLibrary/Station/partial_operation_flow",
            user="in-progress.operator",
            status=ExecutionStatusKind.NOT_COMPLETED,
            start_time=process_start,
        )
        operation = process.add_operation_run(operation)

        initial_sequence = SequenceRun(
            name="Sequence/Initial",
            version="INIT-1.0",
            user="in-progress.operator",
            status=ExecutionStatusKind.PASS,
            start_time=_default_tz_datetime(start_timestamp, 14, 5),
            end_time=_default_tz_datetime(start_timestamp, 14, 15),
        )
        initial_sequence = operation.add_sequence_run(initial_sequence)

        measure_time = _default_tz_datetime(start_timestamp, 14, 7)
        initial_sequence.add_step_run(
            StepRun(
                name="InitialStep",
                status=ExecutionStatusKind.PASS,
                start_time=measure_time,
                end_time=measure_time,
                measure=Measure(
                    value=42.0,
                    unit="Volt",
                    symbol="V",
                    time=measure_time,
                    status=ExecutionStatusKind.PASS,
                ),
            )
        )

        ongoing_sequence = SequenceRun(
            name="Sequence/Ongoing",
            version="ONGOING-1.0",
            user="in-progress.operator",
            status=ExecutionStatusKind.NOT_COMPLETED,
            start_time=_default_tz_datetime(start_timestamp, 14, 35),
        )
        ongoing_sequence = operation.add_sequence_run(ongoing_sequence)

        ongoing_measure_time = _default_tz_datetime(start_timestamp, 14, 36)
        ongoing_sequence.add_step_run(
            StepRun(
                name="OngoingMeasurement",
                status=ExecutionStatusKind.PASS,
                start_time=ongoing_measure_time,
                end_time=ongoing_measure_time,
                measure=Measure(
                    value="Collecting data",
                    time=ongoing_measure_time,
                    status=ExecutionStatusKind.PASS,
                ),
            )
        )

        warehouse.save_xml(output_path)
    finally:
        model.UTIL = util_original

    return output_path
