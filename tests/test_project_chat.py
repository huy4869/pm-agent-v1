import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from app.intelligence.project_chat import answer_project

class ProjectChatTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {"project": {"name": "Demo"}, "syncedAt": "2026-09-30",
            "metrics": SimpleNamespace(total_issues=1), "versions": [],
            "issues": [{"key": "RM-1", "subject": "Urgent task", "done": False,
            "overdue": True, "assignee": "PM", "redmineUrl": "https://example.test/issues/1"}]}
        self.risk = {"headline": "One overdue task"}
    def ask(self, answer):
        client = SimpleNamespace(last_provider="mock", generate_json=lambda *args: json.dumps(answer))
        with patch("app.intelligence.project_chat.build_ai_client", return_value=client):
            return answer_project(self.snapshot, None, None, self.risk, [], "Task nào gấp?", [])
    def test_real_issue_links_are_server_grounded(self):
        result = self.ask({"answer": "Kiểm tra RM-1", "issue_keys": ["RM-1", "RM-999"]})
        self.assertFalse(result["fallback"])
        self.assertEqual([x["key"] for x in result["evidence"]], ["RM-1"])
        self.assertEqual(result["evidence"][0]["url"], "https://example.test/issues/1")
    def test_invented_task_in_answer_falls_back(self):
        self.assertTrue(self.ask({"answer": "Giao RM-999", "issue_keys": []})["fallback"])
    def test_provider_failure_returns_facts(self):
        with patch("app.intelligence.project_chat.build_ai_client", side_effect=RuntimeError("offline")):
            result = answer_project(self.snapshot, None, None, self.risk, [], "Hello", [])
        self.assertTrue(result["fallback"])
        self.assertIn("RM-1", result["answer"])
