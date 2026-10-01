"""Sync only task status/start/due fields from the approved BCY status sheet.

This script intentionally never updates assignee, description, or priority on
existing issues. Blank source values are omitted and preserve Redmine data.
"""

from __future__ import annotations

from typing import Any

from setup_redmine_spmm_hierarchy import (
    EPIC_SUBJECT,
    PRIORITY_NORMAL,
    PROJECT_ID,
    TRACKER_TASK,
    find_issue,
    get_issue,
    request,
)


STATUS_IDS = {
    "Done": 3,       # Resolved until BA, DEV, and TEST are all Done
    "Doing": 2,      # In Progress
    "Pending": 10,   # Held
    "Review": 4,     # Feedback
}

# BA and DEV tasks may be Closed when both stages are Done. TEST stays Resolved
# until there is an explicit confirmation that testing passed with no bugs.
BA_DEV_DONE_FEATURES = {
    "Phiếu đề nghị SPMM",
    "Quyết định giao chỉ tiêu kế hoạch Năm",
    "Quyết định triển khai",
    "Thực thi cài đặt",
    "Đơn vị (Department)",
    "Đơn vị và Đơn vị sản xuất",
    "Chỉnh sửa Master data Đơn vị sản xuất & Đơn vị",
    "Bảng giá",
    "Phân loại SPMM",
}


def target_status_id(subject: str, source_status: str) -> int:
    if source_status != "Done":
        return STATUS_IDS[source_status]
    is_ba_or_dev = subject.startswith("BA - ") or subject.startswith("DEV - ")
    ba_dev_complete = any(subject.endswith(name) for name in BA_DEV_DONE_FEATURES)
    return 5 if is_ba_or_dev and ba_dev_complete else 3

FROM_NEW_PATHS = {
    2: [2],
    4: [2, 4],
    10: [2, 4, 10],
    5: [2, 3, 5],
}

FALLBACK_PATHS = {
    2: [2],
    3: [2, 3],
    4: [2, 4],
    10: [2, 4, 10],
    5: [2, 3, 5],
}


def item(
    subject: str,
    status: str = "",
    start: str | None = None,
    due: str | None = None,
) -> dict[str, Any]:
    return {"subject": subject, "status": status, "start": start, "due": due}


UPDATES = [
    item("BA - Phiếu đề nghị SPMM", "Done", due="2026-08-19"),
    item("DEV - Phiếu đề nghị SPMM", "Done", "2026-08-19", "2026-08-25"),
    item("TEST - Phiếu đề nghị SPMM", "Done", "2026-08-26", "2026-09-03"),
    item("BA - Quyết định giao chỉ tiêu kế hoạch Năm", "Done", "2026-08-19", "2026-08-21"),
    item("DEV - Quyết định giao chỉ tiêu kế hoạch Năm", "Done", "2026-08-22", "2026-08-26"),
    item("TEST - Quyết định giao chỉ tiêu kế hoạch Năm", "Done", "2026-09-03", "2026-09-03"),
    item("BA - Quyết định giao chỉ tiêu kế hoạch BỔ SUNG", "Done", "2026-08-22", "2026-09-03"),
    item("DEV - Quyết định giao chỉ tiêu kế hoạch BỔ SUNG", "Doing"),
    item("BA - Quyết định triển khai", "Done", "2026-08-19", "2026-08-22"),
    item("DEV - Quyết định triển khai", "Done", "2026-08-26", "2026-09-03"),
    item("TEST - Quyết định triển khai", "Done", "2026-09-03", "2026-09-04"),
    item("BA - Thực thi cài đặt", "Done", "2026-08-24", "2026-08-26"),
    item("DEV - Thực thi cài đặt", "Done", "2026-08-28", "2026-09-04"),
    item("TEST - Thực thi cài đặt", "Doing", "2026-09-07"),
    item("BA - Hợp đồng sản xuất", "Done", "2026-08-19", "2026-08-22"),
    item("DEV - Hợp đồng sản xuất", "Doing", "2026-09-07"),
    item("BA - Nhập kho", "Done", "2026-08-19", "2026-08-24"),
    item("DEV - Nhập kho", "Doing", "2026-09-07", "2026-09-08"),
    item("BA - Điều chuyển", "Done", "2026-08-26", "2026-09-03"),
    item("BA - Cấp phát", "Review", "2026-08-22"),
    item("BA - Danh sách tài sản", "Doing", "2026-08-24", "2026-08-27"),
    item("BA - Sửa chữa", "Pending"),
    item("BA - Kiểm kê", "Pending"),
    item("BA - Thu hồi", "Pending"),
    item("BA - Đơn vị (Department)", "Done", due="2026-08-18"),
    item("DEV - Đơn vị (Department)", "Done"),
    item("TEST - Đơn vị (Department)", "Done", "2026-09-04", "2026-09-04"),
    item("BA - Chỉnh sửa Master data Đơn vị sản xuất & Đơn vị", "Done", due="2026-08-28"),
    item("DEV - Đơn vị và Đơn vị sản xuất", "Done", "2026-09-03", "2026-09-03"),
    item("TEST - Đơn vị và Đơn vị sản xuất", "Done", "2026-09-04", "2026-09-04"),
    item("DEV - Tiêu hủy", "Doing"),
    item("BA - Tài khoản", "Pending"),
    item("BA - Biểu mẫu", "Pending"),
    item("BA - Bảng giá", "Done"),
    item("DEV - Bảng giá", "Done", "2026-09-03", "2026-09-03"),
    item("TEST - Bảng giá", "Done", "2026-09-04", "2026-09-04"),
    item("BA - Phân loại SPMM", "Done", due="2026-08-19"),
    item("DEV - Phân loại SPMM", "Done"),
    item("TEST - Phân loại SPMM", "Done", "2026-09-07", "2026-09-07"),
]


