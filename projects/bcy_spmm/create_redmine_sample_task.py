"""Create the supplied sample task in the configured Redmine project.

The script is idempotent by subject: if a matching issue already exists in the
project, it prints that issue instead of creating a duplicate.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_URL = (os.getenv("REDMINE_BASE_URL") or "").strip().rstrip("/")
API_KEY = (os.getenv("REDMINE_API_KEY") or "").strip()
PROJECT_ID = (os.getenv("REDMINE_PROJECT_ID") or "").strip()
SUBJECT = "Phiếu đề nghị SPMM"
ASSIGNEE_LOGIN = "Hanglt102"
ASSIGNEE_DISPLAY_NAME = "Luc Thi Hang"

DESCRIPTION = """Xuất phụ lục - tạm thời theo form của FPT/ đi theo biểu mẫu

h3. Thông tin thực hiện

|_. Giai đoạn |_. PIC |_. Start date |_. End date |_. Status |_. Ghi chú |
| BA | Quynhdtn17 |  | 19/08/2026 | Done | "Link Figma":https://gitlab.fis.vn/akames/project-knowledge/bcy/documents/-/tree/master/ngoai-giao/de-nghi-spmm?ref_type=heads<br>"Link tài liệu":https://gitlab.fis.vn/akames/project-knowledge/bcy/documents/-/tree/master/ngoai-giao/de-nghi-spmm?ref_type=heads |
| Dev | Lampt45 | 19/08/2026 | 25/08/2026 | Done | "Màn hình request form":https://10.86.60.81/track-and-trace/request-form |
| Test | Hanglt102 | 26/08/2026 |  |  |  |
"""


def _headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY,
    }


def _get(path: str, **params: Any) -> dict[str, Any]:
    response = requests.get(
        f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=30
    )
    response.raise_for_status()
    return response.json()


def _find_assignee_id(login: str, display_name: str) -> int | None:
    offset = 0
    while True:
        data = _get(
            f"/projects/{PROJECT_ID}/memberships.json", limit=100, offset=offset
        )
        memberships = data.get("memberships", [])
        for membership in memberships:
            user = membership.get("user") or {}
            member_name = str(user.get("name", "")).casefold()
            if member_name in {login.casefold(), display_name.casefold()}:
                return int(user["id"])
        offset += len(memberships)
        if not memberships or offset >= int(data.get("total_count", offset)):
            break

    return None


def _find_high_priority_id() -> int | None:
    priorities = _get("/enumerations/issue_priorities.json").get(
        "issue_priorities", []
    )
    high_names = {"high", "cao", "urgent", "khẩn cấp"}
    match = next(
        (p for p in priorities if str(p.get("name", "")).casefold() in high_names),
        None,
    )
    return int(match["id"]) if match else None


def _find_existing_issue() -> dict[str, Any] | None:
    data = _get(
        "/issues.json",
        project_id=PROJECT_ID,
        status_id="*",
        subject=SUBJECT,
        limit=100,
    )
    return next(
        (
            issue
            for issue in data.get("issues", [])
            if str(issue.get("subject", "")).strip().casefold() == SUBJECT.casefold()
        ),
        None,
    )


def main() -> int:
    missing = [
        name
        for name, value in (
            ("REDMINE_BASE_URL", BASE_URL),
            ("REDMINE_API_KEY", API_KEY),
            ("REDMINE_PROJECT_ID", PROJECT_ID),
        )
        if not value
    ]
    if missing:
        print(f"ERROR: Missing configuration: {', '.join(missing)}", file=sys.stderr)
        return 2

    try:
        existing = _find_existing_issue()
        if existing:
            issue_id = existing["id"]
            print(f"SKIP: Issue already exists: #{issue_id} - {SUBJECT}")
            print(f"URL: {BASE_URL}/issues/{issue_id}")
            return 0

        assignee_id = _find_assignee_id(ASSIGNEE_LOGIN, ASSIGNEE_DISPLAY_NAME)
        if assignee_id is None:
            print(
                f"ERROR: Project member {ASSIGNEE_LOGIN!r} was not found; "
                "issue was not created.",
                file=sys.stderr,
            )
            return 3

        issue: dict[str, Any] = {
            "project_id": PROJECT_ID,
            "subject": SUBJECT,
            "description": DESCRIPTION,
            "assigned_to_id": assignee_id,
            "start_date": "2026-08-26",
        }
        priority_id = _find_high_priority_id()
        if priority_id is not None:
            issue["priority_id"] = priority_id

        response = requests.post(
            f"{BASE_URL}/issues.json",
            headers=_headers(),
            json={"issue": issue},
            timeout=30,
        )
        response.raise_for_status()
        created = response.json()["issue"]
    except requests.RequestException as exc:
        detail = ""
        if exc.response is not None:
            detail = f" Response: {exc.response.text[:500]}"
        print(f"ERROR: Could not create Redmine issue: {exc}.{detail}", file=sys.stderr)
        return 1

    issue_id = created["id"]
    print(f"CREATED: #{issue_id} - {SUBJECT}")
    print(f"Assignee: {ASSIGNEE_LOGIN}")
    print(f"URL: {BASE_URL}/issues/{issue_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
