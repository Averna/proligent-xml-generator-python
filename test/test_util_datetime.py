import datetime
import unittest
from unittest.mock import patch

from proligent.model import Util


class UtilFormatDatetimeTests(unittest.TestCase):
    def test_format_datetime_naive_with_timezone_name(self) -> None:
        util = Util(timezone="America/New_York")
        naive_time = datetime.datetime(2024, 1, 1, 12, 0, 0)

        formatted = util.format_datetime(naive_time)

        self.assertEqual(formatted, "2024-01-01T12:00:00-05:00")

    def test_format_datetime_naive_with_tzinfo(self) -> None:
        offset = datetime.timedelta(hours=3, minutes=30)
        util = Util(timezone=datetime.timezone(offset))
        naive_time = datetime.datetime(2024, 6, 1, 8, 15, 30)

        formatted = util.format_datetime(naive_time)

        self.assertEqual(formatted, "2024-06-01T08:15:30+03:30")

    def test_format_datetime_defaults_to_machine_timezone(self) -> None:
        util = Util()
        naive_time = datetime.datetime(2024, 3, 10, 8, 0, 0)
        machine_timezone = datetime.timezone(datetime.timedelta(hours=-7))

        with patch.object(Util, "_machine_timezone", return_value=machine_timezone):
            formatted = util.format_datetime(naive_time)

        self.assertEqual(formatted, "2024-03-10T08:00:00-07:00")


if __name__ == "__main__":
    unittest.main()