def all_project_issues() -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    offset = 0
    while True:
        payload = request(
            "GET", "/issues.json",
            params={
                "project_id": PROJECT_ID,
                "status_id": "*",
                "limit": 100,
                "offset": offset,
            },
        ).json()
        page = payload.get("issues", [])
        issues.extend(page)
        offset += len(page)
        if not page or offset >= int(payload.get("total_count", len(issues))):
            return issues


def create_missing_ba_bieu_mau() -> dict[str, Any]:
    epic = find_issue(EPIC_SUBJECT)
    if not epic:
        raise RuntimeError(f"Epic not found: {EPIC_SUBJECT}")
    feature = find_issue("Biểu mẫu", int(epic["id"]))
    if not feature:
        raise RuntimeError("Feature not found: Biểu mẫu")
    response = request(
        "POST", "/issues.json",
        json={"issue": {
            "project_id": PROJECT_ID,
            "tracker_id": TRACKER_TASK,
            "parent_issue_id": int(feature["id"]),
            "fixed_version_id": 21,
            "subject": "BA - Biểu mẫu",
            "assigned_to_id": "",
            "description": "",
            "priority_id": PRIORITY_NORMAL,
            "start_date": "",
            "due_date": "",
        }},
    )
    return get_issue(int(response.json()["issue"]["id"]))


def set_status(issue: dict[str, Any], target_id: int) -> dict[str, Any]:
    issue_id = int(issue["id"])
    if int(issue["status"]["id"]) == target_id:
        return issue
    request("PUT", f"/issues/{issue_id}.json", json={"issue": {"status_id": target_id}})
    issue = get_issue(issue_id)
    if int(issue["status"]["id"]) == target_id:
        return issue
    for status_id in FALLBACK_PATHS[target_id]:
        if int(issue["status"]["id"]) == target_id:
            break
        request("PUT", f"/issues/{issue_id}.json", json={"issue": {"status_id": status_id}})
        issue = get_issue(issue_id)
    if int(issue["status"]["id"]) != target_id:
        raise RuntimeError(
            f"#{issue_id}: workflow could not change {issue['status']['name']} to status {target_id}"
        )
    return issue


def main() -> None:
    issues = all_project_issues()
    by_subject = {str(issue["subject"]): issue for issue in issues}
    if "BA - Biểu mẫu" not in by_subject:
        created = create_missing_ba_bieu_mau()
        by_subject[str(created["subject"])] = created

    results: list[dict[str, Any]] = []
    errors: list[str] = []
    for source in UPDATES:
        issue = by_subject.get(source["subject"])
        if not issue:
            raise RuntimeError(f"Task not found: {source['subject']}")
        fields: dict[str, Any] = {}
        if source["start"] is not None:
            fields["start_date"] = source["start"]
        if source["due"] is not None:
            fields["due_date"] = source["due"]
        if fields:
            request("PUT", f"/issues/{issue['id']}.json", json={"issue": fields})
            issue = get_issue(int(issue["id"]))
        if source["status"]:
            try:
                issue = set_status(issue, target_status_id(source["subject"], source["status"]))
            except RuntimeError as exc:
                issue = get_issue(int(issue["id"]))
                errors.append(str(exc))
        results.append(issue)

    for issue in results:
        print(
            f"#{issue['id']} | {issue['status']['name']} | "
            f"{issue.get('start_date') or '-'} -> {issue.get('due_date') or '-'} | "
            f"{issue['subject']}"
        )
    if errors:
        print("\nWorkflow-blocked status changes:")
        for error in errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
