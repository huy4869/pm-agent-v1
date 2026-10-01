import os
from typing import Any, Protocol

from app.domain.models import ProjectIssue, StatusChange


class ProjectCollector(Protocol):
    project_key: str
    source: str

    def collect_project_issues(self) -> list[dict]: ...
    def collect_issue_changelog(self, issue_key: str) -> Any: ...
    def normalize_issue(self, issue: dict) -> ProjectIssue: ...
    def normalize_status_history(self, changelog: Any) -> list[StatusChange]: ...
    def get_status_since(self, issue: ProjectIssue, history: list[StatusChange]) -> str | None: ...


def build_collector() -> tuple[ProjectCollector, str]:
    source = os.getenv("PM_SOURCE", "jira").strip().lower()
    if source == "jira":
        from app.jira.client import JiraClient
        from app.jira.collector import JiraCollector
        client = JiraClient()
        return JiraCollector(client), client.base_url
    if source == "redmine":
        from app.redmine.client import RedmineClient
        from app.redmine.collector import RedmineCollector
        client = RedmineClient()
        return RedmineCollector(client), client.base_url
    raise ValueError("PM_SOURCE must be either 'jira' or 'redmine'")
