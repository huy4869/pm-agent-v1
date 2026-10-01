"""Sync non-blank BA/DEV/TEST PIC values from BCY Master control."""

from sync_task_schedule_status import all_project_issues
from setup_redmine_spmm_hierarchy import request


PIC_IDS = {
    "Quynhdtn17": 117,
    "Huongntm62": 119,
    "Anhdv76": 114,
    "Lampt45": 118,
    "Hanglt102": 115,
    # Not mapped to a Redmine project member.
    "Anhnt634": None,
}


def assignment(subject: str, pic: str) -> tuple[str, str]:
    return subject, pic


ASSIGNMENTS = [
    assignment("BA - Phiếu đề nghị SPMM", "Quynhdtn17"),
    assignment("DEV - Phiếu đề nghị SPMM", "Lampt45"),
    assignment("TEST - Phiếu đề nghị SPMM", "Hanglt102"),
    assignment("BA - Quyết định giao chỉ tiêu kế hoạch Năm", "Quynhdtn17"),
    assignment("DEV - Quyết định giao chỉ tiêu kế hoạch Năm", "Anhdv76"),
    assignment("TEST - Quyết định giao chỉ tiêu kế hoạch Năm", "Hanglt102"),
    assignment("BA - Quyết định giao chỉ tiêu kế hoạch BỔ SUNG", "Quynhdtn17"),
    assignment("DEV - Quyết định giao chỉ tiêu kế hoạch BỔ SUNG", "Anhdv76"),
    assignment("BA - Quyết định triển khai", "Huongntm62"),
    assignment("DEV - Quyết định triển khai", "Anhdv76"),
    assignment("TEST - Quyết định triển khai", "Hanglt102"),
    assignment("BA - Thực thi cài đặt", "Huongntm62"),
    assignment("DEV - Thực thi cài đặt", "Lampt45"),
    assignment("TEST - Thực thi cài đặt", "Hanglt102"),
    assignment("BA - Hợp đồng sản xuất", "Anhnt634"),
    assignment("DEV - Hợp đồng sản xuất", "Anhdv76"),
    assignment("BA - Nhập kho", "Quynhdtn17"),
    assignment("DEV - Nhập kho", "Lampt45"),
    assignment("BA - Điều chuyển", "Huongntm62"),
    assignment("DEV - Điều chuyển", "Lampt45"),
    assignment("BA - Cấp phát", "Anhnt634"),
    assignment("DEV - Cấp phát", "Lampt45"),
    assignment("BA - Danh sách tài sản", "Quynhdtn17"),
    assignment("BA - Sửa chữa", "Quynhdtn17"),
    assignment("BA - Kiểm kê", "Quynhdtn17"),
    assignment("BA - Thu hồi", "Quynhdtn17"),
    assignment("BA - Tiêu hủy", "Anhnt634"),
    assignment("BA - Đơn vị (Department)", "Quynhdtn17"),
    assignment("DEV - Đơn vị (Department)", "Lampt45"),
    assignment("TEST - Đơn vị (Department)", "Hanglt102"),
    assignment("BA - Chỉnh sửa Master data Đơn vị sản xuất & Đơn vị", "Quynhdtn17"),
    assignment("DEV - Đơn vị và Đơn vị sản xuất", "Anhdv76"),
    assignment("TEST - Đơn vị và Đơn vị sản xuất", "Hanglt102"),
    assignment("BA - Tài khoản", "Quynhdtn17"),
    assignment("BA - Biểu mẫu", "Quynhdtn17"),
    assignment("BA - Bảng giá", "Anhnt634"),
    assignment("DEV - Bảng giá", "Anhdv76"),
    assignment("BA - Phân loại SPMM", "Quynhdtn17"),
    assignment("DEV - Phân loại SPMM", "Anhdv76"),
    assignment("TEST - Phân loại SPMM", "Hanglt102"),
]


def main() -> int:
    issues = all_project_issues()
    by_subject = {str(issue["subject"]): issue for issue in issues}
    updated = 0
    unchanged = 0
    unmapped: list[str] = []
    missing: list[str] = []

    for subject, pic in ASSIGNMENTS:
        issue = by_subject.get(subject)
        if not issue:
            missing.append(subject)
            continue
        user_id = PIC_IDS[pic]
        if user_id is None:
            unmapped.append(f"{subject}: {pic}")
            continue
        current_id = int(issue.get("assigned_to", {}).get("id", 0))
        if current_id == user_id:
            unchanged += 1
            continue
        request(
            "PUT",
            f"/issues/{issue['id']}.json",
            json={"issue": {"assigned_to_id": user_id}},
        )
        updated += 1
        print(f"Updated #{issue['id']} | {subject} | {pic} (#{user_id})")

    print(f"Updated {updated}; unchanged {unchanged}.")
    if unmapped:
        print("Unmapped PIC values:")
        for value in unmapped:
            print(f"- {value}")
    if missing:
        print("Missing tasks:")
        for value in missing:
            print(f"- {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
