from pathlib import Path
from typing import List

from .agents.evidence_matcher import EvidenceMatcherAgent
from .agents.gap_analyzer import GapAnalyzerAgent
from .agents.interview_prep import InterviewPrepAgent
from .agents.jd_parser import JDParserAgent
from .agents.report_writer import ReportAgent
from .agents.resume_parser import ResumeParserAgent
from .agents.scorer import FitScoringAgent
from .connectors.local_files import JobLoaderAgent
from .connectors.csv_loader import CSVJobLoader
from .schemas import JobMatchReport
from .tools.text_utils import read_text


class JobFitWorkflow:
    def __init__(self):
        self.loader = JobLoaderAgent()
        self.jd_parser = JDParserAgent()
        self.resume_parser = ResumeParserAgent()
        self.matcher = EvidenceMatcherAgent()
        self.scorer = FitScoringAgent()
        self.gap_analyzer = GapAnalyzerAgent()
        self.interview = InterviewPrepAgent()
        self.reporter = ReportAgent()

    def run(self, resume_path: str, jobs_dir: str, output_dir: str) -> List[JobMatchReport]:
        resume_text = read_text(Path(resume_path))
        resume_profile = self.resume_parser.parse(resume_text)
        if str(jobs_dir).lower().endswith(".csv"):
            jobs = CSVJobLoader().load(jobs_dir)
        else:
            jobs = self.loader.load(jobs_dir)
        reports = []
        for job in jobs:
            jd_requirements = self.jd_parser.parse(job.text)
            matches = self.matcher.match(jd_requirements, resume_profile, resume_text)
            score = self.scorer.score(matches)
            reports.append(JobMatchReport(
                job=job,
                fit_score=score,
                recommendation=self.scorer.recommendation(score),
                matches=matches,
                gaps=self.gap_analyzer.analyze(matches),
                resume_suggestions=self.gap_analyzer.suggestions(matches),
                interview_questions=self.interview.generate(matches),
                need_manual_review=score < 65 or any(m.score < 0.5 and m.required_keywords for m in matches),
            ))
        self.reporter.write(reports, output_dir)
        return sorted(reports, key=lambda r: r.fit_score, reverse=True)
