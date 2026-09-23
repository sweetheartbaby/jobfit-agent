import unittest

from jobfit_agent.config import load_config, dimensions_from_config
from jobfit_agent.workflow import JobFitWorkflow


class ConfigTest(unittest.TestCase):
    def test_load_simple_yaml_config(self):
        config = load_config("examples/jobfit.yaml")
        self.assertEqual(config.manual_review_threshold, 65)
        self.assertIn("Tool Calling", config.keywords["agent_rag"])

    def test_workflow_with_config(self):
        reports = JobFitWorkflow().run("examples/resume.md", "examples/jobs", "/tmp/jobfit-config-test", config_path="examples/jobfit.yaml")
        self.assertTrue(reports)

    def test_dimensions_from_config(self):
        config = load_config("examples/jobfit.yaml")
        dimensions = dimensions_from_config(config)
        self.assertTrue(any(d.name == "agent_rag" for d in dimensions))


if __name__ == "__main__":
    unittest.main()
