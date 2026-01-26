from __future__ import annotations

import datetime
from pathlib import Path

from proligent.model import (
    DataWareHouse,
    ExecutionStatusKind,
    Limit,
    LimitExpression,
    Measure,
    OperationRun,
    ProcessRun,
    ProductUnit,
    SequenceRun,
    StepRun,
)
from test.test_mocks import mock_datetime_now, mock_util_timezone

DEFAULT_FROZEN_TIMESTAMP = datetime.datetime(2024, 1, 1, 12, 0, 0)


def generate_readme_example2(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:
    frozen_timestamp = start_timestamp or DEFAULT_FROZEN_TIMESTAMP
    with mock_util_timezone("Europe/Paris"), mock_datetime_now(frozen_timestamp):
        warehouse = DataWareHouse(generation_time=frozen_timestamp)

        product = warehouse.set_product_unit(ProductUnit(
            product_unit_identifier='DutSerialNumber',
            product_full_name='Product/readme_example2',
            manufacturer='Averna'
        ))

        process = warehouse.set_process_run(ProcessRun(
            name='Process/readme_example2',
            process_mode='PROD',
            product_unit_identifier='DutSerialNumber',
            product_full_name='Product/readme_example2',
            start_time=frozen_timestamp,
        ))

        operation = process.add_operation_run(OperationRun(
            name='Operation1',
            station='Station/readme_example2',
            start_time=frozen_timestamp,
        ))

        sequence = operation.add_sequence_run(SequenceRun(
            name='Sequence1',
            start_time=frozen_timestamp,
        ))

        sequence.add_step_run(
            StepRun(
                name="Step1",
                status=ExecutionStatusKind.PASS,
                start_time=frozen_timestamp,
                end_time=frozen_timestamp,
                measure=Measure(
                    value=15,
                    time=frozen_timestamp,
                    status=ExecutionStatusKind.PASS,
                    limit=Limit(
                        LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
                        lower_bound=10,
                        higher_bound=25
                    ),
                )
            )
        )

        sequence.complete(status=ExecutionStatusKind.PASS, end_time=frozen_timestamp)
        operation.complete(status=ExecutionStatusKind.PASS, end_time=frozen_timestamp)
        process.complete(status=ExecutionStatusKind.PASS, end_time=frozen_timestamp)

        warehouse.save_xml(output_path)
    return output_path
