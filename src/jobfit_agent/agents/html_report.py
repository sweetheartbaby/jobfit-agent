from html import escape
from typing import List

from ..schemas import JobMatchReport


class HTMLReportAgent:
    def generate(self, reports: List[JobMatchReport]) -> str:
        reports = sorted(reports, key=lambda r: r.fit_score, reverse=True)
        rows = []
        for i, r in enumerate(reports, 1):
            rows.append(
                f"<tr><td>{i}</td><td>{escape(r.job.title)}</td><td>{escape(r.job.company)}</td>"
                f"<td><b>{r.fit_score}</b></td><td>{escape(r.recommendation)}</td></tr>"
            )
        cards = "\n".join(self._job_card(r) for r in reports)
        best = reports[0] if reports else None
        summary = f"Best match: {escape(best.job.title)} - {escape(best.job.company)} ({best.fit_score})" if best else "No jobs found."
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>JobFit Match Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; margin: 32px; color: #182033; background: #f6f8fb; }}
    .container {{ max-width: 1080px; margin: 0 auto; }}
    .hero, .card {{ background: white; border: 1px solid #e6e8ef; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(22, 34, 51, 0.06); }}
    h1 {{ margin: 0 0 8px; }}
    h2 {{ margin-top: 0; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid #edf0f5; text-align: left; }}
    th {{ color: #526071; font-size: 13px; }}
    .score {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: #e8f3ff; color: #075db3; font-weight: 700; }}
    .tag {{ display: inline-block; margin: 3px; padding: 4px 8px; border-radius: 999px; background: #eef6ee; color: #1d6b35; font-size: 12px; }}
    .missing {{ background: #fff2e8; color: #a34b00; }}
    .evidence {{ border-left: 3px solid #7aa7ff; padding-left: 10px; color: #3b4658; }}
    .muted {{ color: #687386; }}
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <h1>JobFit Match Report</h1>
      <p class="muted">{summary}</p>
    </section>
    <section class="card">
      <h2>Overall Ranking</h2>
      <table><thead><tr><th>Rank</th><th>Role</th><th>Company</th><th>Score</th><th>Recommendation</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
    </section>
    {cards}
  </div>
</body>
</html>
"""

    def _job_card(self, report: JobMatchReport) -> str:
        dims = []
        for m in report.matches:
            matched = "".join(f"<span class='tag'>{escape(k)}</span>" for k in m.matched_keywords) or "<span class='muted'>None</span>"
            missing = "".join(f"<span class='tag missing'>{escape(k)}</span>" for k in m.missing_keywords) or "<span class='muted'>None</span>"
            dims.append(f"<tr><td>{escape(m.label)}</td><td>{m.score}</td><td>{matched}</td><td>{missing}</td></tr>")
        evidence = []
        for m in report.matches:
            for e in m.evidence:
                evidence.append(f"<p class='evidence'><b>{escape(m.label)}:</b> {escape(e)}</p>")
        gaps = "".join(f"<li>{escape(g)}</li>" for g in report.gaps) or "<li>No obvious gap found.</li>"
        suggestions = "".join(f"<li>{escape(s)}</li>" for s in report.resume_suggestions) or "<li>No suggestion generated.</li>"
        return f"""
    <section class="card">
      <h2>{escape(report.job.title)} - {escape(report.job.company)} <span class="score">{report.fit_score}</span></h2>
      <p><b>Recommendation:</b> {escape(report.recommendation)}</p>
      <h3>Dimension Scores</h3>
      <table><thead><tr><th>Dimension</th><th>Score</th><th>Matched</th><th>Missing</th></tr></thead><tbody>{''.join(dims)}</tbody></table>
      <h3>Resume Evidence</h3>
      {''.join(evidence) or '<p class="muted">No direct evidence found.</p>'}
      <h3>Gaps</h3><ul>{gaps}</ul>
      <h3>Resume Suggestions</h3><ul>{suggestions}</ul>
    </section>"""
