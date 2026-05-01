import unittest

from proligent.model import ProcessRun, Util


class ProcessRunBuildDeterministicProcessRunIdTests(unittest.TestCase):
    def test_comparable_deterministic_process_run_id(self) -> None:
        """
        This unit test exists to be manually compared to other methods that
        need to produce the same output IDs.

        e.g. ResultsProcessor's Utils.GetDeterministicProcessRunId

        Look for this reference:
        CPDD: {4CABFF4A-F1A0-4C73-AD91-4C84BA2E0E92}
        """
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "PROD"
        )
        self.assertEqual("b68f75b8-7bae-3caf-bc41-834c7f76bafa", actual_id)

        # different product_full_name
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/Different123",
            "PROD-12345",
            "2000-01-01",
            "PROD"
        )
        self.assertEqual("7b28bf95-b862-0e49-1bcc-49e96fdb5617", actual_id)

        # different identifier
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "DIFFERENT-99999",
            "2000-01-01",
            "PROD"
        )
        self.assertEqual("da7bda3f-3989-c8f9-0e28-e4b4ec055d18", actual_id)

        # different process_start_time
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2026-12-31",
            "PROD"
        )
        self.assertEqual("9d7aefe2-05b7-19a2-bbe9-d10a480cab3f", actual_id)

        # different process_mode
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "RMA"
        )
        self.assertEqual("7a228f80-9441-f195-c2e3-e1fcff8c5cc7", actual_id)

    def test_build_deterministic_process_run_id_is_stable_for_same_input(self) -> None:
        """Verify that the same inputs produce the same deterministic ID."""
        first = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )
        second = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )

        self.assertEqual(first, second)

    def test_build_deterministic_process_run_id_differs_with_different_product_name(self) -> None:
        """Verify that different product names produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName1/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName2/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_differs_with_different_identifier(self) -> None:
        """Verify that different identifiers produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-11111",
            "2000-01-01",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-22222",
            "2000-01-01",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_differs_with_different_process_start_time(self) -> None:
        """Verify that different process start times produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2024-01-15",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_differs_with_different_process_mode(self) -> None:
        """Verify that different process modes produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "2000-01-01",
            "RMA"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_with_constant_start_time(self) -> None:
        """Verify the method works with the constant process start time value."""
        process_start_time = "2000-01-01"
        id_value = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            process_start_time,
            "Production"
        )

        # Verify it returns a valid UUID string format
        self.assertIsInstance(id_value, str)
        self.assertEqual(len(id_value), 36)  # UUID string is 36 chars (with hyphens)
        # Verify it has the standard UUID format with hyphens
        parts = id_value.split("-")
        self.assertEqual(len(parts), 5)

    def test_process_run_id_is_none_when_not_provided(self) -> None:
        """Verify that ProcessRun.id remains None when not explicitly set."""
        process_run = ProcessRun(
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        self.assertIsNone(process_run.id)

    def test_process_run_id_deterministic_is_valid_uuid(self) -> None:
        """Verify that id_deterministic returns a valid UUID string."""
        process_run = ProcessRun(
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        self.assertIsInstance(process_run.id_deterministic, str)
        self.assertEqual(len(process_run.id_deterministic), 36)  # Valid UUID format
        self.assertEqual(len(process_run.id_deterministic.split("-")), 5)

    def test_process_run_uses_provided_id(self) -> None:
        """Verify that ProcessRun uses the provided ID when specified."""
        custom_id = "12345678-1234-5678-1234-567812345678"
        process_run = ProcessRun(
            id=custom_id,
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        self.assertEqual(process_run.id, custom_id)

    def test_process_run_id_deterministic_stable_for_same_values(self) -> None:
        """Verify that id_deterministic produces the same value for the same field values."""
        run1 = ProcessRun(
            product_full_name="Product/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )
        run2 = ProcessRun(
            product_full_name="Product/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        self.assertEqual(run1.id_deterministic, run2.id_deterministic)

    def test_process_run_id_deterministic_reflects_field_changes(self) -> None:
        """Verify that id_deterministic updates when fields are changed after construction."""
        run = ProcessRun(
            product_full_name="Product/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )
        id_before = run.id_deterministic

        run.product_full_name = "Product/Widget/456"
        id_after = run.id_deterministic

        self.assertNotEqual(id_before, id_after)

    def test_process_run_different_deterministic_id_with_different_product_name(self) -> None:
        """Verify that different product names result in different id_deterministic values."""
        run1 = ProcessRun(
            product_full_name="Product1/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )
        run2 = ProcessRun(
            product_full_name="Product2/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        self.assertNotEqual(run1.id_deterministic, run2.id_deterministic)

    def test_util_default_process_start_time(self) -> None:
        """Verify that Util has the default process start time."""
        util = Util()
        self.assertEqual(util.deterministic_id_process_start_time, "2000-01-01")

    def test_util_custom_process_start_time(self) -> None:
        """Verify that consumers can customize process start time in Util."""
        custom_time = "2024-06-15"
        util = Util(deterministic_id_process_start_time=custom_time)
        self.assertEqual(util.deterministic_id_process_start_time, custom_time)

    def test_process_run_id_deterministic_uses_util_process_start_time(self) -> None:
        """Verify that id_deterministic uses UTIL.deterministic_id_process_start_time."""
        run = ProcessRun(
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        expected_id = ProcessRun.build_deterministic_process_run_id(
            "TestProduct/Widget/123",
            "UNIT-001",
            Util().deterministic_id_process_start_time,
            "Production"
        )

        self.assertEqual(run.id_deterministic, expected_id)

    def test_build_uses_explicit_id_when_provided(self) -> None:
        """Verify that build() uses the explicit id when set."""
        custom_id = "12345678-1234-5678-1234-567812345678"
        run = ProcessRun(
            id=custom_id,
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        built = run.build()
        self.assertEqual(built.process_run_id, custom_id)

    def test_build_uses_id_deterministic_when_id_is_none(self) -> None:
        """Verify that build() falls back to id_deterministic when id is None."""
        run = ProcessRun(
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            process_mode="Production"
        )

        built = run.build()
        self.assertEqual(built.process_run_id, run.id_deterministic)


if __name__ == "__main__":
    unittest.main()
