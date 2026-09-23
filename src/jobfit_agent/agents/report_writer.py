import json
from pathlib import Path
from typing import List

from ..schemas import JobMatchReport
from .resume_tailoring import ResumeTailoringAgent
from .html_report import HTMLReportAgent


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
        (out / "resume_tailoring.md").write_text(ResumeTailoringAgent().generate(sorted_reports), encoding="utf-8")
        (out / "match_report.html").write_text(HTMLReportAgent().generate(sorted_reports), encoding="utf-8")

    def _markdown(self, reports: List[JobMatchReport]) -> str:
        lines = ["# JobFit Match Report", "", self._top_summary(reports), "", "## Overall Ranking", ""]
        lines += ["| Rank | Role | Company | Fit Score | Recommendation | Manual Review |", "| --- | --- | --- | ---: | --- | --- |"]
        for i, report in enumerate(reports, 1):
            review = "Yes" if report.need_manual_review else "No"
            lines.append(f"| {i} | {report.job.title} | {report.job.company} | {report.fit_score} | {report.recommendation} | {review} |")

        for report in reports:
            lines += ["", "---", "", f"## {report.job.title} - {report.job.company}", "", f"**Score:** {report.fit_score} / 100", "", f"**Recommendation:** {report.recommendation}", ""]
            lines += ["### Dimension Scores", "", "| Dimension | Weight | Score | Matched | Missing |", "| --- | ---: | ---: | --- | --- |"]
            for match in report.matches:
                lines.append(
                    f"| {match.label} | {int(match.weight * 100)}% | {match.score} | "
                    f"{', '.join(match.matched_keywords) or '-'} | {', '.join(match.missing_keywords) or '-'} |"
                )
            lines += ["", "### Why it matches"]
            evidence_lines = self._evidence_lines(report)
            lines += evidence_lines or ["- No strong resume evidence found. Treat this result as low confidence."]
            lines += ["", "### Gaps"]
            lines += [f"- {gap}" for gap in report.gaps] or ["- No obvious gap found."]
            lines += ["", "### Resume Suggestions"]
            lines += [f"- {s}" for s in report.resume_suggestions] or ["- No suggestion generated."]
        return "\n".join(lines) + "\n"

    def _top_summary(self, reports: List[JobMatchReport]) -> str:
        if not reports:
            return "No valid jobs found."
        best = reports[0]
        return (
            f"Best match: **{best.job.title} - {best.job.company}** "
            f"with a fit score of **{best.fit_score}**."
        )

    def _evidence_lines(self, report: JobMatchReport) -> List[str]:
        lines = []
        for match in report.matches:
            if match.matched_keywords:
                lines.append(f"- **{match.label}** matches {', '.join(match.matched_keywords)}.")
            for evidence in match.evidence:
                lines.append(f"  - Resume evidence: {evidence}")
        return lines[:12]

    def _questions(self, reports: List[JobMatchReport]) -> str:
        lines = ["# Interview Questions", ""]
        for report in reports:
            lines += [f"## {report.job.title} - {report.job.company}", ""]
            for q in report.interview_questions:
                lines.append(f"- {q}")
            lines.append("")
        return "\n".join(lines)
