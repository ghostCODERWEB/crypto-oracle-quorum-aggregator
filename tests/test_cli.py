import csv, io, json, subprocess, sys, tempfile, unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_json_and_csv_consistent(self):
        expected = json.loads(Path("examples/expected.json").read_text())
        run = subprocess.run(
            [sys.executable, "-m", "cryptolab", "examples/input.json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout), expected)
        csv_run = subprocess.run(
            [
                sys.executable,
                "-m",
                "cryptolab",
                "examples/input.json",
                "--format",
                "csv",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(csv_run.returncode, 0, csv_run.stderr)
        self.assertEqual(
            next(csv.reader(io.StringIO(csv_run.stdout))), ["path", "value"]
        )

    def test_atomic_output_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "out.json"
            path.write_text("old")
            run = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "cryptolab",
                    "examples/input.json",
                    "--output",
                    str(path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(
                json.loads(path.read_text()),
                json.loads(Path("examples/expected.json").read_text()),
            )
            bad = Path(directory) / "bad.json"
            bad.write_text('{"a":1,"a":2}')
            run = subprocess.run(
                [sys.executable, "-m", "cryptolab", str(bad), "--output", str(path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(run.returncode, 2)
            self.assertIn("duplicate JSON key", run.stderr)
            self.assertEqual(
                json.loads(path.read_text()),
                json.loads(Path("examples/expected.json").read_text()),
            )
