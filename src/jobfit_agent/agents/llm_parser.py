from typing import Dict, List, Optional

from ..llm import OpenAICompatibleClient, SYSTEM_PROMPT, merge_keywords


class LLMParserAgent:
    def __init__(self, model: str, base_url: Optional[str] = None):
        self.client = OpenAICompatibleClient(model=model, base_url=base_url)
        self.last_error = None

    def enhance(self, text: str, rule_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
        user = f"Extract capabilities from this text as JSON only:\n\n{text[:8000]}"
        result = self.client.chat_json(SYSTEM_PROMPT, user)
        if not result.ok or result.data is None:
            self.last_error = result.error
            return rule_data
        return merge_keywords(rule_data, result.data)
