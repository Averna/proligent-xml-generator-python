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


def generate_readme_example1(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:
    frozen_timestamp = start_timestamp or DEFAULT_FROZEN_TIMESTAMP
    with mock_util_timezone("Europe/Paris"), mock_datetime_now(frozen_timestamp):
        limit = Limit(LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND, lower_bound=10, higher_bound=25)
        measure = Measure(
            value=15,
            status=ExecutionStatusKind.PASS,
            limit=limit,
            time=frozen_timestamp
        )
        step = StepRun(
            name='Step1',
            status=ExecutionStatusKind.PASS,
            measure=measure,
            start_time=frozen_timestamp,
            end_time=frozen_timestamp
        )
        sequence = SequenceRun(
            name='Sequence1',
            station='Station/readme_example1',
            status=ExecutionStatusKind.PASS,
            start_time=frozen_timestamp,
            end_time=frozen_timestamp,
            steps=[step],
        )
        operation = OperationRun(
            name='Operation1',
            station='Station/readme_example1',
            status=ExecutionStatusKind.PASS,
            start_time=frozen_timestamp,
            end_time=frozen_timestamp,
            sequences=[sequence],
        )
        process = ProcessRun(
            product_unit_identifier='DutSerialNumber',
            product_full_name='Product/readme_example1',
            operations=[operation],
            name='Process/readme_example1',
            process_mode='PROD',
            status=ExecutionStatusKind.PASS,
            start_time=frozen_timestamp,
            end_time=frozen_timestamp,
        )
        product = ProductUnit(
            product_unit_identifier='DutSerialNumber',
            product_full_name='Product/readme_example1',
            manufacturer='Averna'
        )
        warehouse = DataWareHouse(
            top_process=process,
            product_unit=product,
            generation_time=frozen_timestamp,
        )
        warehouse.save_xml(output_path)
    return output_path
