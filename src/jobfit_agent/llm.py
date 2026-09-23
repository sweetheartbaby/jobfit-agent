import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class LLMResult:
    ok: bool
    data: Optional[Dict]
    error: Optional[str] = None


def repair_json(text: str) -> Optional[Dict]:
    text = text.strip()
    candidates = [text]
    fenced = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.S | re.I)
    candidates.extend(fenced)
    obj = re.search(r"\{.*\}", text, flags=re.S)
    if obj:
        candidates.append(obj.group(0))
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


class OpenAICompatibleClient:
    def __init__(self, model: str, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: int = 30):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.timeout = timeout

    def chat_json(self, system: str, user: str) -> LLMResult:
        if not self.api_key:
            return LLMResult(False, None, "OPENAI_API_KEY is not set")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"]
            data = repair_json(content)
            if data is None:
                return LLMResult(False, None, "LLM returned invalid JSON")
            return LLMResult(True, data)
        except (urllib.error.URLError, KeyError, TimeoutError, json.JSONDecodeError) as exc:
            return LLMResult(False, None, str(exc))


SYSTEM_PROMPT = """You extract job/resume capabilities as strict JSON. Do not invent facts. Output keys: required_skills, project_experience, agent_rag, engineering, business, background. Each value is a list of short keywords found in the text."""


def merge_keywords(rule_data: Dict[str, List[str]], llm_data: Dict) -> Dict[str, List[str]]:
    merged = {k: list(v) for k, v in rule_data.items()}
    for key in merged:
        values = llm_data.get(key, []) if isinstance(llm_data, dict) else []
        if isinstance(values, list):
            for item in values:
                if isinstance(item, str) and item and item not in merged[key]:
                    merged[key].append(item[:40])
    return merged
