import argparse

from .workflow import JobFitWorkflow


def main():
    parser = argparse.ArgumentParser(prog="jobfit", description="Rank job descriptions by resume fit.")
    sub = parser.add_subparsers(dest="command", required=True)
    rank = sub.add_parser("rank", help="Rank jobs against a resume")
    rank.add_argument("--resume", required=True, help="Path to resume markdown/txt file")
    rank.add_argument("--jobs", required=True, help="Directory containing job description files")
    rank.add_argument("--output", default="reports", help="Output directory")
    args = parser.parse_args()

    if args.command == "rank":
        reports = JobFitWorkflow().run(args.resume, args.jobs, args.output)
        for i, report in enumerate(reports, 1):
            print(f"{i}. {report.job.title} ({report.job.company}) - {report.fit_score} - {report.recommendation}")


if __name__ == "__main__":
    main()
