import argparse

from .workflow import JobFitWorkflow
from .sample import run_sample


def main():
    parser = argparse.ArgumentParser(prog="jobfit", description="Rank job descriptions by resume fit.")
    sub = parser.add_subparsers(dest="command", required=True)
    sample = sub.add_parser("sample", help="Run the built-in sample and generate reports")
    sample.add_argument("--output", default="reports", help="Output directory")

    rank = sub.add_parser("rank", help="Rank jobs against a resume")
    rank.add_argument("--resume", required=True, help="Path to resume markdown/txt file")
    rank.add_argument("--jobs", required=True, help="Directory containing job description files")
    rank.add_argument("--output", default="reports", help="Output directory")
    rank.add_argument("--llm", default=None, help="Optional OpenAI-compatible model name, e.g. gpt-4o-mini")
    rank.add_argument("--llm-base-url", default=None, help="Optional OpenAI-compatible base URL")
    rank.add_argument("--config", default=None, help="Optional JSON or simple YAML config path")
    args = parser.parse_args()

    if args.command == "sample":
        reports = run_sample(args.output)
    elif args.command == "rank":
        reports = JobFitWorkflow().run(args.resume, args.jobs, args.output, llm_model=args.llm, llm_base_url=args.llm_base_url, config_path=args.config)
        for i, report in enumerate(reports, 1):
            print(f"{i}. {report.job.title} ({report.job.company}) - {report.fit_score} - {report.recommendation}")


if __name__ == "__main__":
    main()
