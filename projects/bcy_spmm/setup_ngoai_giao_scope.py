"""Idempotently create the remaining Cơ yếu Ngoại giao scope in Redmine."""

from __future__ import annotations

import re
from typing import Any

from setup_redmine_spmm_hierarchy import (
    BASE_URL,
    EPIC_SUBJECT,
    PRIORITY_NORMAL,
    PRIORITY_HIGH,
    PRIORITY_URGENT,
    PROJECT_ID,
    STATUS_NEW,
    TRACKER_FEATURE,
    TRACKER_TASK,
    USER_HANG,
    USER_HUY,
    USER_LAM,
    USER_QUYNH,
    create_issue,
    ensure_blocks,
    ensure_target_versions,
    find_issue,
    get_issue,
    update_issue,
)


USER_ANH_DO_VIET = 114
USER_MAI_HUONG = 119

PIC_IDS = {
    "Quynhdtn17": USER_QUYNH,
    "Huongntm62": USER_MAI_HUONG,
    "Anhdv76": USER_ANH_DO_VIET,
    "Lampt45": USER_LAM,
    "Hanglt102": USER_HANG,
    # These users are not project members yet and intentionally remain unassigned.
    "Anhnt634": None,
    "Sonnt203": None,
}

STATUS_PATHS = {
    "Done": [2, 3, 5],       # In Progress -> Resolved -> Closed
    "Doing": [2],            # In Progress
    "Pending": [2, 4, 10],   # In Progress -> Feedback -> Held
    "Review": [2, 3, 4],     # In Progress -> Resolved -> Feedback
}

URGENT_FEATURES = {
    "Quyết định giao chỉ tiêu kế hoạch BỔ SUNG",
    "Quyết định triển khai",
    "Thực thi cài đặt",
    "Điều chuyển",
    "Cấp phát",
    "Danh sách tài sản",
    "Sửa chữa",
    "Kiểm kê",
    "Thu hồi",
    "Tiêu hủy",
}

TASK_SUBJECT_OVERRIDES = {
    ("BA", "Đơn vị và Đơn vị sản xuất"): "BA - Chỉnh sửa Master data Đơn vị sản xuất & Đơn vị",
}


def stage(
    pic: str = "",
    start: str | None = None,
    due: str | None = None,
    status: str = "",
    note: str = "",
) -> dict[str, Any]:
    return {"pic": pic, "start": start, "due": due, "status": status, "note": note}


