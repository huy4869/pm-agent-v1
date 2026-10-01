"""Rename the BCY feature and all of its child tasks without changing other fields."""

from setup_redmine_spmm_hierarchy import PROJECT_ID, request


OLD_TITLE = "Quyết định giao chỉ tiêu kế hoạch ĐỘT XUẤT"
NEW_TITLE = "Quyết định giao chỉ tiêu kế hoạch BỔ SUNG"


def main() -> int:
    issues = request(
        "GET",
        "/issues.json",
        params={"project_id": PROJECT_ID, "status_id": "*", "limit": 100},
    ).json().get("issues", [])

    matches = [issue for issue in issues if OLD_TITLE in issue.get("subject", "")]
    if not matches:
        print("No matching issues found; nothing changed.")
        return 0

    for issue in matches:
        issue_id = int(issue["id"])
        old_subject = issue["subject"]
        new_subject = old_subject.replace(OLD_TITLE, NEW_TITLE)
        request("PUT", f"/issues/{issue_id}.json", json={"issue": {"subject": new_subject}})
        print(f"Updated #{issue_id}: {old_subject} -> {new_subject}")

    print(f"Updated {len(matches)} issue(s). Only the subject field was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
