from typing import Dict, List

from .jd_parser import DIMENSIONS
from ..tools.text_utils import find_keywords


class ResumeParserAgent:
    def parse(self, resume_text: str) -> Dict[str, List[str]]:
        return {dimension.name: find_keywords(resume_text, dimension.keywords) for dimension in DIMENSIONS}
