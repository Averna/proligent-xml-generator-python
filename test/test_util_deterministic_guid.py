import unittest

from proligent.model import Util

class UtilDeterministicGuidTests(unittest.TestCase):
    def test_get_deterministic_guid_is_stable_for_same_input(self) -> None:
        first = Util.get_deterministic_guid("ABC-123")
        second = Util.get_deterministic_guid("ABC-123")

        self.assertEqual(first, second)

    def test_get_deterministic_guid_matches_known_value(self) -> None:
        guid = Util.get_deterministic_guid("ABC-123")

        self.assertEqual(guid, "7215942c-cf5b-e269-8c0a-e2b4e89c1b0f")

    def test_get_deterministic_guid_uses_cp1252_by_default(self) -> None:
        cp1252_guid = Util.get_deterministic_guid("é")
        utf8_guid = Util.get_deterministic_guid("é", encoding="utf-8")

        self.assertEqual(cp1252_guid, "76870634-6994-dd1d-1dfb-0aca54681407")
        self.assertEqual(utf8_guid, "97cddd66-decf-b2ab-f6fb-8a999b4bc76f")
        self.assertNotEqual(cp1252_guid, utf8_guid)


if __name__ == "__main__":
    unittest.main()
