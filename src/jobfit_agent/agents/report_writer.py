import json
from pathlib import Path
from typing import List

from ..schemas import JobMatchReport


class ReportAgent:
    def write(self, reports: List[JobMatchReport], output_dir: str) -> None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        sorted_reports = sorted(reports, key=lambda r: r.fit_score, reverse=True)

        (out / "match_report.json").write_text(
            json.dumps([r.to_dict() for r in sorted_reports], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (out / "match_report.md").write_text(self._markdown(sorted_reports), encoding="utf-8")
        (out / "interview_questions.md").write_text(self._questions(sorted_reports), encoding="utf-8")

    def _markdown(self, reports: List[JobMatchReport]) -> str:
        lines = ["# JobFit Match Report", ""]
        lines += ["## Overall Ranking", "", "| Rank | Role | Company | Fit Score | Recommendation |", "| --- | --- | --- | ---: | --- |"]
        for i, report in enumerate(reports, 1):
            lines.append(f"| {i} | {report.job.title} | {report.job.company} | {report.fit_score} | {report.recommendation} |")
        for report in reports:
            lines += ["", f"## {report.job.title} - {report.company if False else report.job.company}", "", f"Score: **{report.fit_score}**", "", "### Evidence Matches"]
            for match in report.matches:
                lines.append(f"- **{match.dimension}**: {match.score}; matched: {', '.join(match.matched_keywords) or 'none'}")
                for evidence in match.evidence:
                    lines.append(f"  - Evidence: {evidence}")
            lines += ["", "### Gaps"]
            lines += [f"- {gap}" for gap in report.gaps] or ["- No obvious gap found."]
            lines += ["", "### Resume Suggestions"]
            lines += [f"- {s}" for s in report.resume_suggestions]
        return "\n".join(lines) + "\n"

    def _questions(self, reports: List[JobMatchReport]) -> str:
        lines = ["# Interview Questions", ""]
        for report in reports:
            lines += [f"## {report.job.title} - {report.job.company}", ""]
            for q in report.interview_questions:
                lines.append(f"- {q}")
            lines.append("")
        return "\n".join(lines)
