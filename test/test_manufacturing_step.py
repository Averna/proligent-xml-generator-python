import datetime
import unittest
from unittest.mock import patch

from proligent.model import ExecutionStatusKind, ManufacturingStep


class ManufacturingStepCompleteTests(unittest.TestCase):
    def test_complete_without_end_time_refreshes_timestamp(self) -> None:
        step = ManufacturingStep()
        first_timestamp = datetime.datetime(2024, 1, 1, 12, 0, 0)
        second_timestamp = datetime.datetime(2024, 1, 1, 12, 0, 5)

        with patch("proligent.model.datetime.datetime") as mock_datetime:
            mock_datetime.now.side_effect = [first_timestamp, second_timestamp]

            step.complete(ExecutionStatusKind.PASS)
            self.assertEqual(step.end_time, first_timestamp)

            step.complete(ExecutionStatusKind.FAIL)
            self.assertEqual(step.end_time, second_timestamp)


if __name__ == "__main__":
    unittest.main()
