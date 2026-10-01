from datetime import datetime
from zoneinfo import ZoneInfo
import os

from app.i18n import health_label, is_vi


def _now():
    tz = os.getenv("REPORT_TIMEZONE", "Asia/Ho_Chi_Minh")
    try:
        return datetime.now(ZoneInfo(tz))
    except Exception:
        return datetime.now()


def build_header_section(project_state, report_filename: str | None = None) -> list[str]:
    today = _now().strftime("%d %b %Y")
    title = "Cập nhật dự án hằng ngày" if is_vi() else "Daily Project Update"
    project_label = "Dự án" if is_vi() else "Project"
    report_label = "File báo cáo" if is_vi() else "Report file"
    lines = [f"🤖 <b>{title}</b>", today, f"{project_label}: <b>{project_state.project_key}</b>"]
    if report_filename:
        lines.append(f"📎 {report_label}: <b>{report_filename}</b>")
    lines.append("")
    return lines


def build_health_section(metrics, intelligence) -> list[str]:
    health = intelligence.health
    icon = {"HEALTHY":"🟢","WATCH":"🟡","AT_RISK":"🟠","CRITICAL":"🔴"}.get(health,"⚪️")
    label = health_label(health)
    prefix = "Sức khỏe dự án" if is_vi() else "Health"
    lines=[f"{icon} <b>{prefix}: {label}</b>"]
    if intelligence.headline:
        lines.append(intelligence.headline)
    lines.append("")
    return lines


def build_progress_section(metrics) -> list[str]:
    total=metrics.total_issues; done=metrics.done_issues
    completion=round(done/total*100) if total else 0
    if is_vi():
        return [
            "📊 <b>Tổng quan dự án</b>",
            f"• {total} issue · {metrics.active_issues} đang hoạt động · {done} hoàn thành · {completion}% hoàn tất",
            f"• {metrics.overdue_issues} quá hạn · {metrics.blocked_issues} bị chặn · {metrics.blocking_issues} blocker đang hoạt động",
            "",
        ]
    return [
        "📊 <b>Project Snapshot</b>",
        f"• {total} issues · {metrics.active_issues} active · {done} done · {completion}% complete",
        f"• {metrics.overdue_issues} overdue · {metrics.blocked_issues} blocked · {metrics.blocking_issues} active blockers",
        "",
    ]
