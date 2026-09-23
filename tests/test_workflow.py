import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from jobfit_agent.workflow import JobFitWorkflow


class WorkflowTest(unittest.TestCase):
    def test_workflow_generates_ranked_reports(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "reports"
            reports = JobFitWorkflow().run("examples/resume.md", "examples/jobs", str(output_dir))
            self.assertTrue(reports)
            self.assertGreaterEqual(reports[0].fit_score, reports[-1].fit_score)
            self.assertTrue((output_dir / "match_report.md").exists())
            self.assertTrue((output_dir / "match_report.json").exists())
            self.assertTrue((output_dir / "interview_questions.md").exists())
            self.assertTrue((output_dir / "resume_tailoring.md").exists())

    def test_csv_loader_supported(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "reports"
            reports = JobFitWorkflow().run("examples/resume.md", "examples/jobs.csv", str(output_dir))
            self.assertEqual(len(reports), 3)


    def test_html_snapshot_loader_supported(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "reports"
            reports = JobFitWorkflow().run("examples/resume.md", "examples/html_jobs", str(output_dir))
            self.assertEqual(len(reports), 1)


if __name__ == "__main__":
    unittest.main()
