from typing import Dict, List, Optional

from .jd_parser import DIMENSIONS, DimensionConfig
from ..tools.text_utils import find_keywords


class ResumeParserAgent:
    def __init__(self, dimensions: Optional[List[DimensionConfig]] = None):
        self.dimensions = dimensions or DIMENSIONS

    def parse(self, resume_text: str) -> Dict[str, List[str]]:
        return {dimension.name: find_keywords(resume_text, dimension.keywords) for dimension in self.dimensions}
