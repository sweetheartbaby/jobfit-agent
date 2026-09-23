import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from jobfit_agent.sample import run_sample


class SampleTest(unittest.TestCase):
    def test_run_sample(self):
        with TemporaryDirectory() as temp_dir:
            reports = run_sample(temp_dir)
            self.assertTrue(reports)
            self.assertTrue((Path(temp_dir) / "match_report.html").exists())


if __name__ == "__main__":
    unittest.main()
