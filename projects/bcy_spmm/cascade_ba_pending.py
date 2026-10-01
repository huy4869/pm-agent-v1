"""Cascade BA Pending/Held status to sibling DEV and TEST tasks."""

from collections import defaultdict

from sync_task_schedule_status import all_project_issues, set_status


STATUS_HELD = 10


def main() -> int:
    issues = all_project_issues()
    children: dict[int, list[dict]] = defaultdict(list)
    for issue in issues:
        parent = issue.get("parent")
        if parent:
            children[int(parent["id"])].append(issue)

    updated = 0
    matched_features = 0
    for parent_id, siblings in children.items():
        ba_tasks = [
            issue
            for issue in siblings
            if issue.get("subject", "").startswith("BA - ")
            and int(issue["status"]["id"]) == STATUS_HELD
        ]
        if not ba_tasks:
            continue
        matched_features += 1
        print(f"Parent #{parent_id}: {ba_tasks[0]['subject']}")
        for issue in siblings:
            subject = issue.get("subject", "")
            if not (subject.startswith("DEV - ") or subject.startswith("TEST - ")):
                continue
            before = int(issue["status"]["id"])
            issue = set_status(issue, STATUS_HELD)
            if before != int(issue["status"]["id"]):
                updated += 1
            print(f"  #{issue['id']} | {issue['status']['name']} | {subject}")

    print(f"Matched {matched_features} feature(s); changed {updated} task status(es).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
