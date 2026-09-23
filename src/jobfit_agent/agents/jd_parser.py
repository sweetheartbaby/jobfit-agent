from dataclasses import dataclass
from typing import Dict, List

from ..tools.text_utils import find_keywords


@dataclass
class DimensionConfig:
    name: str
    label: str
    weight: float
    keywords: List[str]


DIMENSIONS = [
    DimensionConfig("required_skills", "必备技术技能", 0.30, ["Python", "TypeScript", "Golang", "Java", "FastAPI", "Docker", "MySQL", "Redis", "WebSocket"]),
    DimensionConfig("project_experience", "项目经历匹配", 0.25, ["项目", "平台", "系统", "落地", "业务", "数据分析", "代码助手", "智能客服", "自动化"]),
    DimensionConfig("agent_rag", "Agent / RAG 经验", 0.20, ["Agent", "RAG", "LangChain", "LangGraph", "Workflow", "ReAct", "Plan", "Execute", "Milvus", "向量", "检索", "Reranker", "MCP"]),
    DimensionConfig("engineering", "工程能力", 0.10, ["API", "接口", "服务", "权限", "JWT", "RBAC", "缓存", "部署", "测试", "监控", "重试", "降级"]),
    DimensionConfig("business", "业务理解", 0.10, ["业务理解", "需求", "方案", "流程", "用户", "评估", "成本", "效率"]),
    DimensionConfig("background", "学历/背景", 0.05, ["本科", "硕士", "计算机", "软件工程", "学历"]),
]


class JDParserAgent:
    def parse(self, jd_text: str) -> Dict[str, List[str]]:
        return {dimension.name: find_keywords(jd_text, dimension.keywords) for dimension in DIMENSIONS}
