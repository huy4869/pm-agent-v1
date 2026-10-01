from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

JIRA_BASE_URL = (os.getenv("JIRA_BASE_URL") or os.getenv("JIRA_URL") or "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL") or os.getenv("JIRA_USER_EMAIL") or ""
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN") or os.getenv("JIRA_TOKEN") or ""


def _auth() -> HTTPBasicAuth:
    return HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)


def _headers() -> dict[str, str]:
    return {"Accept": "application/json", "Content-Type": "application/json"}


def _validate() -> None:
    missing = []
    if not JIRA_BASE_URL: missing.append("JIRA_BASE_URL")
    if not JIRA_EMAIL: missing.append("JIRA_EMAIL")
    if not JIRA_API_TOKEN: missing.append("JIRA_API_TOKEN")
    if missing:
        raise RuntimeError("Missing Jira config in .env: " + ", ".join(missing))


def _get_issue(key: str) -> dict:
    r = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/issue/{key}",
        auth=_auth(), headers=_headers(),
        params={"fields": "summary,status,assignee,duedate"}, timeout=30,
    )
    r.raise_for_status()
    return r.json()


def _get_transitions(key: str) -> list[dict]:
    r = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/issue/{key}/transitions",
        auth=_auth(), headers=_headers(), timeout=30,
    )
    r.raise_for_status()
    return r.json().get("transitions", [])


def main() -> None:
    _validate()
    if len(sys.argv) < 3:
        print('Usage: python scripts/test_jira_transition.py DEV-26 "Done"')
        raise SystemExit(1)
    key = sys.argv[1].strip().upper()
    target = sys.argv[2].strip()
    issue = _get_issue(key)
    current = issue["fields"]["status"]["name"]
    print(f"{key}: {current} -> {target}")
    if current.lower() == target.lower():
        print("No change required.")
        return
    transitions = _get_transitions(key)
    match = next((t for t in transitions if t["to"]["name"].lower() == target.lower()), None)
    if not match:
        print("Available targets:")
        for t in transitions:
            print(f"- {t['to']['name']} (transition {t['id']})")
        raise RuntimeError(f"No transition from {current!r} to {target!r}")
    r = requests.post(
        f"{JIRA_BASE_URL}/rest/api/3/issue/{key}/transitions",
        auth=_auth(), headers=_headers(),
        json={"transition": {"id": match["id"]}}, timeout=30,
    )
    r.raise_for_status()
    updated = _get_issue(key)["fields"]["status"]["name"]
    print(f"Done: {key}: {current} -> {updated}")


if __name__ == "__main__":
    main()
