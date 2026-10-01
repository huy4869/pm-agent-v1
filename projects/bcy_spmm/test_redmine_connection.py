"""Smoke-test the Redmine configuration in .env against the real API."""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def main() -> int:
    base_url = (os.getenv("REDMINE_BASE_URL") or "").strip().rstrip("/")
    api_key = (os.getenv("REDMINE_API_KEY") or "").strip()
    project_id = (os.getenv("REDMINE_PROJECT_ID") or "").strip()

    missing = [
        name
        for name, value in (
            ("REDMINE_BASE_URL", base_url),
            ("REDMINE_API_KEY", api_key),
            ("REDMINE_PROJECT_ID", project_id),
        )
        if not value
    ]
    if missing:
        print(f"ERROR: Missing configuration: {', '.join(missing)}", file=sys.stderr)
        return 2

    headers = {
        "Accept": "application/json",
        "X-Redmine-API-Key": api_key,
    }

    try:
        current_user = requests.get(
            f"{base_url}/users/current.json",
            headers=headers,
            timeout=30,
        )
        current_user.raise_for_status()
        user = current_user.json().get("user", {})

        project_response = requests.get(
            f"{base_url}/projects/{project_id}.json",
            headers=headers,
            timeout=30,
        )
        project_response.raise_for_status()
        project = project_response.json().get("project", {})
    except requests.RequestException as exc:
        print(f"ERROR: Redmine connection failed: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ERROR: Redmine returned invalid JSON: {exc}", file=sys.stderr)
        return 1

    user_label = user.get("login") or user.get("id") or "unknown"
    project_label = project.get("name") or project.get("identifier") or project_id
    print(f"OK: Connected to Redmine as {user_label}")
    print(f"OK: Project is accessible: {project_label} (id={project.get('id', project_id)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
