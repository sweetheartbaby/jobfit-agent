from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class Job:
    job_id: str
    title: str
    company: str
    source_file: str
    text: str


@dataclass
class RequirementMatch:
    dimension: str
    label: str
    weight: float
    required_keywords: List[str]
    matched_keywords: List[str]
    missing_keywords: List[str]
    score: float
    evidence: List[str]


@dataclass
class JobMatchReport:
    job: Job
    fit_score: float
    recommendation: str
    matches: List[RequirementMatch]
    gaps: List[str]
    resume_suggestions: List[str]
    interview_questions: List[str]
    need_manual_review: bool

    def to_dict(self) -> Dict:
        return asdict(self)
