import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


class RedmineClient:
    def __init__(self) -> None:
        self.base_url = (os.getenv("REDMINE_BASE_URL") or "").rstrip("/")
        self.api_key = os.getenv("REDMINE_API_KEY")
        if not self.base_url:
            raise ValueError("Missing REDMINE_BASE_URL")
        if not self.api_key:
            raise ValueError("Missing REDMINE_API_KEY")
        self.headers = {
            "Accept": "application/json",
            "X-Redmine-API-Key": self.api_key,
        }
        # Reuse TCP/TLS connections across paginated Redmine requests.
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.timeout = float(os.getenv("REDMINE_TIMEOUT_SECONDS", "15"))

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


    def list_projects(self) -> list[dict]:
        projects: list[dict] = []
        offset = 0
        while True:
            data = self._get(
                "/projects.json",
                {"limit": 100, "offset": offset},
            )
            page = data.get("projects", [])
            projects.extend(page)
            offset += len(page)
            if not page or offset >= data.get("total_count", offset):
                break
        return projects

    def list_project_issues(self, project_id: str, limit: int = 100) -> list[dict]:
        issues: list[dict] = []
        offset = 0
        while True:
            data = self._get(
                "/issues.json",
                {
                    "project_id": project_id,
                    "status_id": "*",
                    "include": "relations",
                    "sort": "updated_on:desc",
                    "limit": min(limit, 100),
                    "offset": offset,
                },
            )
            page = data.get("issues", [])
            issues.extend(page)
            offset += len(page)
            if not page or offset >= data.get("total_count", offset):
                break
        return issues

    def get_issue(self, issue_id: int | str, include: str = "journals") -> dict:
        return self._get(
            f"/issues/{issue_id}.json",
            {"include": include},
        ).get("issue", {})

    def get_issue_statuses(self) -> dict[str, str]:
        data = self._get("/issue_statuses.json")
        return {
            str(status["id"]): (
                "Closed" if status.get("is_closed") else status["name"]
            )
            for status in data.get("issue_statuses", [])
        }

    def get_project(self, project_id: str) -> dict:
        return self._get(f"/projects/{project_id}.json", {"include": "trackers,issue_categories"}).get("project", {})

    def list_project_versions(self, project_id: str) -> list[dict]:
        return self._get(f"/projects/{project_id}/versions.json").get("versions", [])
