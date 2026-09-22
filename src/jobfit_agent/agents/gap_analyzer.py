from typing import List

from ..schemas import RequirementMatch


class GapAnalyzerAgent:
    def analyze(self, matches: List[RequirementMatch]) -> List[str]:
        gaps = []
        for match in matches:
            if match.missing_keywords:
                gaps.append(f"{match.dimension}: missing {', '.join(match.missing_keywords)}")
        return gaps

    def suggestions(self, matches: List[RequirementMatch]) -> List[str]:
        suggestions = []
        for match in matches:
            if match.matched_keywords and match.evidence:
                suggestions.append(f"突出 {match.dimension} 相关经历：{match.evidence[0]}")
            if match.missing_keywords:
                suggestions.append(f"如果真实具备，请在简历中补充 {', '.join(match.missing_keywords)} 的项目证据；如果不具备，不要编造。")
        return suggestions[:8]
