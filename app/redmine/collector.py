import os

from app.jira.normalizer import get_status_since
from app.redmine.client import RedmineClient
from app.redmine.normalizer import normalize_issue, normalize_status_history


class RedmineCollector:
    source = "redmine"

    def __init__(self, client: RedmineClient, project_key: str | None = None) -> None:
        self.client = client
        self.project_key = project_key or os.getenv("REDMINE_PROJECT_ID")
        if not self.project_key:
            raise ValueError("Missing REDMINE_PROJECT_ID")
        self.status_names = client.get_issue_statuses()

    def collect_project_issues(self) -> list[dict]:
        return self.client.list_project_issues(self.project_key)

    def collect_issue_changelog(self, issue_key: str) -> dict:
        return self.client.get_issue(issue_key.removeprefix("RM-"), include="journals")

    normalize_issue = staticmethod(normalize_issue)
    def normalize_status_history(self, issue: dict):
        return normalize_status_history(issue, self.status_names)
    get_status_since = staticmethod(get_status_since)
