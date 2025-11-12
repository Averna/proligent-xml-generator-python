from __future__ import annotations

import datetime
from pathlib import Path

import pytz

from proligent import model
from proligent.model import (
    Characteristic,
    DataWareHouse,
    Document,
    Limit,
    LimitExpression,
    Measure,
    OperationRun,
    ProcessRun,
    ProductUnit,
    SequenceRun,
    StepRun,
    Util,
)
from proligent.datawarehouse.datawarehouse_model import ExecutionStatusKind


def _default_tz_datetime(start_timestamp: datetime.datetime, hour: int, minute: int, second: int = 0) -> datetime.datetime:
    return start_timestamp + datetime.timedelta(hours=hour, minutes=minute, seconds=second)


def generate_simple_oprun_reverse_order(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:

    tz = pytz.timezone("America/New_York")
    default_start_timestamp = tz.localize(datetime.datetime(2024, 1, 1, 0, 0, 0))
    generation_time = start_timestamp or _default_tz_datetime(default_start_timestamp, 9, 0)
    start_timestamp = start_timestamp or default_start_timestamp

    util_original = model.UTIL
    model.UTIL = Util(timezone="America/New_York")
    try:
        process_start = _default_tz_datetime(start_timestamp, 8, 0)
        process_end = _default_tz_datetime(start_timestamp, 8, 20)
        sequence_start = _default_tz_datetime(start_timestamp, 8, 10)
        sequence_end = _default_tz_datetime(start_timestamp, 8, 12)

        inspection_time = _default_tz_datetime(start_timestamp, 8, 10, 30)
        count_time = _default_tz_datetime(start_timestamp, 8, 10, 45)
        visual_time = _default_tz_datetime(start_timestamp, 8, 11, 0)
        calibration_time = _default_tz_datetime(start_timestamp, 8, 11, 15)
        notes_time = _default_tz_datetime(start_timestamp, 8, 11, 30)

        steps = [
            StepRun(
                name="Inspection",
                status=ExecutionStatusKind.PASS,
                start_time=inspection_time,
                end_time=inspection_time,
                measure=Measure(
                        value=1.23,
                        time=inspection_time,
                        unit="Volt",
                        symbol="V",
                        status=ExecutionStatusKind.PASS,
                        limit=Limit(
                            LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
                            lower_bound=1.1,
                            higher_bound=1.25
                        ),
                    ),
                characteristics=[
                    Characteristic(full_name="Channel", value="A"),
                ],
                documents=[
                    Document(
                        file_name="InspectionReport.pdf",
                        name="Inspection Report",
                        description="Results for the inspection step",
                    )
                ],
            ),
            StepRun(
                name="CountCheck",
                status=ExecutionStatusKind.PASS,
                start_time=count_time,
                end_time=count_time,
                measure=Measure(
                        value=42,
                        time=count_time,
                        status=ExecutionStatusKind.PASS,
                    ),
            ),
            StepRun(
                name="VisualApproval",
                status=ExecutionStatusKind.PASS,
                start_time=visual_time,
                end_time=visual_time,
                measure=Measure(
                        value=True,
                        time=visual_time,
                        status=ExecutionStatusKind.PASS,
                    ),
            ),
            StepRun(
                name="CalibrationTimestamp",
                status=ExecutionStatusKind.PASS,
                start_time=calibration_time,
                end_time=calibration_time,
                measure=Measure(
                        value=calibration_time,
                        time=calibration_time,
                        unit="Volt",
                        symbol="V",
                        status=ExecutionStatusKind.PASS,
                    ),
            ),
            StepRun(
                name="OperatorNotes",
                status=ExecutionStatusKind.PASS,
                start_time=notes_time,
                end_time=notes_time,
                measure=Measure(
                        value="All checks passed",
                        time=notes_time,
                        status=ExecutionStatusKind.PASS,
                    ),
            ),
        ]

        sequence = SequenceRun(
            name="Sequence/Main",
            version="1.0",
            station="PythonLibrary/Station/simple_oprun_reverse_order",
            user="operator",
            status=ExecutionStatusKind.PASS,
            start_time=sequence_start,
            end_time=sequence_end,
            steps=steps,
            characteristics=[
                Characteristic(full_name="SequenceType", value="Main"),
            ],
            documents=[
                Document(
                    file_name="SequenceChecklist.pdf",
                    name="Sequence Checklist",
                    description="Checklist completed before running the sequence",
                )
            ],
        )

        operation = OperationRun(
            name="Operation/Example",
            station="PythonLibrary/Station/simple_oprun_reverse_order",
            user="operator",
            process_name="PythonLibrary/Process/simple_oprun_reverse_order",
            status=ExecutionStatusKind.PASS,
            start_time=process_start,
            end_time=process_end,
            sequences=[sequence],
            characteristics=[
                Characteristic(full_name="Batch", value="B-42"),
            ],
            documents=[
                Document(
                    file_name="OperationReport.pdf",
                    name="Operation Report",
                    description="Summary for operation Operation/Example",
                )
            ],
        )

        process = ProcessRun(
            name="PythonLibrary/Process/simple_oprun_reverse_order",
            process_mode="PROD",
            product_unit_identifier="PU-001",
            product_full_name="PythonLibrary/Product/simple_oprun_reverse_order",
            status=ExecutionStatusKind.PASS,
            start_time=process_start,
            end_time=process_end,
            operations=[operation],
        )

        product_unit = ProductUnit(
            product_unit_identifier="PU-001",
            product_full_name="PythonLibrary/Product/simple_oprun_reverse_order",
            characteristics=[
                Characteristic(full_name="Serial", value="PU-001"),
            ],
            documents=[
                Document(
                    file_name="ProductCertificate.pdf",
                    name="Certificate of Conformance",
                    description="Certification for product PU-001",
                )
            ],
        )

        warehouse = DataWareHouse(
            top_process=process,
            product_unit=product_unit,
            generation_time=generation_time,
        )

        warehouse.save_xml(output_path)
    finally:
        model.UTIL = util_original

    return output_path
