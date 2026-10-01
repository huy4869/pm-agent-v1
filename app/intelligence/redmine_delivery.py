from __future__ import annotations

from collections import Counter
from typing import Any

from app.domain.statuses import is_active_status


PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2}
CLOSED_VERSION_STATUSES = {"closed", "done", "completed", "complete"}


def _action(
    action_id: str,
    priority: str,
    title: str,
    detail: str,
    *,
    category: str,
    count: int = 0,
    filter_name: str | None = None,
    version_id: str | None = None,
) -> dict[str, Any]:
    return {
        "id": action_id,
        "priority": priority,
        "title": title,
        "detail": detail,
        "category": category,
        "count": count,
        "filter": filter_name,
        "versionId": version_id,
    }


def _sort_actions(actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(actions, key=lambda item: (PRIORITY_ORDER.get(item["priority"], 9), -int(item.get("count") or 0), item["title"]))


def _project_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "overdue": sum(1 for x in issues if x.get("overdue")),
        "blocked": sum(1 for x in issues if x.get("blocked")),
        "blocking": sum(1 for x in issues if x.get("blocking")),
        "stale": sum(1 for x in issues if x.get("stale")),
        "unassigned": sum(1 for x in issues if x.get("unassigned")),
        "nearDue": sum(1 for x in issues if x.get("nearDue")),
        "pending": sum(1 for x in issues if x.get("pending")),
        "open": sum(1 for x in issues if not x.get("done")),
    }


def _version_is_closed(version: dict[str, Any]) -> bool:
    return str(version.get("status") or "").strip().lower() in CLOSED_VERSION_STATUSES


