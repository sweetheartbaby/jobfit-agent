from pathlib import Path

from .workflow import JobFitWorkflow


def run_sample(output_dir: str = "reports"):
    project_root = Path(__file__).resolve().parents[2]
    resume = project_root / "examples" / "resume.md"
    jobs = project_root / "examples" / "jobs"
    config = project_root / "examples" / "jobfit.yaml"
    return JobFitWorkflow().run(str(resume), str(jobs), output_dir, config_path=str(config))
