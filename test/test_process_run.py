import unittest

from proligent.model import ProcessRun


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
            "ProcessFamily/ProcessName",
            "1.0",
            "PROD"
        )
        self.assertEqual("7af755d8-3ee3-4d09-897e-2e7810170091", actual_id)

        # different product_full_name
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/Different123",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "PROD"
        )
        self.assertEqual("0a433e5a-2975-4672-9ad4-9d6949802492", actual_id)

        # different identifier
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "DIFFERENT-99999",
            "ProcessFamily/ProcessName",
            "1.0",
            "PROD"
        )
        self.assertEqual("68549968-4863-4179-bd03-288af539d32f", actual_id)

        # different process_full_name
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/DifferentProcessName",
            "1.0",
            "PROD"
        )
        self.assertEqual("d327dcd3-5bb8-4c53-9bc4-d4f75cd77af0", actual_id)

        # different process_version
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "2.0",
            "PROD"
        )
        self.assertEqual("9e64615b-72dd-48ef-b475-8cff51f3caa2", actual_id)

        # different process_mode
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "RMA"
        )
        self.assertEqual("153e2144-9cc7-489f-8191-dc0662aecaf2", actual_id)

        # empty process version
        actual_id = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "",
            "PROD"
        )
        self.assertEqual("81423af8-ede4-4b27-ade1-7eb95fb59f75", actual_id)

    def test_build_deterministic_process_run_id_is_stable_for_same_input(self) -> None:
        """Verify that the same inputs produce the same deterministic ID."""
        first = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )
        second = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )

        self.assertEqual(first, second)

    def test_build_deterministic_process_run_id_differs_with_different_product_name(self) -> None:
        """Verify that different product names produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName1/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName2/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_differs_with_different_identifier(self) -> None:
        """Verify that different identifiers produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-11111",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-22222",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_differs_with_different_process_full_name(self) -> None:
        """Verify that different process full names produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessNameA",
            "1.0",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessNameB",
            "1.0",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_differs_with_different_process_version(self) -> None:
        """Verify that different process versions produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "2.0",
            "Production"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_accepts_empty_process_full_name(self) -> None:
        """Verify deterministic ID generation works when process full name is empty."""
        id_value = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "",
            "1.0",
            "Production"
        )

        self.assertIsInstance(id_value, str)
        self.assertEqual(len(id_value), 36)

    def test_build_deterministic_process_run_id_accepts_empty_process_version(self) -> None:
        """Verify deterministic ID generation works when process version is empty."""
        id_value = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "",
            "Production"
        )

        self.assertIsInstance(id_value, str)
        self.assertEqual(len(id_value), 36)

    def test_build_deterministic_process_run_id_with_both_empty_process_fields_is_stable(self) -> None:
        """Verify deterministic ID is stable when process full name and version are both empty."""
        first = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "",
            "",
            "Production"
        )
        second = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "",
            "",
            "Production"
        )
        with_values = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )

        self.assertEqual(first, second)
        self.assertNotEqual(first, with_values)

    def test_build_deterministic_process_run_id_differs_with_different_process_mode(self) -> None:
        """Verify that different process modes produce different IDs."""
        id1 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "Production"
        )
        id2 = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
            "RMA"
        )

        self.assertNotEqual(id1, id2)

    def test_build_deterministic_process_run_id_returns_valid_uuid_format(self) -> None:
        """Verify the method returns a valid UUID string format."""
        id_value = ProcessRun.build_deterministic_process_run_id(
            "ProductFamily/ProductName/PartNumber",
            "PROD-12345",
            "ProcessFamily/ProcessName",
            "1.0",
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

    def test_process_run_id_deterministic_uses_process_name_and_version(self) -> None:
        """Verify that id_deterministic includes process name and version."""
        run = ProcessRun(
            product_full_name="TestProduct/Widget/123",
            product_unit_identifier="UNIT-001",
            name="StationA/ProcessB",
            version="v2.1",
            process_mode="Production"
        )

        expected_id = ProcessRun.build_deterministic_process_run_id(
            "TestProduct/Widget/123",
            "UNIT-001",
            "StationA/ProcessB",
            "v2.1",
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
