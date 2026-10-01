"""Synchronize BCY Feature statuses from their BA/DEV/TEST child tasks."""

from __future__ import annotations

from setup_ngoai_giao_scope import sync_feature_status
from setup_redmine_spmm_hierarchy import (
    EPIC_SUBJECT,
    PROJECT_ID,
    TRACKER_FEATURE,
    TRACKER_TASK,
    find_issue,
    get_issue,
    request,
)


def main() -> None:
    epic = find_issue(EPIC_SUBJECT)
    if not epic:
        raise RuntimeError(f"Epic not found: {EPIC_SUBJECT}")
    epic_id = int(epic["id"])
    data = request(
        "GET",
        "/issues.json",
        params={"project_id": PROJECT_ID, "status_id": "*", "limit": 100},
    ).json()
    issues = data.get("issues", [])
    features = [
        issue for issue in issues
        if issue.get("tracker", {}).get("id") == TRACKER_FEATURE
        and (issue.get("parent") or {}).get("id") == epic_id
    ]
    tasks_by_parent: dict[int, list[dict]] = {}
    for issue in issues:
        parent_id = (issue.get("parent") or {}).get("id")
        if issue.get("tracker", {}).get("id") == TRACKER_TASK and parent_id:
            tasks_by_parent.setdefault(int(parent_id), []).append(issue)

    for feature in features:
        feature_id = int(feature["id"])
        updated = sync_feature_status(
            get_issue(feature_id), tasks_by_parent.get(feature_id, [])
        )
        print(f"#{feature_id}: {updated['status']['name']} - {updated['subject']}")


if __name__ == "__main__":
    main()
