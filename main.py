from app.ai.analyst import ProjectAIAnalyst
from app.ai.client_factory import build_ai_client
from app.ai.grounding import ground_ai_analysis
from app.config import AppConfig
from app.domain.project_state import build_project_state
from app.intelligence.hotspots import build_project_hotspots
from app.intelligence.project_summary import build_project_intelligence_summary
from app.intelligence.risk_intelligence import RiskEscalationPolicy, build_risk_intelligence
from app.logging.run_report import RunReportWriter
from app.memory.delta import calculate_project_delta
from app.memory.snapshot import build_project_snapshot
from app.memory.snapshot_store import SnapshotStore
from app.metrics.project_metrics import calculate_project_metrics
from app.reports.daily_report import build_daily_report, build_minimal_daily_report
from app.reports.daily_report_file import DailyReportFileWriter
from app.risk.project_risk import calculate_project_risk_summary
from app.telegram.client import TelegramClient
from app.telegram.publisher import TelegramPublisher
from app.sources import build_collector


def run_daily_report() -> None:
    config = AppConfig()
    print("PM Agent starting...")

    collector, source_base_url = build_collector()
    snapshot_store = SnapshotStore(
        directory=config.snapshot_directory, retention=config.snapshot_retention
    )
    snapshot_history = snapshot_store.load_recent(collector.project_key)
    previous_snapshot = snapshot_history[-1] if snapshot_history else None

    project_state = build_project_state(collector)
    print(f"✓ {collector.source.title()} data collected: {len(project_state.issues)} issues")
    project_state.metrics = calculate_project_metrics(project_state)
    project_risk = calculate_project_risk_summary(project_state)
    intelligence = build_project_intelligence_summary(
        project_state, project_state.metrics, project_risk
    )

    current_snapshot = build_project_snapshot(project_state)
    delta = calculate_project_delta(
        previous_snapshot, current_snapshot, no_progress_days=config.no_progress_days
    )
    hotspots = build_project_hotspots(
        project_state, delta, min_score=config.hotspot_min_score,
        max_items=config.hotspot_max_items,
    )
    risk_intelligence = build_risk_intelligence(
        current_snapshot, snapshot_history,
        policy=RiskEscalationPolicy(
            blocker_escalation_days=config.risk_blocker_escalation_days,
            overdue_escalation_days=config.risk_overdue_escalation_days,
            dependency_escalation_count=config.risk_dependency_escalation_count,
            critical_pressure_score=config.risk_critical_pressure_score,
            action_pressure_score=config.risk_action_pressure_score,
        ),
    )
    print(
        "✓ Analysis completed; "
        f"hotspots: {len(hotspots.items)}; "
        f"escalations: {len(risk_intelligence.escalation_candidates)}"
    )

    ai_analysis = None
    ai_error = None
    ai_client = build_ai_client()
    try:
        ai_analysis = ProjectAIAnalyst(ai_client).analyze(
            project_state, delta, hotspots, risk_intelligence
        )
        ai_analysis = ground_ai_analysis(
            ai_analysis, project_state, intelligence.health
        )
        provider = ai_client.last_provider or "unknown"
        print(f"✓ AI assessment completed via {provider}")
        if ai_client.failures:
            print(f"  ↳ fallback used after {len(ai_client.failures)} provider failure(s)")
    except Exception as exc:
        ai_error = f"{type(exc).__name__}: {exc}"
        print("! All AI providers unavailable; using deterministic fallback")

    detailed_report_path = DailyReportFileWriter(
        directory=config.daily_report_directory,
        retention=config.daily_report_retention,
    ).write(
        project_state=project_state, metrics=project_state.metrics,
        intelligence=intelligence, delta=delta, hotspots=hotspots,
        risk_intelligence=risk_intelligence, ai_analysis=ai_analysis,
        ai_error=ai_error, jira_base_url=source_base_url,
        change_limit=config.detailed_report_change_limit,
        cluster_limit=config.detailed_report_cluster_limit,
    )
    print(f"✓ Detailed daily report saved: {detailed_report_path}")

    # Build a useful PM brief, not a tiny fallback. If it exceeds Telegram's
    # safe limit, compress progressively while protecting assessment, risks,
    # actions, lifecycle and snapshot.
    profiles = [
        (config.daily_report_max_risks, config.daily_report_max_actions, config.daily_report_max_observations, config.daily_report_change_detail_limit),
        (4, 4, 1, 4),
        (3, 3, 1, 3),
    ]
    daily_report = ""
    for max_risks, max_actions, max_observations, change_limit in profiles:
        daily_report = build_daily_report(
            project_state=project_state, metrics=project_state.metrics,
            project_risk=project_risk, intelligence=intelligence, delta=delta,
            jira_base_url=source_base_url, ai_analysis=ai_analysis,
            hotspots=hotspots, risk_intelligence=risk_intelligence,
            report_filename=detailed_report_path.name,
            max_risks=max_risks, max_actions=max_actions,
            max_observations=max_observations, change_detail_limit=change_limit,
            burst_threshold=config.daily_report_burst_threshold,
        )
        if len(daily_report) <= config.telegram_safe_char_limit:
            break
    detailed_report_path.with_suffix(".short.html").write_text(daily_report, encoding="utf-8")
    print(f"✓ Daily report generated: {len(daily_report)} chars")

    # Persist analytical state before external delivery. A Telegram outage must
    # never lose the run's evidence or memory.
    saved_path = snapshot_store.save(current_snapshot)
    print(f"✓ Snapshot saved: {saved_path}")

    delivery_status = "NOT_ATTEMPTED"
    try:
        # Document delivery is intentionally disabled for now because Telegram
        # renders sendDocument as a second message. The .md report is still
        # generated, retained under data/daily_reports, and named in the brief.
        # Re-enable later when file hosting/deep-link UX is implemented.
        attachment = None
        TelegramPublisher(TelegramClient()).publish(daily_report, attachment)
        delivery_status = "SENT"
        print("✓ Telegram message sent")
    except Exception as exc:
        delivery_status = f"FAILED — {type(exc).__name__}: {exc}"
        print("⚠ Telegram delivery failed; analysis, report and snapshot were preserved.")
        print(f"  {type(exc).__name__}: {exc}")

    log_path = RunReportWriter(
        directory=config.run_log_directory, retention=config.run_log_retention
    ).write(
        project_state=project_state, metrics=project_state.metrics,
        intelligence=intelligence, delta=delta, hotspots=hotspots,
        daily_report=daily_report, ai_analysis=ai_analysis, ai_error=ai_error,
        risk_intelligence=risk_intelligence, delivery_status=delivery_status,
        detailed_report_path=str(detailed_report_path),
    )
    print(f"✓ Run log saved: {log_path}")
    print("Done.")


def main() -> None:
    import sys
    if len(sys.argv) > 1 and sys.argv[1].lower() in {"bot", "telegram"}:
        from app.telegram.bot import run_bot
        run_bot()
        return
    run_daily_report()


if __name__ == "__main__":
    main()
