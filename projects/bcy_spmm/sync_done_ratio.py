"""Set progress to 100% for tasks marked Done in the approved BCY schedule."""

from sync_task_schedule_status import UPDATES, all_project_issues
from setup_redmine_spmm_hierarchy import request


def main() -> int:
    issues = all_project_issues()
    by_subject = {str(issue["subject"]): issue for issue in issues}
    done_subjects = [item["subject"] for item in UPDATES if item["status"] == "Done"]

    updated = 0
    for subject in done_subjects:
        issue = by_subject.get(subject)
        if not issue:
            raise RuntimeError(f"Task not found: {subject}")
        issue_id = int(issue["id"])
        if int(issue.get("done_ratio", 0)) != 100:
            request(
                "PUT",
                f"/issues/{issue_id}.json",
                json={"issue": {"done_ratio": 100}},
            )
            updated += 1
        print(f"#{issue_id} | 100% | {subject}")

    print(f"Updated {updated} task(s); verified {len(done_subjects)} Done task(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