def build_project_delivery(
    issues: list[dict[str, Any]],
    current_version: dict[str, Any] | None,
    versions: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Deterministic delivery assessment for dashboard use.

    Uses only the already-collected snapshot. Closed versions are historical,
    while backlog/no-deadline versions are buckets rather than milestones.
    """

    counts = _project_counts(issues)
    actions: list[dict[str, Any]] = []
    reasons: list[str] = []
    critical = False
    at_risk = False

    # Open versions whose milestone date has already passed are risks, but they
    # must not be mislabeled as the "current" version.
    overdue_versions = [
        v for v in (versions or [])
        if not _version_is_closed(v)
        and v.get("dueDate") is not None
        and v.get("daysLeft") is not None
        and int(v["daysLeft"]) < 0
        and int(v.get("open") or 0) > 0
    ]
    for version in overdue_versions[:3]:
        days_late = abs(int(version["daysLeft"]))
        open_count = int(version.get("open") or 0)
        version_name = version.get("name") or "Version"
        version_id = str(version.get("id"))
        critical = True
        reasons.append(f"{version_name} đã quá hạn {days_late} ngày nhưng còn {open_count} task mở")
        actions.append(_action(
            f"overdue-version-{version_id}", "P0",
            f"Chốt phương án xử lý {version_name}",
            f"Milestone đã quá hạn {days_late} ngày, còn {open_count} task chưa hoàn tất.",
            category="version", count=open_count, filter_name="open", version_id=version_id,
        ))

    # "Current" is a dated, non-closed milestone from today onward. A backlog
    # without deadline never triggers milestone/deadline rules.
    if current_version and current_version.get("open", 0) > 0 and current_version.get("dueDate") is not None:
        days_left = current_version.get("daysLeft")
        progress = int(current_version.get("progress") or 0)
        open_count = int(current_version.get("open") or 0)
        version_id = str(current_version.get("id"))
        version_name = current_version.get("name") or "Version hiện tại"
        if days_left is not None and 0 <= int(days_left) <= 3 and progress < 70 and open_count >= 3:
            critical = True
            reasons.append(f"{version_name} chỉ còn {days_left} ngày, tiến độ {progress}%")
            actions.append(_action(
                "current-version-critical", "P0",
                f"Rà soát phạm vi {version_name}",
                f"Còn {days_left} ngày nhưng mới hoàn tất {progress}%, còn {open_count} task mở.",
                category="version", count=open_count, filter_name="open", version_id=version_id,
            ))
        elif days_left is not None and 0 <= int(days_left) <= 7 and progress < 80 and open_count > 0:
            at_risk = True
            reasons.append(f"{version_name} còn {days_left} ngày, tiến độ {progress}%")
            actions.append(_action(
                "current-version-watch", "P1",
                f"Review kế hoạch {version_name}",
                f"Còn {days_left} ngày, tiến độ {progress}%, {open_count} task vẫn đang mở.",
                category="version", count=open_count, filter_name="open", version_id=version_id,
            ))

    if counts["blocked"]:
        if counts["blocked"] >= 3:
            critical = True
        else:
            at_risk = True
        reasons.append(f"{counts['blocked']} task đang bị dependency chặn")
        actions.append(_action(
            "blocked", "P0" if counts["blocked"] >= 3 else "P1",
            f"Gỡ vướng {counts['blocked']} task bị chặn",
            "Mở danh sách Blocked để xác định blocker và owner cần xử lý.",
            category="blocked", count=counts["blocked"], filter_name="blocked",
        ))

    if counts["overdue"]:
        if counts["overdue"] >= 10:
            critical = True
        else:
            at_risk = True
        reasons.append(f"{counts['overdue']} task đã quá hạn")
        actions.append(_action(
            "overdue", "P0" if counts["overdue"] >= 10 else "P1",
            f"Xử lý {counts['overdue']} task quá hạn",
            "Xác nhận lại deadline, owner và kế hoạch hoàn thành cho các task quá hạn.",
            category="overdue", count=counts["overdue"], filter_name="overdue",
        ))

    if counts["unassigned"]:
        if counts["unassigned"] >= 3:
            at_risk = True
        actions.append(_action(
            "unassigned", "P1" if counts["unassigned"] >= 3 else "P2",
            f"Phân công owner cho {counts['unassigned']} task",
            "Chỉ tính task đang mở và không ở trạng thái Pending/Held.",
            category="unassigned", count=counts["unassigned"], filter_name="unassigned",
        ))

    if counts["stale"]:
        if counts["stale"] >= 3:
            at_risk = True
            reasons.append(f"{counts['stale']} task đang xử lý lâu không cập nhật")
        actions.append(_action(
            "stale", "P1" if counts["stale"] >= 3 else "P2",
            f"Follow-up {counts['stale']} task lâu không cập nhật",
            "Kiểm tra tiến độ thực tế và cập nhật trạng thái trên Redmine.",
            category="stale", count=counts["stale"], filter_name="stale",
        ))

    if counts["blocking"]:
        at_risk = True
        reasons.append(f"{counts['blocking']} task đang chặn task khác")
        actions.append(_action(
            "blocking", "P1",
            f"Ưu tiên {counts['blocking']} task đang block downstream",
            "Các task này có dependency ảnh hưởng trực tiếp đến công việc khác.",
            category="blocking", count=counts["blocking"], filter_name="blocking",
        ))

    # Pending/Held is informational by itself, not a hot spot. Only turn it into
    # a PM action when a real dated milestone is approaching.
    if counts["pending"] and current_version and current_version.get("dueDate") is not None and current_version.get("daysLeft") is not None:
        days_left = int(current_version["daysLeft"])
        if 0 <= days_left <= 7:
            pending_in_version = int(current_version.get("pending") or 0)
            if pending_in_version:
                at_risk = True
                reasons.append(f"{pending_in_version} task Pending/Held trong version sắp đến hạn")
                actions.append(_action(
                    "pending-near-milestone", "P1",
                    f"Rà soát {pending_in_version} task Pending/Held",
                    f"Version còn {days_left} ngày; cần xác nhận task nào tiếp tục giữ Pending và task nào phải kích hoạt lại.",
                    category="pending", count=pending_in_version, filter_name="pending", version_id=str(current_version.get("id")),
                ))

    workload = Counter(
        x.get("assignee")
        for x in issues
        if is_active_status(x.get("status")) and not x.get("done") and not x.get("pending") and x.get("assignee")
    )
    actionable_open = sum(workload.values())
    if workload and actionable_open >= 6:
        owner, count = workload.most_common(1)[0]
        if count >= 5 and count / actionable_open >= 0.5:
            at_risk = True
            reasons.append(f"Khối lượng đang tập trung {count}/{actionable_open} task đang xử lý vào {owner}")
            actions.append(_action(
                "workload-concentration", "P2",
                f"Rà soát tải công việc của {owner}",
                f"Đang giữ {count}/{actionable_open} task đang xử lý; cân nhắc điều phối lại nếu có nghẽn.",
                category="workload", count=count,
            ))

    level = "CRITICAL" if critical else "AT_RISK" if at_risk else "GREEN"
    if level == "GREEN":
        headline = "Chưa ghi nhận tín hiệu delivery cần PM xử lý từ dữ liệu Redmine hiện tại."
    elif level == "CRITICAL":
        headline = "Có tín hiệu delivery cần PM ưu tiên xử lý ngay."
    else:
        headline = "Có một số tín hiệu cần PM theo dõi và xử lý trong kỳ hiện tại."

    return {
        "level": level,
        "headline": headline,
        "reasons": reasons[:8],
        "counts": counts,
    }, _sort_actions(actions)[:10]


def build_version_delivery(
    version: dict[str, Any],
    issues: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    counts = _project_counts(issues)

    if _version_is_closed(version):
        return {
            "level": "GREEN",
            "headline": "Version đã đóng; dữ liệu được giữ để xem lịch sử, không đánh delivery risk hiện tại.",
            "reasons": [],
            "counts": counts,
        }, []

    actions: list[dict[str, Any]] = []
    reasons: list[str] = []
    critical = False
    at_risk = False
    version_id = str(version.get("id"))
    name = version.get("name") or "Version"
    days_left = version.get("daysLeft")
    progress = int(version.get("progress") or 0)

    # No deadline = backlog/work bucket. Do not infer milestone pressure from it.
    if counts["open"] > 0 and version.get("dueDate") is not None and days_left is not None and days_left < 0:
        critical = True
        reasons.append(f"Version đã quá hạn {abs(days_left)} ngày nhưng còn {counts['open']} task mở")
        actions.append(_action(
            "version-overdue", "P0", f"Chốt lại kế hoạch {name}",
            f"Version quá hạn {abs(days_left)} ngày, còn {counts['open']} task chưa hoàn tất.",
            category="version", count=counts["open"], filter_name="open", version_id=version_id,
        ))
    elif counts["open"] > 0 and version.get("dueDate") is not None and days_left is not None and 0 <= days_left <= 7 and progress < 80:
        at_risk = True
        reasons.append(f"Còn {days_left} ngày nhưng tiến độ mới {progress}%")
        actions.append(_action(
            "version-near-due", "P1", f"Review phạm vi {name}",
            f"Còn {days_left} ngày, tiến độ {progress}%, còn {counts['open']} task mở.",
            category="version", count=counts["open"], filter_name="open", version_id=version_id,
        ))

    if counts["blocked"]:
        critical = critical or counts["blocked"] >= 3
        at_risk = True
        reasons.append(f"{counts['blocked']} task bị chặn")
        actions.append(_action(
            "version-blocked", "P0" if counts["blocked"] >= 3 else "P1",
            f"Gỡ vướng {counts['blocked']} task blocked",
            "Các blocker trong version cần được xử lý trước khi tiếp tục downstream.",
            category="blocked", count=counts["blocked"], filter_name="blocked", version_id=version_id,
        ))
    if counts["overdue"]:
        at_risk = True
        reasons.append(f"{counts['overdue']} task quá hạn")
        actions.append(_action(
            "version-task-overdue", "P1", f"Xử lý {counts['overdue']} task quá hạn",
            "Rà lại owner và ngày hoàn thành dự kiến cho các task quá hạn trong version.",
            category="overdue", count=counts["overdue"], filter_name="overdue", version_id=version_id,
        ))
    if counts["unassigned"]:
        at_risk = at_risk or counts["unassigned"] >= 3
        actions.append(_action(
            "version-unassigned", "P1" if counts["unassigned"] >= 3 else "P2",
            f"Phân công {counts['unassigned']} task chưa có owner",
            "Pending/Held không bị tính vào nhóm này.",
            category="unassigned", count=counts["unassigned"], filter_name="unassigned", version_id=version_id,
        ))
    if counts["stale"]:
        at_risk = at_risk or counts["stale"] >= 3
        actions.append(_action(
            "version-stale", "P1" if counts["stale"] >= 3 else "P2",
            f"Follow-up {counts['stale']} task stale",
            "Task đang xử lý nhưng thiếu cập nhật tiến độ gần đây.",
            category="stale", count=counts["stale"], filter_name="stale", version_id=version_id,
        ))
    if counts["pending"] and version.get("dueDate") is not None and days_left is not None and 0 <= days_left <= 7:
        at_risk = True
        reasons.append(f"{counts['pending']} task Pending/Held khi version sắp đến hạn")
        actions.append(_action(
            "version-pending", "P1", f"Rà soát {counts['pending']} task Pending/Held",
            "Pending không phải điểm nóng mặc định, nhưng cần xác nhận lại khi milestone đã gần deadline.",
            category="pending", count=counts["pending"], filter_name="pending", version_id=version_id,
        ))

    level = "CRITICAL" if critical else "AT_RISK" if at_risk else "GREEN"
    if version.get("dueDate") is None and level == "GREEN":
        headline = "Backlog/version chưa có deadline; chỉ theo dõi rủi ro ở cấp task, không đánh áp lực milestone."
    else:
        headline = (
            "Version có rủi ro delivery cần xử lý ngay." if level == "CRITICAL" else
            "Version có một số tín hiệu cần PM theo dõi." if level == "AT_RISK" else
            "Version chưa có tín hiệu delivery đáng chú ý từ dữ liệu hiện tại."
        )
    return {"level": level, "headline": headline, "reasons": reasons[:6], "counts": counts}, _sort_actions(actions)[:8]
