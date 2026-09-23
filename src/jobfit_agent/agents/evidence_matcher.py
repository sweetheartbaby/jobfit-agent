from typing import Dict, List, Optional

from .jd_parser import DIMENSIONS, DimensionConfig
from ..schemas import RequirementMatch
from ..tools.text_utils import find_evidence


class EvidenceMatcherAgent:
    def __init__(self, dimensions: Optional[List[DimensionConfig]] = None):
        self.dimensions = dimensions or DIMENSIONS

    def match(self, jd_requirements: Dict[str, List[str]], resume_profile: Dict[str, List[str]], resume_text: str) -> List[RequirementMatch]:
        results = []
        for dimension in self.dimensions:
            required = jd_requirements.get(dimension.name, [])
            candidate = resume_profile.get(dimension.name, [])
            matched = sorted(set(required) & set(candidate))
            missing = sorted(set(required) - set(candidate))
            if not required:
                score = 0.6 if candidate else 0.4
            else:
                score = len(matched) / len(required)
            results.append(RequirementMatch(
                dimension=dimension.name,
                label=dimension.label,
                weight=dimension.weight,
                required_keywords=required,
                matched_keywords=matched,
                missing_keywords=missing,
                score=round(score, 2),
                evidence=find_evidence(resume_text, matched),
            ))
        return results
