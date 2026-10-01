import os

from dotenv import load_dotenv


load_dotenv()


def jira_issue_url(
    issue_key: str,
) -> str:
    base_url = os.getenv(
        "JIRA_BASE_URL"
    )

    if not base_url:
        raise ValueError(
            "Missing JIRA_BASE_URL"
        )

    return (
        f"{base_url.rstrip('/')}"
        f"/browse/{issue_key}"
    )