import unittest
from unittest.mock import patch

from app.domain.models import ProjectState
from app.resource.ai_reasoner import analyze_allocation


class FakeClient:
    last_provider = "FakeAI"

    def generate_json(self, prompt, response_schema):
        self.prompt = prompt
        return '{"understood_request":"backend 3 ngày từ mai","assessment":"Chưa có candidate lý tưởng.","candidates":[],"recommendation":"Cần xác minh skill trước.","alternatives":[],"missing_information":["skill"],"confidence":"MEDIUM"}'


class ResourceAllocationTest(unittest.TestCase):
    @patch("app.resource.ai_reasoner._build_ai_client")
    @patch("app.resource.ai_reasoner.load_profiles", return_value=[])
    def test_ai_first_allocation_uses_raw_request(self, _profiles, build_client):
        fake = FakeClient()
        build_client.return_value = fake
        state = ProjectState(project_key="DEV", issues=[])
        result, provider = analyze_allocation(state, "Có task backend 3 ngày từ mai. Ai làm được?")
        self.assertEqual(provider, "FakeAI")
        self.assertIn("backend 3 ngày", fake.prompt)
        self.assertIn("Do not use, invent, or request a deterministic score", fake.prompt)
        self.assertEqual(result["confidence"], "MEDIUM")


if __name__ == "__main__":
    unittest.main()
