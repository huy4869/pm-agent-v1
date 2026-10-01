"""Create the approved PTSC Marine AMS maintenance bugs idempotently."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "projects" / "bcy_spmm"))

from setup_redmine_spmm_hierarchy import request  # noqa: E402


PROJECT_ID = 63
EPIC_ID = 10253
ASSIGNEE_ID = 110
TRACKER_BUG = 1

BUGS = [
    {
        "subject": "Có thể tạo mới phiếu On/Off Hire khi đã tồn tại phiếu trạng thái Mới",
        "module": "Quản lý HĐ tàu → Giám sát hoạt động tàu → Biên bản On/Off Hire",
        "description": "Hệ thống vẫn cho phép tạo thêm phiếu On/Off Hire khi đã tồn tại 01 phiếu ở trạng thái Mới.",
        "current": "Có thể tồn tại đồng thời 02 phiếu On Hire ở trạng thái Mới.",
        "expected": "Chỉ cho phép tồn tại 01 phiếu On/Off Hire ở trạng thái Mới.",
    },
    {
        "subject": "Báo cáo hoạt động và tiêu thụ nhiên liệu không hiển thị đầy đủ tàu nội bộ",
        "module": "Quản lý HĐ tàu → Báo cáo → Báo cáo hoạt động và tiêu thụ nhiên liệu tàu",
        "description": "Báo cáo chưa hiển thị đầy đủ danh sách tàu nội bộ; ghi nhận thiếu tàu Sao Vàng và Vũng Tàu.",
        "current": "Một số tàu nội bộ không hiển thị trên báo cáo.",
        "expected": "Hiển thị đầy đủ tàu nội bộ, kể cả tàu đang On/Off Hire.",
    },
    {
        "subject": "Vùng hoạt động mặc định chưa đúng đối với tàu PTSC và tàu thuê bare",
        "module": "Quản lý HĐ tàu → Báo cáo → Báo cáo hiệu suất đội tàu",
        "description": "Một số tàu PTSC và tàu thuê bare chưa có thông tin Vùng hoạt động, hệ thống đang xác định giá trị mặc định chưa đúng.",
        "current": "Khi chưa có Vùng hoạt động, hệ thống đang mặc định là Nước ngoài.",
        "expected": "Khi chưa có Vùng hoạt động, mặc định là Việt Nam.",
    },
]


def issue_description(item: dict[str, str]) -> str:
    return (
        f"Module: {item['module']}\n\n"
        f"Description: {item['description']}\n\n"
        f"Current Result: {item['current']}\n\n"
        f"Expected Result: {item['expected']}"
    )


def main() -> None:
    epic = request("GET", f"/issues/{EPIC_ID}.json").json()["issue"]
    assert epic["project"]["id"] == PROJECT_ID
    assert epic["tracker"]["id"] == 6

    existing = request(
        "GET",
        "/issues.json",
        params={"project_id": PROJECT_ID, "status_id": "*", "limit": 100},
    ).json()["issues"]

    for item in BUGS:
        matches = [issue for issue in existing if issue["subject"].strip() == item["subject"]]
        if len(matches) > 1:
            raise RuntimeError(f"Multiple issues already use subject: {item['subject']}")
        if matches:
            issue_id = int(matches[0]["id"])
            action = "EXISTING"
        else:
            created = request(
                "POST",
                "/issues.json",
                json={
                    "issue": {
                        "project_id": PROJECT_ID,
                        "tracker_id": TRACKER_BUG,
                        "parent_issue_id": EPIC_ID,
                        "assigned_to_id": ASSIGNEE_ID,
                        "subject": item["subject"],
                        "description": issue_description(item),
                    }
                },
            ).json()["issue"]
            issue_id = int(created["id"])
            action = "CREATED"

        checked = request("GET", f"/issues/{issue_id}.json").json()["issue"]
        assert checked["project"]["id"] == PROJECT_ID
        assert checked["tracker"]["id"] == TRACKER_BUG
        assert checked["parent"]["id"] == EPIC_ID
        assert checked["assigned_to"]["id"] == ASSIGNEE_ID
        actual_description = checked["description"].replace("\r\n", "\n")
        assert actual_description == issue_description(item)
        print(f"{action} #{issue_id} | {checked['subject']}")


if __name__ == "__main__":
    main()
