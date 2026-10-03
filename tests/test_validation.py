import unittest
from cryptolab.common import number, integer, records, chronology, identity, allocate


class ValidationTests(unittest.TestCase):
    def test_boolean_amount(self):
        with self.assertRaises(ValueError):
            integer(True)
        with self.assertRaises(ValueError):
            number(False)

    def test_finite_decimal(self):
        for v in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaises(ValueError):
                number(v)

    def test_identifier_bounds(self):
        for v in ("", " ", None, "a" * 201):
            with self.assertRaises(ValueError):
                identity(v)

    def test_duplicate_records(self):
        with self.assertRaises(ValueError):
            records([{"id": "a"}, {"id": "a"}], "id")

    def test_event_order(self):
        with self.assertRaises(ValueError):
            chronology([{"timestamp": 2}, {"timestamp": 1}])

    def test_rounding_conservation(self):
        self.assertEqual(
            allocate(5, {"a": 1, "b": 1, "c": 1}), {"a": 2, "b": 2, "c": 1}
        )
        self.assertEqual(sum(allocate(101, {"x": 2, "y": 3}).values()), 101)
