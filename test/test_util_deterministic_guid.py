import unittest

from proligent.model import Util

class UtilDeterministicGuidTests(unittest.TestCase):
    def test_get_deterministic_guid_is_stable_for_same_input(self) -> None:
        first = Util.get_deterministic_guid("ABC-123")
        second = Util.get_deterministic_guid("ABC-123")

        self.assertEqual(first, second)

    def test_get_deterministic_guid_matches_known_value(self) -> None:
        guid = Util.get_deterministic_guid("ABC-123")

        self.assertEqual(guid, "4d156d7b-c9c3-4c00-8aa1-e5b06e46e1f4")

    def test_get_deterministic_guid_uses_utf8_sha256_algorithm(self) -> None:
        guid = Util.get_deterministic_guid("é")

        self.assertEqual(guid, "4a99557e-4033-4353-9de2-eb65472017ca")

    def test_get_deterministic_guid_rejects_none_input(self) -> None:
        with self.assertRaises(ValueError):
            Util.get_deterministic_guid(None)


if __name__ == "__main__":
    unittest.main()
