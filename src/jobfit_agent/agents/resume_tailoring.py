from typing import List

from ..schemas import JobMatchReport


class ResumeTailoringAgent:
    """Generate fact-grounded resume tailoring advice.

    The MVP intentionally does not invent new experience. It only rewrites around
    matched evidence and explicitly lists missing items as "do not claim unless
    true".
    """

    def generate(self, reports: List[JobMatchReport]) -> str:
        sorted_reports = sorted(reports, key=lambda r: r.fit_score, reverse=True)
        lines = ["# Resume Tailoring Suggestions", ""]
        lines.append("This report is evidence-grounded: only use claims that are supported by your original resume.")
        lines.append("")
        for report in sorted_reports:
            lines += [f"## {report.job.title} - {report.job.company}", ""]
            lines += ["### Focus Areas"]
            focus = [m for m in report.matches if m.matched_keywords]
            for match in focus[:4]:
                lines.append(f"- Emphasize **{match.label}**: {', '.join(match.matched_keywords)}")
            if not focus:
                lines.append("- No strong focus area found from current resume evidence.")

            lines += ["", "### Evidence-based Rewrite Draft"]
            drafts = self._rewrite_drafts(report)
            lines += [f"- {draft}" for draft in drafts] or ["- Add more concrete project evidence before tailoring this role."]

            lines += ["", "### Do Not Claim Unless True"]
            missing = []
            for match in report.matches:
                missing.extend(match.missing_keywords)
            for item in sorted(set(missing))[:12]:
                lines.append(f"- {item}")
            if not missing:
                lines.append("- No obvious missing keyword found.")

            lines += ["", "### Evidence To Prepare Before Interview"]
            lines += [
                "- Prepare one project story with background, task, action, result, and your exact contribution.",
                "- Prepare metrics for retrieval quality, latency, success rate, or efficiency improvement if they are true.",
                "- Prepare failure-handling examples: low-confidence refusal, retry, fallback, and manual review.",
            ]
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    def _rewrite_drafts(self, report: JobMatchReport) -> List[str]:
        drafts = []
        for match in report.matches:
            if match.evidence:
                keywords = ", ".join(match.matched_keywords) if match.matched_keywords else match.label
                drafts.append(f"围绕 {keywords} 强化表达：{match.evidence[0]}。")
        return drafts[:5]
