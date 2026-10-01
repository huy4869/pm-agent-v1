"""Create the first BCY Epic/Feature/BA-DEV-TEST hierarchy in Redmine."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_URL = (os.getenv("REDMINE_BASE_URL") or "").strip().rstrip("/")
API_KEY = (os.getenv("REDMINE_API_KEY") or "").strip()
PROJECT_ID = (os.getenv("REDMINE_PROJECT_ID") or "").strip()

EPIC_SUBJECT = "Cục Cơ Yếu Ngoại Giao"
FEATURE_SUBJECT = "Phiếu đề nghị SPMM"
FEATURE_ID = 10296

TRACKER_EPIC = 6
TRACKER_FEATURE = 2
TRACKER_TASK = 4
PRIORITY_NORMAL = 2
PRIORITY_HIGH = 3
PRIORITY_URGENT = 4
STATUS_NEW = 1

USER_HUY = 120
USER_QUYNH = 117
USER_LAM = 118
USER_HANG = 115

TARGET_VERSIONS = (
    ("Trial - Cơ yếu Ngoại giao - 15/09", "2026-09-15"),
    ("Trial - Cơ yếu Đảng Chính quyền - 30/09", "2026-09-30"),
    ("Full Deployment - 30/12", "2026-12-30"),
)


def headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY,
    }


def request(method: str, path: str, **kwargs: Any) -> requests.Response:
    response: requests.Response | None = None
    for attempt in range(3):
        try:
            response = requests.request(
                method, f"{BASE_URL}{path}", headers=headers(), timeout=30, **kwargs
            )
            if response.status_code < 500:
                break
        except requests.RequestException:
            if attempt == 2:
                raise
        time.sleep(attempt + 1)
    assert response is not None
    if not response.ok:
        raise RuntimeError(
            f"{method} {path} failed ({response.status_code}): {response.text[:500]}"
        )
    return response


def get_issue(issue_id: int) -> dict[str, Any]:
    return request("GET", f"/issues/{issue_id}.json", params={"include": "relations"}).json()["issue"]


def find_issue(subject: str, parent_id: int | None = None) -> dict[str, Any] | None:
    data = request(
        "GET",
        "/issues.json",
        params={"project_id": PROJECT_ID, "status_id": "*", "subject": subject, "limit": 100},
    ).json()
    matches = [
        issue
        for issue in data.get("issues", [])
        if str(issue.get("subject", "")).strip().casefold() == subject.casefold()
    ]
    if parent_id is None:
        return next((issue for issue in matches if not issue.get("parent")), None)
    return next(
        (issue for issue in matches if (issue.get("parent") or {}).get("id") == parent_id),
        None,
    )


def create_issue(fields: dict[str, Any]) -> dict[str, Any]:
    response = request("POST", "/issues.json", json={"issue": fields})
    return get_issue(int(response.json()["issue"]["id"]))


def ensure_target_versions() -> dict[str, int]:
    data = request("GET", f"/projects/{PROJECT_ID}/versions.json").json()
    existing = {
        str(version["name"]): version for version in data.get("versions", [])
    }
    result: dict[str, int] = {}
    for name, due_date in TARGET_VERSIONS:
        payload = {
            "name": name,
            "status": "open",
            "due_date": due_date,
            "description": f"BCY milestone due {due_date}.",
            "sharing": "none",
        }
        version = existing.get(name)
        if version:
            version_id = int(version["id"])
            request("PUT", f"/versions/{version_id}.json", json={"version": payload})
        else:
            created = request(
                "POST",
                f"/projects/{PROJECT_ID}/versions.json",
                json={"version": payload},
            ).json()["version"]
            version_id = int(created["id"])
        result[name] = version_id
    return result


def update_issue(issue_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    request("PUT", f"/issues/{issue_id}.json", json={"issue": fields})
    return get_issue(issue_id)


def upsert_child(subject: str, parent_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    existing = find_issue(subject, parent_id)
    payload = {
        "project_id": PROJECT_ID,
        "tracker_id": TRACKER_TASK,
        "parent_issue_id": parent_id,
        "subject": subject,
        **fields,
    }
    if existing:
        return update_issue(int(existing["id"]), payload)
    return create_issue(payload)


def ensure_blocks(source_id: int, target_id: int) -> None:
    relations = get_issue(source_id).get("relations", [])
    exists = any(
        relation.get("relation_type") == "blocks"
        and (
            (relation.get("issue_id") == source_id and relation.get("issue_to_id") == target_id)
            or (relation.get("issue_id") == target_id and relation.get("issue_to_id") == source_id)
        )
        for relation in relations
    )
    if not exists:
        request(
            "POST",
            f"/issues/{source_id}/relations.json",
            json={"relation": {"issue_to_id": target_id, "relation_type": "blocks"}},
        )


def close_via_workflow(issue: dict[str, Any]) -> dict[str, Any]:
    """Redmine's Task workflow requires New -> In Progress -> Resolved -> Closed."""
    issue_id = int(issue["id"])
    current_id = int(issue["status"]["id"])
    sequence = [STATUS_NEW, 2, 3, 5]
    start = sequence.index(current_id) + 1 if current_id in sequence else 1
    for status_id in sequence[start:]:
        issue = update_issue(issue_id, {"status_id": status_id, "done_ratio": 100})
    return issue


