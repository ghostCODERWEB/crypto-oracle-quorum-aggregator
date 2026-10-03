import copy, json, unittest
from pathlib import Path
from cryptolab import analyze

EXAMPLE = json.loads(Path("examples/input.json").read_text())
EXPECTED = json.loads(Path("examples/expected.json").read_text())


def at(document, pointer):
    for key in pointer.strip("/").split("/"):
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


class DomainTests(unittest.TestCase):
    def test_example_regression(self):
        self.assertEqual(analyze(EXAMPLE), EXPECTED)

    def test_input_isolation(self):
        snapshot = copy.deepcopy(EXAMPLE)
        analyze(EXAMPLE)
        self.assertEqual(EXAMPLE, snapshot)

    def test_deterministic_replay(self):
        self.assertEqual(analyze(EXAMPLE), analyze(copy.deepcopy(EXAMPLE)))

    def test_missing_required_fields(self):
        with self.assertRaises(ValueError):
            analyze({})

    def test_nonobject_document(self):
        for value in ([], None, True, "data"):
            with self.assertRaises(ValueError):
                analyze(value)

    def test_nonfinite_document(self):
        bad = copy.deepcopy(EXAMPLE)
        bad["nonfinite"] = float("nan")
        with self.assertRaises(ValueError):
            analyze(bad)

    def test_domain_rejection(self):
        bad = copy.deepcopy(EXAMPLE)
        bad.update(INVALID)
        with self.assertRaises(ValueError):
            analyze(bad)


INVALID = {"quorum": 3}


def check_0(self):
    self.assertEqual(at(analyze(EXAMPLE), "/median"), "101")


DomainTests.test_known_answer_0 = check_0


def check_1(self):
    self.assertEqual(at(analyze(EXAMPLE), "/accepted"), ["a", "b"])


DomainTests.test_known_answer_1 = check_1


def check_2(self):
    self.assertEqual(at(analyze(EXAMPLE), "/rejected/0/reason"), "timestamp")


DomainTests.test_known_answer_2 = check_2


def check_3(self):
    self.assertEqual(at(analyze(EXAMPLE), "/rejected/0/id"), "c")


DomainTests.test_known_answer_3 = check_3


def alternate_scenario(self):
    d = copy.deepcopy(EXAMPLE)
    d.update(
        {
            "feeds": [
                {"id": "a", "timestamp": 9, "price": 100},
                {"id": "b", "timestamp": 9, "price": 102},
                {"id": "c", "timestamp": 9, "price": 1000},
            ]
        }
    )
    observed = at(analyze(d), "/accepted")
    self.assertEqual(observed, ["a", "b"])


DomainTests.test_alternate_scenario = alternate_scenario
