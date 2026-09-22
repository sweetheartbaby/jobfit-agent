from typing import List

from ..schemas import RequirementMatch


QUESTION_MAP = {
    "agent_rag": "请讲一个你设计 Agent/RAG 链路的项目：任务如何拆分、接了哪些工具、失败如何处理、效果如何评估？",
    "required_skills": "请结合项目说明你如何使用这些技术栈解决实际问题，并说明遇到的工程难点。",
    "project_experience": "请选一个最能体现业务价值的项目，说明需求背景、你的职责、结果指标和复盘。",
    "engineering": "如果工具调用超时、接口失败或权限不足，你会如何设计重试、降级和日志监控？",
    "business": "请说明你如何把业务需求拆成 Agent 可以执行的任务流。",
    "background": "请说明你的专业基础如何支撑该岗位要求。",
}


class InterviewPrepAgent:
    def generate(self, matches: List[RequirementMatch]) -> List[str]:
        questions = []
        for match in matches:
            if match.score < 0.75:
                questions.append(QUESTION_MAP.get(match.dimension, f"请补充说明 {match.dimension} 相关经验。"))
                if match.missing_keywords:
                    questions.append(f"JD 提到 {', '.join(match.missing_keywords)}，你是否有真实经验？如果没有，准备如何补齐？")
        return questions[:10]