SCOPE = [
    {
        "subject": "Quyết định giao chỉ tiêu kế hoạch Năm",
        "scope": "Tạm ẩn QĐGCTKH tạo thủ công.",
        "priority": "Cao",
        "ba": stage("Quynhdtn17", "2026-08-19", "2026-08-21", "Done", "https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=335-32882&t=cRZlJxa6ABcCTPlP-4"),
        "dev": stage("Anhdv76", "2026-08-22", "2026-08-26", "Done", "https://10.86.60.81/procurement/purchase-requisition"),
        "test": stage("Hanglt102"),
    },
    {
        "subject": "Quyết định giao chỉ tiêu kế hoạch BỔ SUNG",
        "scope": "",
        "priority": "",
        "feature_status": "Pending",
        "ba": stage("Quynhdtn17", "2026-08-22", None, "Pending"),
        "dev": stage("Anhdv76"),
        "test": stage(),
    },
    {
        "subject": "Quyết định triển khai",
        "scope": "",
        "priority": "Cao",
        "ba": stage("Huongntm62", "2026-08-19", "2026-08-22", "Done", "https://gitlab.fis.vn/akames/project-knowledge/bcy/documents/-/blob/master/ngoai-giao/quyet-dinh-trien-khai/html-design/quyet-dinh-trien-khai-prototype.html?ref_type=heads"),
        "dev": stage("Anhdv76", "2026-08-26", "2026-09-03", "Doing"),
        "test": stage(),
    },
    {
        "subject": "Thực thi cài đặt",
        "scope": "Màn cũ là kế hoạch cài đặt cấp phát; chỉ nhập thông tin về tham số cài đặt thực tế, cấp nào cũng nhập được.",
        "priority": "Cao",
        "ba": stage("Huongntm62", "2026-08-24", "2026-08-26", "Done", "https://gitlab.fis.vn/akames/project-knowledge/bcy/documents/-/blob/master/ngoai-giao/thuc-thi-cai-dat/html-wireframe/thuc-thi-cai-dat-wireframe.html?ref_type=heads"),
        "dev": stage("Lampt45", "2026-08-28", "2026-09-04"),
        "test": stage(),
    },
    {
        "subject": "Hợp đồng sản xuất",
        "scope": "",
        "priority": "Cao",
        "ba": stage("Anhnt634", "2026-08-19", "2026-08-22", "Done", "https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=728-2&t=4uDbgEh8zpauOkCY-4"),
        "dev": stage(), "test": stage(),
    },
    {
        "subject": "Nhập kho",
        "scope": "Điều chỉnh giảm validate theo nhập kho Cục.",
        "priority": "Cao",
        "ba": stage("Sonnt203", "2026-08-19", "2026-08-24", "Doing"),
        "dev": stage(), "test": stage(),
    },
    {
        "subject": "Điều chuyển",
        "scope": "Điều chuyển từ Cục QL sang Cục CY đi theo QĐGCTKH hoặc QĐTK, không đi theo KHCĐCP.",
        "priority": "Cao",
        "ba": stage("Huongntm62", "2026-08-26", "2026-09-03", "Doing"),
        "dev": stage(), "test": stage(),
    },
    {
        "subject": "Cấp phát",
        "scope": "Cấp phát Đang sử dụng/Dự phòng.",
        "priority": "Cao",
        "ba": stage("Anhnt634", "2026-08-22", None, "Review"),
        "dev": stage(), "test": stage(),
    },
    {
        "module": "Quản lý tài sản", "subject": "Danh sách tài sản", "scope": "", "priority": "Cao",
        "ba": stage("Sonnt203", "2026-08-24", "2026-08-27", "Review"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Quản lý tài sản", "subject": "Sửa chữa",
        "scope": "Ngoại giao không sửa chữa tài sản; thường khi hỏng sẽ thu hồi hoặc tiêu hủy tại chỗ vì ở nước ngoài.",
        "priority": "Cao", "ba": stage("Sonnt203"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Quản lý tài sản", "subject": "Kiểm kê", "scope": "Tạm pending.", "priority": "",
        "ba": stage("Sonnt203"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Quản lý tài sản", "subject": "Thu hồi", "scope": "Đổi trạng thái.", "priority": "Cao",
        "ba": stage("Quynhdtn17"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Quản lý tài sản", "subject": "Tiêu hủy", "scope": "Đổi trạng thái.", "priority": "Cao",
        "ba": stage("Quynhdtn17"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Cấu hình hệ thống", "subject": "Đơn vị (Department)",
        "scope": "Chỉnh sửa màn Master Data - Đơn vị.", "priority": "Cao",
        "ba": stage("Quynhdtn17", None, "2026-08-18", "Done", "Mô tả thay đổi"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Cấu hình hệ thống", "subject": "Đơn vị và Đơn vị sản xuất",
        "scope": "Vấn đề: Đang chưa mapping được tài khoản là của 1 đơn vị sản xuất với 1 đơn vị sản xuất thực tế trên HĐ (nên phân quyền dữ liệu không đúng)",
        "priority": "", "ba": stage("Quynhdtn17", None, "2026-08-28", "Done"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Cấu hình hệ thống", "subject": "Tài khoản",
        "scope": "Tài khoản gán vào phòng ban hay đơn vị.", "priority": "Cao",
        "ba": stage("Quynhdtn17"), "dev": stage(), "test": stage(),
    },
    {
        "module": "Cấu hình hệ thống", "subject": "Biểu mẫu",
        "scope": "Chỉnh sửa màn Master Data - Đơn vị.", "priority": "Cao",
        "ba": stage(), "dev": stage(), "test": stage(),
    },
    {
        "module": "Cấu hình hệ thống", "subject": "Bảng giá",
        "scope": "Giá liên kết sang QĐGCTKH và Hợp đồng.", "priority": "Cao",
        "ba": stage("Anhnt634", None, None, "Done", "https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-9775&t=KNGF1u9qBaKiQcW2-4"),
        "dev": stage("Anhdv76", "2026-09-03", "2026-09-03", "Doing"), "test": stage(),
    },
    {
        "module": "Cấu hình hệ thống", "subject": "Phân loại SPMM",
        "scope": "Màn thêm mới Danh mục sản phẩm và giá trị dữ liệu: Ẩn cột Loại sản phẩm; chỉ có một cấp phân loại sản phẩm.",
        "priority": "", "ba": stage("Quynhdtn17", None, "2026-08-19", "Done"),
        "dev": stage(), "test": stage(),
    },
]


def meaningful(data: dict[str, Any]) -> bool:
    return any(data.get(key) for key in ("pic", "start", "due", "status", "note"))


def transition(issue: dict[str, Any], source_status: str) -> dict[str, Any]:
    target_path = STATUS_PATHS.get(source_status, [])
    current = int(issue["status"]["id"])
    if current in target_path:
        target_path = target_path[target_path.index(current) + 1 :]
    elif current != STATUS_NEW:
        return issue
    for status_id in target_path:
        issue = update_issue(int(issue["id"]), {"status_id": status_id})
    return issue


def sync_feature_status(feature: dict[str, Any], tasks: list[dict[str, Any]]) -> dict[str, Any]:
    if not tasks:
        return feature
    statuses = [int(task["status"]["id"]) for task in tasks]
    if 10 in statuses:              # Held/Pending takes precedence.
        source_status = "Pending"
    elif 2 in statuses:             # An actively executing phase.
        source_status = "Doing"
    elif 4 in statuses:             # Waiting for review/feedback.
        source_status = "Review"
    elif all(status == 5 for status in statuses):
        source_status = "Done"
    elif 5 in statuses and STATUS_NEW in statuses:
        source_status = "Doing"    # Some phases done, a later phase not started.
    else:
        return feature
    return transition(feature, source_status)


def upsert_task(
    feature_id: int, phase: str, feature_subject: str, data: dict[str, Any], version_id: int, priority_id: int
) -> dict[str, Any]:
    subject = TASK_SUBJECT_OVERRIDES.get(
        (phase, feature_subject), f"{phase} - {feature_subject}"
    )
    task_label = subject.split(" - ", 1)[1]
    description = f"{phase}: {task_label}."
    urls = re.findall(r"https?://[^\s)]+", str(data.get("note", "")))
    if phase != "DEV":
        for url in dict.fromkeys(urls):
            label = "Figma" if "figma.com" in url.casefold() else "Doc"
            description += f"\n\n{label}: {url}"
    fields: dict[str, Any] = {
        "project_id": PROJECT_ID, "tracker_id": TRACKER_TASK,
        "parent_issue_id": feature_id, "fixed_version_id": version_id,
        "subject": subject, "description": description,
        "start_date": data.get("start"), "due_date": data.get("due"),
    }
    fields["priority_id"] = priority_id
    assignee = PIC_IDS.get(str(data.get("pic", "")))
    # Explicit null prevents Redmine from applying its default assignee when
    # the supplied PIC is blank or is not yet a member of this project.
    fields["assigned_to_id"] = assignee if assignee is not None else ""
    existing = find_issue(subject, feature_id)
    if existing and phase == "BA" and "Requirement " in str(get_issue(int(existing["id"])).get("description", "")):
        fields.pop("description", None)
    issue = update_issue(int(existing["id"]), fields) if existing else create_issue(fields)
    return transition(issue, str(data.get("status", "")))


def main() -> None:
    epic = find_issue(EPIC_SUBJECT)
    if not epic:
        raise RuntimeError(f"Epic not found: {EPIC_SUBJECT}")
    epic_id = int(epic["id"])
    version_id = ensure_target_versions()["Trial - Cơ yếu Ngoại giao - 15/09"]
    created_features: list[int] = []
    created_tasks: list[int] = []

    for item in SCOPE:
        subject = str(item["subject"])
        description_parts: list[str] = []
        if item.get("scope"):
            description_parts.append(f"Scope: {item['scope']}")
        if item.get("module"):
            description_parts.append(f"Module: {item['module']}")
        feature_fields: dict[str, Any] = {
            "project_id": PROJECT_ID, "tracker_id": TRACKER_FEATURE,
            "parent_issue_id": epic_id, "fixed_version_id": version_id,
            "assigned_to_id": USER_HUY, "subject": subject,
            "description": "\n\n".join(description_parts),
        }
        if subject in URGENT_FEATURES:
            feature_fields["priority_id"] = PRIORITY_URGENT
        else:
            feature_fields["priority_id"] = PRIORITY_NORMAL
        existing = find_issue(subject, epic_id)
        feature = update_issue(int(existing["id"]), feature_fields) if existing else create_issue(feature_fields)
        if item.get("feature_status"):
            feature = transition(feature, str(item["feature_status"]))
        feature_id = int(feature["id"])
        if feature.get("status", {}).get("is_closed"):
            feature = update_issue(feature_id, {"status_id": 2})
        created_features.append(feature_id)

        phase_issues: dict[str, dict[str, Any]] = {}
        for phase, key in (("BA", "ba"), ("DEV", "dev"), ("TEST", "test")):
            # Every Feature must have DEV and TEST placeholders. Missing source
            # data stays null/New/unassigned; BA is created only when supplied.
            if phase in {"DEV", "TEST"} or meaningful(item[key]):
                task_priority_id = PRIORITY_URGENT if subject in URGENT_FEATURES else PRIORITY_NORMAL
                issue = upsert_task(feature_id, phase, subject, item[key], version_id, task_priority_id)
                phase_issues[phase] = issue
                created_tasks.append(int(issue["id"]))
        if "BA" in phase_issues and "DEV" in phase_issues:
            ensure_blocks(int(phase_issues["BA"]["id"]), int(phase_issues["DEV"]["id"]))
        if "DEV" in phase_issues and "TEST" in phase_issues:
            ensure_blocks(int(phase_issues["DEV"]["id"]), int(phase_issues["TEST"]["id"]))
        sync_feature_status(feature, list(phase_issues.values()))

    print(f"Upserted {len(created_features)} features and {len(created_tasks)} phase tasks.")
    print(f"Epic: {BASE_URL}/issues/{epic_id}")
    print("Unassigned PICs (not project members): Anhnt634, Sonnt203")


if __name__ == "__main__":
    main()
