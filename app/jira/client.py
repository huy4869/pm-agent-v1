import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


class JiraClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("JIRA_BASE_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")

        if not self.base_url:
            raise ValueError("Missing JIRA_BASE_URL")

        if not self.email:
            raise ValueError("Missing JIRA_EMAIL")

        if not self.api_token:
            raise ValueError("Missing JIRA_API_TOKEN")

        self.auth = (
            self.email,
            self.api_token,
        )

        self.headers = {
            "Accept": "application/json",
        }

    def search_issues(
        self,
        jql: str,
        fields: list[str],
        max_results: int = 100,
    ) -> dict[str, Any]:
        url = (
            f"{self.base_url}"
            "/rest/api/3/search/jql"
        )

        response = requests.get(
            url,
            params={
                "jql": jql,
                "fields": ",".join(fields),
                "maxResults": max_results,
            },
            auth=self.auth,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_issue_changelog(
        self,
        issue_key: str,
        max_results: int = 100,
    ) -> list[dict]:
        url = (
            f"{self.base_url}"
            f"/rest/api/3/issue/"
            f"{issue_key}/changelog"
        )

        changelogs: list[dict] = []
        start_at = 0

        while True:
            response = requests.get(
                url,
                params={
                    "startAt": start_at,
                    "maxResults": max_results,
                },
                auth=self.auth,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            values = data.get(
                "values",
                [],
            )

            changelogs.extend(
                values
            )

            if data.get(
                "isLast",
                True,
            ):
                break

            if not values:
                break

            start_at += len(
                values
            )

        return changelogs