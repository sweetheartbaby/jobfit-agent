import unittest

from jobfit_agent.llm import repair_json, merge_keywords


class LLMUtilityTest(unittest.TestCase):
    def test_repair_json_from_fenced_block(self):
        data = repair_json('```json\n{"required_skills": ["Python"]}\n```')
        self.assertEqual(data["required_skills"], ["Python"])

    def test_merge_keywords_keeps_rule_data(self):
        merged = merge_keywords({"required_skills": ["Python"]}, {"required_skills": ["FastAPI", "Python"]})
        self.assertEqual(merged["required_skills"], ["Python", "FastAPI"])


if __name__ == "__main__":
    unittest.main()
