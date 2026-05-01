import unittest

from proligent.model import ProcessRun, Util


class TestUtilDeterministicIdProcessStartTime(unittest.TestCase):
    def test_util_default_deterministic_id_process_start_time(self) -> None:
        """Verify that Util has the default process start time for deterministic process run id."""
        util = Util()
        self.assertEqual(util.deterministic_id_process_start_time, "2000-01-01")

    def test_util_custom_deterministic_id_process_start_time(self) -> None:
        """Verify that consumers can customize process start time in Util."""
        custom_time = "2024-06-15"
        util = Util(deterministic_id_process_start_time=custom_time)
        self.assertEqual(util.deterministic_id_process_start_time, custom_time)

    def test_build_deterministic_process_run_id_with_custom_util_start_time(self) -> None:
        """Verify that consumers can use custom Util process start time."""
        custom_util = Util(deterministic_id_process_start_time="2024-06-15")

        # Generate ID using the custom util's process start time
        id_value = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            custom_util.deterministic_id_process_start_time,
            "Production"
        )

        # Should be different from using the default
        id_default = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )

        self.assertNotEqual(id_value, id_default)

    def test_util_deterministic_id_process_start_time_can_be_modified(self) -> None:
        """Verify that consumers can modify the process start time after creation."""
        util = Util()
        original_time = util.deterministic_id_process_start_time
        self.assertEqual(original_time, "2000-01-01")

        # Modify it
        util.deterministic_id_process_start_time = "2025-12-31"
        self.assertEqual(util.deterministic_id_process_start_time, "2025-12-31")


if __name__ == "__main__":
    unittest.main()
