import os
from dataclasses import dataclass


def _float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value else default


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppConfig:
    snapshot_directory: str = os.getenv("SNAPSHOT_DIRECTORY", "data/snapshots")
    snapshot_retention: int = _int_env("SNAPSHOT_RETENTION", 30)

    # Full technical/audit run logs. Keep short by default because these files
    # contain every issue and raw lifecycle details.
    run_log_directory: str = os.getenv("RUN_LOG_DIRECTORY", "data/logs")
    run_log_retention: int = _int_env("RUN_LOG_RETENTION", 14)

    # Human-readable detailed daily reports attached to Telegram.
    daily_report_directory: str = os.getenv(
        "DAILY_REPORT_DIRECTORY", "data/daily_reports"
    )
    daily_report_retention: int = _int_env("DAILY_REPORT_RETENTION", 14)

    telegram_safe_char_limit: int = _int_env("TELEGRAM_SAFE_CHAR_LIMIT", 3800)

    report_language: str = os.getenv("REPORT_LANGUAGE", "vi").strip().lower()
    report_timezone: str = os.getenv("REPORT_TIMEZONE", "Asia/Ho_Chi_Minh").strip()

    ai_context_max_chars: int = _int_env("AI_CONTEXT_MAX_CHARS", 16000)
    ai_context_max_issues: int = _int_env("AI_CONTEXT_MAX_ISSUES", 24)
    ai_context_board_max_issues: int = _int_env("AI_CONTEXT_BOARD_MAX_ISSUES", 100)
    ai_context_max_hotspots: int = _int_env("AI_CONTEXT_MAX_HOTSPOTS", 10)
    ai_context_max_clusters: int = _int_env("AI_CONTEXT_MAX_CLUSTERS", 6)
    ai_context_max_deltas: int = _int_env("AI_CONTEXT_MAX_DELTAS", 12)
    ai_context_max_escalations: int = _int_env("AI_CONTEXT_MAX_ESCALATIONS", 8)
    telegram_attach_daily_report: bool = _bool_env(
        "TELEGRAM_ATTACH_DAILY_REPORT", False
    )

    no_progress_days: float = _float_env("NO_PROGRESS_DAYS", 3.0)
    hotspot_min_score: int = _int_env("HOTSPOT_MIN_SCORE", 3)
    hotspot_max_items: int = _int_env("HOTSPOT_MAX_ITEMS", 8)

    daily_report_max_risks: int = _int_env("DAILY_REPORT_MAX_RISKS", 5)
    daily_report_max_actions: int = _int_env("DAILY_REPORT_MAX_ACTIONS", 4)
    daily_report_max_observations: int = _int_env("DAILY_REPORT_MAX_OBSERVATIONS", 2)
    daily_report_change_detail_limit: int = _int_env(
        "DAILY_REPORT_CHANGE_DETAIL_LIMIT", 5
    )
    daily_report_burst_threshold: int = _int_env(
        "DAILY_REPORT_BURST_THRESHOLD", 20
    )
    detailed_report_change_limit: int = _int_env(
        "DETAILED_REPORT_CHANGE_LIMIT", 12
    )
    detailed_report_cluster_limit: int = _int_env(
        "DETAILED_REPORT_CLUSTER_LIMIT", 6
    )

    risk_blocker_escalation_days: float = _float_env(
        "RISK_BLOCKER_ESCALATION_DAYS", 1.0
    )
    risk_overdue_escalation_days: int = _int_env(
        "RISK_OVERDUE_ESCALATION_DAYS", 3
    )
    risk_dependency_escalation_count: int = _int_env(
        "RISK_DEPENDENCY_ESCALATION_COUNT", 3
    )
    risk_critical_pressure_score: int = _int_env(
        "RISK_CRITICAL_PRESSURE_SCORE", 8
    )
    risk_action_pressure_score: int = _int_env(
        "RISK_ACTION_PRESSURE_SCORE", 4
    )
