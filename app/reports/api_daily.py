"""Generate daily archives from API snapshots, with optional AI analysis and no Telegram delivery."""
from copy import copy
from pathlib import Path
from threading import RLock
import re

from app.config import AppConfig
from app.intelligence.hotspots import build_project_hotspots
from app.intelligence.project_summary import build_project_intelligence_summary
from app.intelligence.risk_intelligence import RiskEscalationPolicy, build_risk_intelligence
from app.memory.delta import calculate_project_delta
from app.memory.snapshot import build_project_snapshot
from app.memory.snapshot_store import SnapshotStore
from app.reports.daily_report import build_daily_report
from app.reports.daily_report_file import DailyReportFileWriter
from app.risk.project_risk import calculate_project_risk_summary

_LOCK = RLock()


def _directory(value: str) -> str:
    path = Path(value)
    return str(path if path.is_absolute() else Path(__file__).resolve().parents[2] / path)


def archive_api_snapshot(snapshot: dict, *, include_ai: bool = False) -> str:
    """Persist once per fetched snapshot; delta always uses the prior history."""
    with _LOCK:
        if snapshot.get("dailyReportFilename"):
            return snapshot["dailyReportFilename"]
        config = AppConfig()
        state = copy(snapshot["state"])
        state.project_key = str(snapshot["project"].get("identifier") or state.project_key)
        if not re.fullmatch(r"[A-Za-z0-9_-]+", state.project_key):
            raise ValueError("Invalid project identifier")
        store = SnapshotStore(_directory(config.snapshot_directory), config.snapshot_retention)
        history = store.load_recent(state.project_key)
        current = build_project_snapshot(state)
        delta = calculate_project_delta(history[-1] if history else None, current, no_progress_days=config.no_progress_days)
        risk = calculate_project_risk_summary(state)
        intelligence = build_project_intelligence_summary(state, state.metrics, risk)
        hotspots = build_project_hotspots(state, delta, min_score=config.hotspot_min_score, max_items=config.hotspot_max_items)
        lifecycle = build_risk_intelligence(current, history, policy=RiskEscalationPolicy(
            blocker_escalation_days=config.risk_blocker_escalation_days,
            overdue_escalation_days=config.risk_overdue_escalation_days,
            dependency_escalation_count=config.risk_dependency_escalation_count,
            critical_pressure_score=config.risk_critical_pressure_score,
            action_pressure_score=config.risk_action_pressure_score,
        ))
        ai_analysis = None
        ai_error = None
        if include_ai:
            from app.ai.analyst import ProjectAIAnalyst
            from app.ai.client_factory import build_ai_client
            from app.ai.grounding import ground_ai_analysis
            try:
                ai_analysis = ProjectAIAnalyst(build_ai_client()).analyze(state, delta, hotspots, lifecycle)
                ai_analysis = ground_ai_analysis(ai_analysis, state, intelligence.health)
            except Exception as exc:
                ai_error = type(exc).__name__
        base = snapshot["client"].base_url
        detailed = DailyReportFileWriter(_directory(config.daily_report_directory), config.daily_report_retention).write(
            project_state=state, metrics=state.metrics, intelligence=intelligence,
            delta=delta, hotspots=hotspots, risk_intelligence=lifecycle,
            ai_analysis=ai_analysis, ai_error=ai_error, jira_base_url=base, change_limit=config.detailed_report_change_limit,
            cluster_limit=config.detailed_report_cluster_limit,
        )
        brief = build_daily_report(state, state.metrics, risk, intelligence, delta, base,
            ai_analysis=ai_analysis, hotspots=hotspots, risk_intelligence=lifecycle, report_filename=detailed.name,
            max_risks=config.daily_report_max_risks, max_actions=config.daily_report_max_actions,
            max_observations=config.daily_report_max_observations,
            change_detail_limit=config.daily_report_change_detail_limit,
            burst_threshold=config.daily_report_burst_threshold,
        )
        detailed.with_suffix(".short.html").write_text(brief, encoding="utf-8")
        store.save(current)
        snapshot["dailyReportFilename"] = detailed.name
        snapshot["dailyReportAiStatus"] = "completed" if ai_analysis is not None else "unavailable" if include_ai else "not_requested"
        return detailed.name
