import unittest

from proligent.model import OperationRun, SequenceRun


class SequenceRunStationTests(unittest.TestCase):
    def test_cannot_set_station_during_initialization(self) -> None:
        with self.assertRaises(TypeError):
            SequenceRun(station="Station/Forbidden")  # type: ignore[arg-type]

    def test_station_setter_is_forbidden(self) -> None:
        sequence = SequenceRun()
        with self.assertRaises(AttributeError):
            sequence.station = "Station/Forbidden"

    def test_build_requires_station(self) -> None:
        sequence = SequenceRun()
        with self.assertRaises(ValueError):
            sequence.build()


class OperationRunStationTests(unittest.TestCase):
    def test_station_is_required(self) -> None:
        with self.assertRaises(ValueError):
            OperationRun()

    def test_station_propagates_to_sequences(self) -> None:
        operation = OperationRun(station="Station/Example")
        sequence = operation.add_sequence_run(SequenceRun())

        built_operation = operation.build()
        self.assertEqual(built_operation.station_full_name, "Station/Example")
        self.assertEqual(sequence.station, "Station/Example")
        self.assertEqual(built_operation.sequence_run[0].station_full_name, "Station/Example")


if __name__ == "__main__":
    unittest.main()
