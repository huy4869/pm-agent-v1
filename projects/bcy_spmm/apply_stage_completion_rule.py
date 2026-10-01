"""Apply the BCY rule: close stage tasks only when BA, DEV and TEST are all Done."""

from sync_task_schedule_status import (
    UPDATES,
    all_project_issues,
    set_status,
    target_status_id,
)


def main() -> int:
    issues = all_project_issues()
    by_subject = {str(issue["subject"]): issue for issue in issues}
    changed = 0
    errors: list[str] = []

    for source in UPDATES:
        if source["status"] != "Done":
            continue
        issue = by_subject.get(source["subject"])
        if not issue:
            raise RuntimeError(f"Task not found: {source['subject']}")
        target_id = target_status_id(source["subject"], "Done")
        before_id = int(issue["status"]["id"])
        try:
            issue = set_status(issue, target_id)
        except RuntimeError as exc:
            errors.append(str(exc))
            issue = by_subject[source["subject"]]
        if before_id != int(issue["status"]["id"]):
            changed += 1
        print(
            f"#{issue['id']} | {issue['status']['name']} | "
            f"{issue.get('done_ratio', 0)}% | {issue['subject']}"
        )

    print(f"Changed {changed} task status(es).")
    if errors:
        print("Workflow-blocked status changes:")
        for error in errors:
            print(f"- {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
