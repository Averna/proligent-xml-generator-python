from __future__ import annotations

import unittest
from pathlib import Path

from proligent.xml_validate import validate_xml
from test.scenarios.generate_complex_oprun import generate_complex_oprun
from test.scenarios.generate_partial_operation_run import (
    generate_partial_operation_run,
)
from test.scenarios.generate_readme_example1 import generate_readme_example1
from test.scenarios.generate_readme_example2 import generate_readme_example2
from test.scenarios.generate_simple_oprun_reverse_order import (
    generate_simple_oprun_reverse_order,
)
from test.scenarios.generate_simple_oprun_normal_order import (
    generate_simple_oprun_normal_order,
)
from test.xml_scenario_runner import run_xml_scenario


class OperationRunsGenerationsScenarios(unittest.TestCase):
    def test_readme_example1(self) -> None:
        def validator(path: Path) -> None:
            validate_xml(path)

        run_xml_scenario(
            test_name="readme_example1",
            generator=generate_readme_example1,
            expected_filename="Proligent_readme_example1.xml",
            validator=validator,
        )

    def test_readme_example2(self) -> None:
        def validator(path: Path) -> None:
            validate_xml(path)

        run_xml_scenario(
            test_name="readme_example2",
            generator=generate_readme_example2,
            expected_filename="Proligent_readme_example2.xml",
            validator=validator,
        )

    def test_simple_oprun_reverse_order(self) -> None:
        def validator(path: Path) -> None:
            validate_xml(path)

        run_xml_scenario(
            test_name="simple_oprun_reverse_order",
            generator=generate_simple_oprun_reverse_order,
            expected_filename="Proligent_simple_oprun_reverse_order.xml",
            validator=validator,
        )

    def test_simple_oprun_normal_order(self) -> None:
        def validator(path: Path) -> None:
            validate_xml(path)

        run_xml_scenario(
            test_name="simple_oprun_normal_order",
            generator=generate_simple_oprun_normal_order,
            expected_filename="Proligent_simple_oprun_normal_order.xml",
            validator=validator,
        )

    def test_complex_oprun(self) -> None:
        def validator(path: Path) -> None:
            validate_xml(path)

        run_xml_scenario(
            test_name="complex_oprun",
            generator=generate_complex_oprun,
            expected_filename="Proligent_complex_oprun.xml",
            validator=validator,
        )

    def test_partial_operation_run(self) -> None:
        def validator(path: Path) -> None:
            validate_xml(path)

        run_xml_scenario(
            test_name="partial_operation_run",
            generator=generate_partial_operation_run,
            expected_filename="Proligent_partial_operation_run.xml",
            validator=validator,
        )


if __name__ == "__main__":
    unittest.main()
