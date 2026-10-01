import os

from app.jira.client import JiraClient
from app.jira.normalizer import get_status_since, normalize_issue, normalize_status_history


PROJECT_ISSUE_FIELDS = [
    "summary",
    "status",
    "assignee",
    "priority",
    "issuetype",
    "created",
    "updated",
    "duedate",
    "parent",
    "issuelinks",
]


class JiraCollector:
    source = "jira"
    def __init__(
        self,
        client: JiraClient,
    ) -> None:
        self.client = client

        self.project_key = os.getenv(
            "JIRA_PROJECT_KEY"
        )

        if not self.project_key:
            raise ValueError(
                "Missing JIRA_PROJECT_KEY"
            )

    def collect_project_issues(
        self,
    ) -> list[dict]:
        data = self.client.search_issues(
            jql=(
                f"project = "
                f"{self.project_key} "
                "ORDER BY updated DESC"
            ),
            fields=PROJECT_ISSUE_FIELDS,
            max_results=100,
        )

        return data.get(
            "issues",
            [],
        )

    def collect_issue_changelog(
        self,
        issue_key: str,
    ) -> list[dict]:
        return (
            self.client
            .get_issue_changelog(
                issue_key
            )
        )

    normalize_issue = staticmethod(normalize_issue)
    normalize_status_history = staticmethod(normalize_status_history)
    get_status_since = staticmethod(get_status_since)
