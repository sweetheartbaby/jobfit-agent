from typing import List, Optional

from .jd_parser import DIMENSIONS, DimensionConfig
from ..schemas import RequirementMatch


class FitScoringAgent:
    def __init__(self, dimensions: Optional[List[DimensionConfig]] = None):
        self.dimensions = dimensions or DIMENSIONS

    def score(self, matches: List[RequirementMatch]) -> float:
        weights = {dimension.name: dimension.weight for dimension in self.dimensions}
        total_weight = sum(weights.values()) or 1.0
        raw = sum(match.score * weights[match.dimension] for match in matches)
        return round(raw / total_weight * 100, 1)

    def recommendation(self, score: float) -> str:
        if score >= 80:
            return "Strong Match"
        if score >= 65:
            return "Good Match"
        if score >= 50:
            return "Possible, needs tailoring"
        return "Not recommended"
