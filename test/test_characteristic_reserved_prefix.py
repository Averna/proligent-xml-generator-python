import unittest

from proligent.model import (
    Characteristic,
    OperationRun,
    ProductUnit,
    SequenceRun,
    StepRun,
)


class CharacteristicReservedPrefixTests(unittest.TestCase):
    def test_step_run_rejects_reserved_characteristic(self) -> None:
        with self.assertRaisesRegex(ValueError, "reserved for internal use"):
            StepRun(characteristics=[Characteristic(full_name="Proligent.Custom")])

    def test_sequence_run_add_characteristic_rejects_reserved_prefix(self) -> None:
        sequence = SequenceRun()
        with self.assertRaisesRegex(ValueError, "reserved for internal use"):
            sequence.add_characteristic(Characteristic(full_name="Proligent.Custom"))

    def test_operation_run_rejects_reserved_characteristic(self) -> None:
        with self.assertRaisesRegex(ValueError, "reserved for internal use"):
            OperationRun(station="Station/A", characteristics=[Characteristic(full_name="Proligent.Custom")])

    def test_product_unit_add_characteristic_rejects_reserved_prefix(self) -> None:
        product_unit = ProductUnit()
        with self.assertRaisesRegex(ValueError, "reserved for internal use"):
            product_unit.add_characteristic(Characteristic(full_name="Proligent.Custom"))


if __name__ == "__main__":
    unittest.main()
