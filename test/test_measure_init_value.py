import datetime
import unittest

from proligent.model import Measure, MeasureKind


class MeasureInitValueInferredKindTests(unittest.TestCase):
    def test_infers_kind_from_supported_python_types(self) -> None:
        cases = [
            ("abc", MeasureKind.STRING),
            (True, MeasureKind.BOOL),
            (42, MeasureKind.INTEGER),
            (3.14, MeasureKind.REAL),
            (datetime.datetime(2024, 1, 1, 8, 30, 0), MeasureKind.DATETIME),
        ]

        for value, expected_kind in cases:
            with self.subTest(value=value, expected_kind=expected_kind):
                result = Measure._init_value_inferred_kind(value)
                self.assertEqual(str(value), result.value)
                self.assertEqual(expected_kind, result.type_value)

    def test_raises_on_unsupported_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "Incompatible value type"):
            Measure._init_value_inferred_kind([1, 2, 3])  # type: ignore[arg-type]


class MeasureInitValueForcedKindTests(unittest.TestCase):
    def test_forced_kind_accepts_compatible_values(self) -> None:
        cases = [
            ("hello", MeasureKind.STRING),
            (True, MeasureKind.BOOL),
            (123, MeasureKind.INTEGER),
            (123.456, MeasureKind.REAL),
            (datetime.datetime(2024, 1, 1, 8, 30, 0), MeasureKind.DATETIME),
        ]

        for value, forced_kind in cases:
            with self.subTest(value=value, forced_kind=forced_kind):
                result = Measure._init_value_forced_kind(value, forced_kind)
                self.assertEqual(str(value), result.value)
                self.assertEqual(forced_kind, result.type_value)

    def test_forced_kind_always_accepts_string_values(self) -> None:
        cases = [
            ("hello", MeasureKind.STRING),
            ("123", MeasureKind.INTEGER),
            ("True", MeasureKind.BOOL),
            ("123.456", MeasureKind.REAL),
            ("2024-01-01T08:30:00", MeasureKind.DATETIME),
        ]

        for value, forced_kind in cases:
            with self.subTest(value=value, forced_kind=forced_kind):
                result = Measure._init_value_forced_kind(value, forced_kind)
                self.assertEqual(str(value), result.value)
                self.assertEqual(forced_kind, result.type_value)

    def test_forced_kind_accepts_int_values_into_real(self) -> None:
        cases = [
            ("123", MeasureKind.REAL),
            ("123.456", MeasureKind.REAL),
        ]

        for value, forced_kind in cases:
            with self.subTest(value=value, forced_kind=forced_kind):
                result = Measure._init_value_forced_kind(value, forced_kind)
                self.assertEqual(str(value), result.value)
                self.assertEqual(forced_kind, result.type_value)

    def test_forced_kind_bool_string_is_case_insensitive(self) -> None:
        cases = [
            ("True", MeasureKind.BOOL),
            ("TRUE", MeasureKind.BOOL),
            ("true", MeasureKind.BOOL),
            ("False", MeasureKind.BOOL),
            ("fAlSe", MeasureKind.BOOL),
        ]

        for value, forced_kind in cases:
            with self.subTest(value=value, forced_kind=forced_kind):
                result = Measure._init_value_forced_kind(value, forced_kind)
                self.assertEqual(str(value), result.value)
                self.assertEqual(forced_kind, result.type_value)

    def test_forced_kind_rejects_incompatible_bool_value_int(self) -> None:
        with self.assertRaisesRegex(ValueError, "not compatible"):
            Measure._init_value_forced_kind(1, MeasureKind.BOOL)

    def test_forced_kind_rejects_incompatible_integer_value(self) -> None:
        with self.assertRaisesRegex(ValueError, "not compatible"):
            Measure._init_value_forced_kind("abc", MeasureKind.INTEGER)

    def test_forced_kind_rejects_incompatible_bool_value_string(self) -> None:
        with self.assertRaisesRegex(ValueError, "not compatible"):
            Measure._init_value_forced_kind("notabool", MeasureKind.BOOL)

    def test_forced_kind_rejects_unsupported_measure_kind(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported MeasureKind"):
            Measure._init_value_forced_kind("abc", object())  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
