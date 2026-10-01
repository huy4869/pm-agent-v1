"""Synchronize BCY Feature and child-task priorities."""

from __future__ import annotations

from setup_ngoai_giao_scope import URGENT_FEATURES
from setup_redmine_spmm_hierarchy import (
    EPIC_SUBJECT,
    FEATURE_SUBJECT,
    PRIORITY_HIGH,
    PRIORITY_NORMAL,
    PRIORITY_URGENT,
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
    urgent_subjects = set(URGENT_FEATURES) | {FEATURE_SUBJECT}
    data = request(
        "GET", "/issues.json",
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
        target = PRIORITY_URGENT if feature["subject"] in urgent_subjects else PRIORITY_NORMAL
        for task in tasks_by_parent.get(feature_id, []):
            request(
                "PUT", f"/issues/{task['id']}.json",
                json={"issue": {"priority_id": target}},
            )
        request(
            "PUT", f"/issues/{feature_id}.json",
            json={"issue": {"priority_id": target}},
        )

    failures: list[str] = []
    for feature in features:
        feature_id = int(feature["id"])
        expected = "Urgent" if feature["subject"] in urgent_subjects else "Normal"
        actual = get_issue(feature_id)["priority"]["name"]
        if actual != expected and expected == "Urgent" and actual != "High":
            failures.append(f"#{feature_id}: expected Urgent/High, got {actual}")
        elif actual != expected and expected == "Normal":
            failures.append(f"#{feature_id}: expected Normal, got {actual}")
        print(f"#{feature_id}: {actual} - {feature['subject']}")
    if failures:
        raise RuntimeError("; ".join(failures))


if __name__ == "__main__":
    main()
