import os
import importlib.util
import unittest
from unittest.mock import Mock, patch

from app.redmine.normalizer import normalize_issue, normalize_relations, normalize_status_history
from app.source_urls import issue_url, project_url

REQUESTS_AVAILABLE = importlib.util.find_spec("requests") is not None
if REQUESTS_AVAILABLE:
    from app.redmine.client import RedmineClient

@unittest.skipUnless(REQUESTS_AVAILABLE, "requests dependency is not installed")
class RedmineClientTests(unittest.TestCase):
    @patch.dict(os.environ, {
        "REDMINE_BASE_URL": "https://redmine.example.com/",
        "REDMINE_API_KEY": "secret",
    }, clear=False)
    @patch("app.redmine.client.requests.get")
    def test_paginates_all_project_issues(self, get: Mock) -> None:
        first = Mock()
        first.raise_for_status.return_value = None
        first.json.return_value = {"issues": [{"id": 1}, {"id": 2}], "total_count": 3}
        second = Mock()
        second.raise_for_status.return_value = None
        second.json.return_value = {"issues": [{"id": 3}], "total_count": 3}
        get.side_effect = [first, second]

        issues = RedmineClient().list_project_issues("7", limit=2)

        self.assertEqual([1, 2, 3], [issue["id"] for issue in issues])
        self.assertEqual("*", get.call_args_list[0].kwargs["params"]["status_id"])
        self.assertEqual(2, get.call_args_list[1].kwargs["params"]["offset"])
        self.assertEqual("secret", get.call_args_list[0].kwargs["headers"]["X-Redmine-API-Key"])


class RedmineNormalizerTests(unittest.TestCase):
    def test_normalizes_issue_and_relations(self) -> None:
        raw = {
            "id": 42, "subject": "Ship feature", "status": {"name": "In Progress"},
            "assigned_to": {"name": "Lan"}, "priority": {"name": "High"},
            "tracker": {"name": "Feature"}, "parent": {"id": 10},
            "created_on": "2026-08-01T00:00:00Z", "updated_on": "2026-08-02T00:00:00Z",
            "due_date": "2026-08-30",
            "relations": [{"issue_id": 42, "issue_to_id": 43, "relation_type": "blocks"}],
        }
        issue = normalize_issue(raw)
        self.assertEqual("RM-42", issue.key)
        self.assertEqual("RM-10", issue.parent_key)
        self.assertEqual("redmine", issue.source)
        self.assertEqual("blocks", issue.dependencies[0].relation)

    def test_inverts_relation_when_current_issue_is_target(self) -> None:
        relations = normalize_relations(43, [
            {"issue_id": 42, "issue_to_id": 43, "relation_type": "blocks"}
        ])
        self.assertEqual("RM-42", relations[0].related_issue_key)
        self.assertEqual("blocked by", relations[0].relation)

    def test_maps_status_ids_in_journals(self) -> None:
        raw = {"journals": [{
            "created_on": "2026-08-03T10:00:00Z",
            "details": [{"property": "attr", "name": "status_id", "old_value": "1", "new_value": "2"}],
        }]}
        history = normalize_status_history(raw, {"1": "New", "2": "In Progress"})
        self.assertEqual("New", history[0].from_status)
        self.assertEqual("In Progress", history[0].to_status)


class RedmineUrlTests(unittest.TestCase):
    @patch.dict(os.environ, {"PM_SOURCE": "redmine"}, clear=False)
    def test_builds_redmine_urls(self) -> None:
        self.assertEqual(
            "https://redmine.example.com/issues/42",
            issue_url("RM-42", "https://redmine.example.com/"),
        )
        self.assertEqual(
            "https://redmine.example.com/projects/7/issues",
            project_url("7", "https://redmine.example.com/"),
        )


if __name__ == "__main__":
    unittest.main()