def assert_issue(
    issue: dict[str, Any], tracker_id: int, assignee_id: int, parent_id: int | None
) -> None:
    actual_parent = (issue.get("parent") or {}).get("id")
    actual_assignee = (issue.get("assigned_to") or {}).get("id")
    assert issue["tracker"]["id"] == tracker_id, issue
    assert actual_assignee == assignee_id, issue
    assert actual_parent == parent_id, issue


def main() -> int:
    missing = [name for name, value in (
        ("REDMINE_BASE_URL", BASE_URL),
        ("REDMINE_API_KEY", API_KEY),
        ("REDMINE_PROJECT_ID", PROJECT_ID),
    ) if not value]
    if missing:
        raise RuntimeError("Missing configuration: " + ", ".join(missing))

    versions = ensure_target_versions()
    trial_ngoai_giao_id = versions["Trial - Cơ yếu Ngoại giao - 15/09"]

    epic = find_issue(EPIC_SUBJECT)
    epic_fields = {
        "project_id": PROJECT_ID,
        "tracker_id": TRACKER_EPIC,
        "subject": EPIC_SUBJECT,
        "description": "Scope: Cục Cơ Yếu Ngoại Giao.\n\nMốc Trial: 15/09/2026.",
        "assigned_to_id": USER_HUY,
        "fixed_version_id": trial_ngoai_giao_id,
        "due_date": "2026-09-15",
        "status_id": STATUS_NEW,
    }
    epic = update_issue(int(epic["id"]), epic_fields) if epic else create_issue(epic_fields)
    epic_id = int(epic["id"])
    assert_issue(epic, TRACKER_EPIC, USER_HUY, None)

    feature = update_issue(FEATURE_ID, {
        "tracker_id": TRACKER_FEATURE,
        "parent_issue_id": epic_id,
        "subject": FEATURE_SUBJECT,
        "description": "Xuất phụ lục - tạm thời theo form của FPT/ đi theo biểu mẫu.",
        "assigned_to_id": USER_HUY,
        "fixed_version_id": trial_ngoai_giao_id,
        "priority_id": PRIORITY_URGENT,
        "start_date": "2026-08-19",
        "due_date": "2026-08-25",
    })
    assert_issue(feature, TRACKER_FEATURE, USER_HUY, epic_id)

    ba = upsert_child("BA - Phiếu đề nghị SPMM", FEATURE_ID, {
        "description": "BA: Phiếu đề nghị SPMM.\n\nDoc: https://gitlab.fis.vn/akames/project-knowledge/bcy/documents/-/tree/master/ngoai-giao/de-nghi-spmm?ref_type=heads",
        "assigned_to_id": USER_QUYNH,
        "fixed_version_id": trial_ngoai_giao_id,
        "priority_id": PRIORITY_URGENT,
        "start_date": "2026-08-19",
        "due_date": "2026-08-19",
        "done_ratio": 100,
    })
    dev = upsert_child("DEV - Phiếu đề nghị SPMM", FEATURE_ID, {
        "description": "DEV: Phiếu đề nghị SPMM.",
        "assigned_to_id": USER_LAM,
        "fixed_version_id": trial_ngoai_giao_id,
        "priority_id": PRIORITY_URGENT,
        "start_date": "2026-08-19",
        "due_date": "2026-08-25",
        "done_ratio": 100,
    })
    test = upsert_child("TEST - Phiếu đề nghị SPMM", FEATURE_ID, {
        "description": "TEST: Phiếu đề nghị SPMM.",
        "assigned_to_id": USER_HANG,
        "fixed_version_id": trial_ngoai_giao_id,
        "priority_id": PRIORITY_URGENT,
        "start_date": "2026-08-26",
        "due_date": None,
        "status_id": 2,
        "done_ratio": 0,
    })
    assert_issue(ba, TRACKER_TASK, USER_QUYNH, FEATURE_ID)
    assert_issue(dev, TRACKER_TASK, USER_LAM, FEATURE_ID)
    assert_issue(test, TRACKER_TASK, USER_HANG, FEATURE_ID)
    ba = close_via_workflow(ba)
    dev = close_via_workflow(dev)

    ensure_blocks(int(ba["id"]), int(dev["id"]))
    ensure_blocks(int(dev["id"]), int(test["id"]))

    print(f"Target Version: Trial - Cơ yếu Ngoại giao - 15/09 (id={trial_ngoai_giao_id})")
    print(f"Epic:   #{epic_id} {BASE_URL}/issues/{epic_id}")
    print(f"Feature: #{FEATURE_ID} {BASE_URL}/issues/{FEATURE_ID}")
    print(f"BA:     #{ba['id']} {BASE_URL}/issues/{ba['id']}")
    print(f"DEV:    #{dev['id']} {BASE_URL}/issues/{dev['id']}")
    print(f"TEST:   #{test['id']} {BASE_URL}/issues/{test['id']}")
    print("Relations: BA blocks DEV; DEV blocks TEST")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (requests.RequestException, RuntimeError, AssertionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
