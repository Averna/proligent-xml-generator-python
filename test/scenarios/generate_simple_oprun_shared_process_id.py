from __future__ import annotations

import datetime
from pathlib import Path

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


def generate_simple_oprun_shared_process_id(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:
    default_start_timestamp = start_timestamp or datetime.datetime(2024, 1, 2, 9, 0, 0)
    generation_time = start_timestamp or _default_tz_datetime(default_start_timestamp, 1, 0)
    start_timestamp = start_timestamp or default_start_timestamp

    util_original = model.UTIL
    model.UTIL = Util(timezone="America/New_York")
    try:
        process_start = _default_tz_datetime(start_timestamp, 0, 0)
        process_end = _default_tz_datetime(start_timestamp, 0, 25)
        sequence_start = _default_tz_datetime(start_timestamp, 0, 5)
        sequence_end = _default_tz_datetime(start_timestamp, 0, 18)

        continuity_time = _default_tz_datetime(start_timestamp, 0, 6, 0)
        torque_time = _default_tz_datetime(start_timestamp, 0, 9, 15)
        firmware_time = _default_tz_datetime(start_timestamp, 0, 12, 30)
        label_time = _default_tz_datetime(start_timestamp, 0, 15, 45)

        warehouse = DataWareHouse(
            generation_time=generation_time,
        )

        # Keep these values aligned with simple_oprun_normal_order so ProcessRunId matches.
        product_unit = warehouse.set_product_unit(ProductUnit(
            product_unit_identifier="PU-001",
            product_full_name="PythonLibrary/Product/simple_oprun_normal_order",
        ))
        product_unit.add_characteristic(Characteristic(full_name="Serial", value="PU-001"))

        process = warehouse.set_process_run(ProcessRun(
            name="PythonLibrary/Process/simple_oprun_shared_process_id",
            process_mode="PROD",
            product_unit_identifier="PU-001",
            product_full_name="PythonLibrary/Product/simple_oprun_normal_order",
            start_time=process_start,
        ))

        operation = process.add_operation_run(OperationRun(
            name="Operation/ExtendedValidation",
            station="PythonLibrary/Station/simple_oprun_shared_process_id",
            user="operator_b",
            start_time=process_start,
        ))
        operation.add_characteristic(Characteristic(full_name="Lot", value="L-9001"))
        operation.add_document(
            Document(
                file_name="ValidationPacket.pdf",
                name="Validation Packet",
                description="Evidence package for extended validation operation",
            )
        )

        sequence = operation.add_sequence_run(SequenceRun(
            name="Sequence/Secondary",
            version="2.1",
            start_time=sequence_start,
            user="operator_b",
        ))

        sequence.add_step_run(
            StepRun(
                name="Continuity",
                status=ExecutionStatusKind.PASS,
                start_time=continuity_time,
                end_time=continuity_time,
                measure=Measure(
                    value=True,
                    time=continuity_time,
                    status=ExecutionStatusKind.PASS,
                ),
                characteristics=[Characteristic(full_name="Fixture", value="FX-7")],
            )
        )

        sequence.add_step_run(
            StepRun(
                name="TorqueAudit",
                status=ExecutionStatusKind.PASS,
                start_time=torque_time,
                end_time=torque_time,
                measure=Measure(
                    value=5.8,
                    time=torque_time,
                    unit="Nm",
                    symbol="Nm",
                    status=ExecutionStatusKind.PASS,
                    limit=Limit(
                        LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
                        lower_bound=5.5,
                        higher_bound=6.1,
                    ),
                ),
            )
        )

        sequence.add_step_run(
            StepRun(
                name="FirmwareCheck",
                status=ExecutionStatusKind.PASS,
                start_time=firmware_time,
                end_time=firmware_time,
                measure=Measure(
                    value="FW-1.2.3",
                    time=firmware_time,
                    status=ExecutionStatusKind.PASS,
                ),
            )
        )

        sequence.add_step_run(
            StepRun(
                name="LabelScan",
                status=ExecutionStatusKind.PASS,
                start_time=label_time,
                end_time=label_time,
                measure=Measure(
                    value=1001,
                    time=label_time,
                    status=ExecutionStatusKind.PASS,
                ),
                documents=[
                    Document(
                        file_name="LabelImage.png",
                        name="Label Image",
                        description="Captured label image for traceability",
                    )
                ],
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
