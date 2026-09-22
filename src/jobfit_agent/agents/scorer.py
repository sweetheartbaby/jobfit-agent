from typing import List

from .jd_parser import DIMENSIONS
from ..schemas import RequirementMatch


class FitScoringAgent:
    def score(self, matches: List[RequirementMatch]) -> float:
        weights = {dimension.name: dimension.weight for dimension in DIMENSIONS}
        return round(sum(match.score * weights[match.dimension] for match in matches) * 100, 1)

    def recommendation(self, score: float) -> str:
        if score >= 80:
            return "Strong Match"
        if score >= 65:
            return "Good Match"
        if score >= 50:
            return "Possible, needs tailoring"
        return "Not recommended"
