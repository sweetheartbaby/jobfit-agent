from typing import Dict, List

from .jd_parser import DIMENSIONS
from ..schemas import RequirementMatch
from ..tools.text_utils import find_evidence


class EvidenceMatcherAgent:
    def match(self, jd_requirements: Dict[str, List[str]], resume_profile: Dict[str, List[str]], resume_text: str) -> List[RequirementMatch]:
        results = []
        for dimension in DIMENSIONS:
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
                required_keywords=required,
                matched_keywords=matched,
                missing_keywords=missing,
                score=round(score, 2),
                evidence=find_evidence(resume_text, matched),
            ))
        return results
