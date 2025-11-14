from __future__ import annotations

import datetime
from pathlib import Path

import pytz

from proligent import model
from proligent.model import (
    Characteristic,
    DataWareHouse,
    Document,
    ExecutionStatusKind,
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


def _default_tz_datetime(start_timestamp: datetime.datetime, hour: int, minute: int, second: int = 0) -> datetime.datetime:
    return start_timestamp + datetime.timedelta(hours=hour, minutes=minute, seconds=second)


def generate_simple_oprun_normal_order(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:
    tz = pytz.timezone("America/New_York")
    default_start_timestamp = start_timestamp or tz.localize(datetime.datetime(2024, 1, 1, 0, 0, 0))
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

        warehouse = DataWareHouse(
            generation_time=generation_time,
        )

        product_unit = warehouse.set_product_unit(ProductUnit(
            product_unit_identifier="PU-001",
            product_full_name="PythonLibrary/Product/simple_oprun_normal_order",
        ))
        product_unit.add_characteristic(Characteristic(full_name="Serial", value="PU-001"))
        product_unit.add_document(
            Document(
                file_name="ProductCertificate.pdf",
                name="Certificate of Conformance",
                description="Certification for product PU-001",
            )
        )

        process = warehouse.set_process_run(ProcessRun(
            name="PythonLibrary/Process/simple_oprun_normal_order",
            process_mode="PROD",
            product_unit_identifier="PU-001",
            product_full_name="PythonLibrary/Product/simple_oprun_normal_order",
            start_time=process_start,
        ))

        operation = process.add_operation_run(OperationRun(
            name="Operation/Example",
            station="PythonLibrary/Station/simple_oprun_normal_order",
            user="operator",
            start_time=process_start,
        ))
        operation.add_characteristic(Characteristic(full_name="Batch", value="B-42"))
        operation.add_document(
            Document(
                file_name="OperationReport.pdf",
                name="Operation Report",
                description="Summary for operation Operation/Example",
            )
        )

        sequence = operation.add_sequence_run(SequenceRun(
            name="Sequence/Main",
            version="1.0",
            start_time=sequence_start,
        ))
        sequence.add_characteristic(Characteristic(full_name="SequenceType", value="Main"))
        sequence.add_document(
            Document(
                file_name="SequenceChecklist.pdf",
                name="Sequence Checklist",
                description="Checklist completed before running the sequence",
            )
        )

        sequence.add_step_run(
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
                characteristics=[Characteristic(full_name="Channel", value="A")],
                documents=[
                    Document(
                        file_name="InspectionReport.pdf",
                        name="Inspection Report",
                        description="Results for the inspection step",
                    )
                ],
            )
        )

        sequence.add_step_run(
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
            )
        )

        sequence.add_step_run(
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
            )
        )

        sequence.add_step_run(
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
            )
        )

        sequence.add_step_run(
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
            )
        )

        sequence.complete(
            status=ExecutionStatusKind.PASS,
            end_time=sequence_end,
        )

        operation.complete(
            status=ExecutionStatusKind.PASS,
            end_time=process_end,
        )

        process.complete(
            status=ExecutionStatusKind.PASS,
            end_time=process_end,
        )
        warehouse.save_xml(output_path)
    finally:
        model.UTIL = util_original

    return output_path
