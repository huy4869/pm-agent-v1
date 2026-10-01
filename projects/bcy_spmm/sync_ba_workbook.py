"""Apply reviewed BA workbook updates to the existing BCY Redmine hierarchy."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from inspect_ba_excel import read_workbook
from setup_ngoai_giao_scope import transition
from setup_redmine_spmm_hierarchy import (
    EPIC_SUBJECT,
    TRACKER_TASK,
    find_issue,
    get_issue,
    request,
    update_issue,
)


def child_tasks(feature_id: int) -> list[dict[str, Any]]:
    data = request(
        "GET",
        "/issues.json",
        params={"parent_id": feature_id, "status_id": "*", "limit": 100},
    ).json()
    return [
        issue
        for issue in data.get("issues", [])
        if issue.get("tracker", {}).get("id") == TRACKER_TASK
        and (issue.get("parent") or {}).get("id") == feature_id
    ]


def rename_feature(epic_id: int) -> int:
    old_subject = "Đơn vị sản xuất"
    new_subject = "Đơn vị và Đơn vị sản xuất"
    feature = find_issue(new_subject, epic_id) or find_issue(old_subject, epic_id)
    if not feature:
        raise RuntimeError(f"Feature not found: {old_subject}")
    feature_id = int(feature["id"])
    update_issue(feature_id, {
        "subject": new_subject,
        "description": "Scope: Vấn đề: Đang chưa mapping được tài khoản là của 1 đơn vị sản xuất với 1 đơn vị sản xuất thực tế trên HĐ (nên phân quyền dữ liệu không đúng)\n\nModule: Cấu hình hệ thống",
    })
    for task in child_tasks(feature_id):
        subject = str(task["subject"])
        phase = subject.split(" - ", 1)[0]
        new_task_subject = (
            "BA - Chỉnh sửa Master data Đơn vị sản xuất & Đơn vị"
            if phase == "BA"
            else f"{phase} - {new_subject}"
        )
        fields: dict[str, Any] = {"subject": new_task_subject}
        description = str(get_issue(int(task["id"])).get("description", ""))
        if "Requirement " not in description:
            fields["description"] = f"{phase}: {new_task_subject.split(' - ', 1)[1]}."
        update_issue(int(task["id"]), fields)
    return feature_id


def update_general_changes(epic_id: int) -> None:
    # Bảng giá: workbook now assigns DEV to Anhdv76 and marks it Doing.
    feature = find_issue("Bảng giá", epic_id)
    if not feature:
        raise RuntimeError("Feature not found: Bảng giá")
    dev = find_issue("DEV - Bảng giá", int(feature["id"]))
    if not dev:
        raise RuntimeError("Task not found: DEV - Bảng giá")
    dev_issue = update_issue(int(dev["id"]), {"assigned_to_id": 114})
    transition(dev_issue, "Doing")

    # Phân loại SPMM: DEV cells are blank in the workbook.
    feature = find_issue("Phân loại SPMM", epic_id)
    if not feature:
        raise RuntimeError("Feature not found: Phân loại SPMM")
    dev = find_issue("DEV - Phân loại SPMM", int(feature["id"]))
    if not dev:
        raise RuntimeError("Task not found: DEV - Phân loại SPMM")
    dev_id = int(dev["id"])
    dev_issue = update_issue(dev_id, {
        "assigned_to_id": "", "start_date": None, "due_date": None, "status_id": 1,
    })
    if int(dev_issue["status"]["id"]) != 1:
        dev_issue = update_issue(dev_id, {"status_id": 2})
        dev_issue = update_issue(dev_id, {"status_id": 1})
    if int(dev_issue["status"]["id"]) != 1:
        raise RuntimeError(
            f"Workflow would not reset DEV - Phân loại SPMM to New; current={dev_issue['status']['name']}"
        )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: sync_ba_workbook.py <workbook.xlsx>")
    workbook = read_workbook(Path(sys.argv[1]))
    if "Thông tin chung" not in workbook:
        raise RuntimeError("Missing workbook sheet: Thông tin chung")

    epic = find_issue(EPIC_SUBJECT)
    if not epic:
        raise RuntimeError(f"Epic not found: {EPIC_SUBJECT}")
    epic_id = int(epic["id"])
    rename_feature(epic_id)
    update_general_changes(epic_id)
    print("Applied changes from sheet: Thông tin chung")


if __name__ == "__main__":
    main()
