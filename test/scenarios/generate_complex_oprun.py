from __future__ import annotations

import datetime
from pathlib import Path

import pytz

from proligent import model
from proligent.datawarehouse.datawarehouse_model import ExecutionStatusKind
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


def _default_tz_datetime(start_timestamp: datetime.datetime, hour: int, minute: int, second: int = 0) -> datetime.datetime:
    return start_timestamp + datetime.timedelta(hours=hour, minutes=minute, seconds=second)


def generate_complex_oprun(
        output_path: Path,
        start_timestamp: datetime.datetime | None = None) -> Path:
    tz = pytz.timezone("America/Bogota")
    default_start_timestamp = start_timestamp or tz.localize(datetime.datetime(2024, 4, 1, 0, 0, 0))
    generation_time = start_timestamp or _default_tz_datetime(default_start_timestamp, 9, 0)
    start_timestamp = start_timestamp or default_start_timestamp

    util_original = model.UTIL
    model.UTIL = Util(timezone="America/Bogota")
    try:
        process_start = _default_tz_datetime(start_timestamp, 7, 0)
        process_end = _default_tz_datetime(start_timestamp, 7, 50)

        functional_start = _default_tz_datetime(start_timestamp, 7, 10)
        functional_end = _default_tz_datetime(start_timestamp, 7, 27)
        safety_start = _default_tz_datetime(start_timestamp, 7, 15)
        safety_end = _default_tz_datetime(start_timestamp, 7, 23)
        diagnostics_start = _default_tz_datetime(start_timestamp, 7, 32)
        diagnostics_end = _default_tz_datetime(start_timestamp, 7, 47)

        warehouse = DataWareHouse(
            generation_time=generation_time,
        )

        warehouse.set_product_unit(ProductUnit(
            product_unit_identifier="PU-COMP-999",
            product_full_name="PythonLibrary/Product/complex_oprun",
            manufacturer='Averna',
            creation_time=process_start,
            manufacturing_time=process_start,
            scrapped=True,
            scrap_time=process_end,
            characteristics=[
                Characteristic(full_name="Variant", value="Ultimate-RevD"),
                Characteristic(full_name="Lot", value="LOT-5566"),
            ],
        ))

        process = warehouse.set_process_run(ProcessRun(
            name="PythonLibrary/Process/complex_oprun",
            process_mode="AUTO",
            product_unit_identifier="PU-COMP-999",
            product_full_name="PythonLibrary/Product/complex_oprun",
            start_time=process_start,
        ))

        operation = process.add_operation_run(OperationRun(
            name="Operation/Comprehensive",
            station="PythonLibrary/Station/complex_oprun",
            user="chief.operator",
            start_time=process_start,
            characteristics=[
                Characteristic(full_name="Shift", value="Night"),
                Characteristic(full_name="Technician", value="Charlie"),
                Characteristic(full_name="FinalStatus", value="Repaired"),
            ],
            documents=[
                Document(
                    file_name="ComprehensiveOperationLog.pdf",
                    name="Operation Log",
                    description="Aggregated log for Operation/Comprehensive failure event.",
                )
            ],
        ))

        functional_sequence = operation.add_sequence_run(SequenceRun(
            name="Sequence/FunctionalTest",
            version="FT-3.2",
            user="chief.operator",
            start_time=functional_start,
            characteristics=[
                Characteristic(full_name="Fixture", value="FT-FX-22"),
            ],
            documents=[
                Document(
                    file_name="FunctionalProcedure.pdf",
                    name="Functional Test Procedure",
                    description="Checklist reviewed before running functional test.",
                )
            ],
        ))

        functional_sequence.add_step_run(
            StepRun(
                name="InitialPowerUp",
                status=ExecutionStatusKind.PASS,
                start_time=_default_tz_datetime(start_timestamp, 7, 11),
                end_time=_default_tz_datetime(start_timestamp, 7, 11),
                measure=Measure(
                        value=_default_tz_datetime(start_timestamp, 7, 11),
                        time=_default_tz_datetime(start_timestamp, 7, 11),
                        status=ExecutionStatusKind.PASS,
                    ),
                characteristics=[
                    Characteristic(full_name="VoltageRange", value="nominal"),
                ],
            )
        )

        functional_sequence.add_step_run(
            StepRun(
                name="FunctionalSummary",
                status=ExecutionStatusKind.FAIL,
                start_time=_default_tz_datetime(start_timestamp, 7, 22),
                end_time=_default_tz_datetime(start_timestamp, 7, 22),
                measure=Measure(
                        value="Errors Logged",
                        time=_default_tz_datetime(start_timestamp, 7, 22),
                        status=ExecutionStatusKind.FAIL,
                    ),
                characteristics=[
                    Characteristic(full_name="SummaryCode", value="ERR-871"),
                ],
            )
        )

        functional_sequence.complete(
            status=ExecutionStatusKind.FAIL,
            end_time=functional_end,
        )

        safety_sequence = operation.add_sequence_run(SequenceRun(
            name="Sequence/FunctionalTest/SubSequence/SafetyChecks",
            version="SC-1.0",
            user="chief.operator",
            start_time=safety_start,
            characteristics=[
                Characteristic(full_name="Inspector", value="QA-123"),
            ],
            documents=[
                Document(
                    file_name="SafetyChecklist.pdf",
                    name="Safety Checklist",
                    description="QA inspector notes for safety evaluation.",
                )
            ],
        ))

        safety_sequence.add_step_run(
            StepRun(
                name="GroundContinuity",
                status=ExecutionStatusKind.FAIL,
                start_time=_default_tz_datetime(start_timestamp, 7, 16),
                end_time=_default_tz_datetime(start_timestamp, 7, 16),
                measure=Measure(
                        value=False,
                        time=_default_tz_datetime(start_timestamp, 7, 16),
                        status=ExecutionStatusKind.FAIL,
                    ),
                characteristics=[
                    Characteristic(full_name="Threshold", value="0.5 Ohm"),
                ],
            )
        )

        safety_sequence.add_step_run(
            StepRun(
                name="OverCurrentDetection",
                status=ExecutionStatusKind.FAIL,
                start_time=_default_tz_datetime(start_timestamp, 7, 18),
                end_time=_default_tz_datetime(start_timestamp, 7, 18),
                measure=Measure(
                        value=12.5,
                        time=_default_tz_datetime(start_timestamp, 7, 18),
                        unit="Amp",
                        symbol="A",
                        status=ExecutionStatusKind.FAIL,
                        limit=Limit(
                            LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
                            lower_bound=0.0,
                            higher_bound=10.0,
                        ),
                    ),
                documents=[
                    Document(
                        file_name="OverCurrentTrace.png",
                        name="Oscilloscope Capture",
                        description="Trace captured during over-current failure.",
                    )
                ],
            )
        )

        safety_sequence.add_step_run(
            StepRun(
                name="AlarmReset",
                status=ExecutionStatusKind.FAIL,
                start_time=_default_tz_datetime(start_timestamp, 7, 20),
                end_time=_default_tz_datetime(start_timestamp, 7, 20),
                measure=Measure(
                        value="Timeout",
                        time=_default_tz_datetime(start_timestamp, 7, 20),
                        status=ExecutionStatusKind.FAIL,
                    ),
            )
        )

        safety_sequence.complete(
            status=ExecutionStatusKind.FAIL,
            end_time=safety_end,
        )

        diagnostics_sequence = operation.add_sequence_run(SequenceRun(
            name="Sequence/Diagnostics",
            version="DG-7.4",
            user="chief.operator",
            start_time=diagnostics_start,
            characteristics=[
                Characteristic(full_name="Routing", value="Manual"),
            ],
            documents=[
                Document(
                    file_name="DiagnosticsMatrix.xlsx",
                    name="Diagnostics Matrix",
                    description="Manual routing instructions for diagnostics sequence.",
                )
            ],
        ))

        diagnostics_sequence.add_step_run(
            StepRun(
                name="DiagnosticScanRange",
                status=ExecutionStatusKind.PASS,
                start_time=_default_tz_datetime(start_timestamp, 7, 34),
                end_time=_default_tz_datetime(start_timestamp, 7, 34),
                measure=Measure(
                        value="W01-W05",
                        time=_default_tz_datetime(start_timestamp, 7, 34),
                        status=ExecutionStatusKind.PASS,
                    ),
                characteristics=[
                    Characteristic(full_name="ScanType", value="Full"),
                ],
            )
        )

        diagnostics_sequence.add_step_run(
            StepRun(
                name="DiagnosticScanValue",
                status=ExecutionStatusKind.PASS,
                start_time=_default_tz_datetime(start_timestamp, 7, 34),
                end_time=_default_tz_datetime(start_timestamp, 7, 34),
                measure=Measure(
                        value=3,
                        time=_default_tz_datetime(start_timestamp, 7, 34),
                        status=ExecutionStatusKind.PASS,
                        limit=Limit(
                            LimitExpression.LOWERBOUND_LEQ_X_LE_HIGHER_BOUND,
                            lower_bound=0,
                            higher_bound=5,
                        ),
                    ),
            )
        )

        diagnostics_sequence.add_step_run(
            StepRun(
                name="RepairNotes",
                status=ExecutionStatusKind.PASS,
                start_time=_default_tz_datetime(start_timestamp, 7, 37),
                end_time=_default_tz_datetime(start_timestamp, 7, 37),
                measure=Measure(
                        value="Replaced fuse F7",
                        time=_default_tz_datetime(start_timestamp, 7, 37),
                        status=ExecutionStatusKind.PASS,
                    ),
            )
        )

        diagnostics_sequence.add_step_run(
            StepRun(
                name="FinalVerification",
                status=ExecutionStatusKind.PASS,
                start_time=_default_tz_datetime(start_timestamp, 7, 44),
                end_time=_default_tz_datetime(start_timestamp, 7, 44),
                measure=Measure(
                        value=True,
                        time=_default_tz_datetime(start_timestamp, 7, 44),
                        status=ExecutionStatusKind.PASS,
                    ),
            )
        )

        diagnostics_sequence.complete(
            status=ExecutionStatusKind.PASS,
            end_time=diagnostics_end,
        )

        operation.complete(
            status=ExecutionStatusKind.FAIL,
            end_time=process_end,
        )

        process.complete(
            status=ExecutionStatusKind.FAIL,
            end_time=process_end,
        )

        warehouse.save_xml(output_path)
    finally:
        model.UTIL = util_original

    return output_path
