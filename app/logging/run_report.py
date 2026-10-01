from datetime import datetime, timezone
from pathlib import Path

from app.ai.models import RiskEvidence


class RunReportWriter:
    def __init__(self, directory: str = "data/logs", retention: int = 14) -> None:
        self.directory = Path(directory)
        self.retention = retention

    def write(
        self,
        *,
        project_state,
        metrics,
        intelligence,
        delta,
        hotspots,
        daily_report: str,
        ai_analysis=None,
        ai_error: str | None = None,
        risk_intelligence=None,
        delivery_status: str | None = None,
        detailed_report_path: str | None = None,
    ) -> Path:
        project_dir = self.directory / project_state.project_key
        project_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        path = project_dir / f"{now.strftime('%Y-%m-%d_%H%M%S%fZ')}.md"

        lines: list[str] = [
            "# PM Agent Run",
            "",
            f"- Project: `{project_state.project_key}`",
            f"- Captured at: `{now.isoformat()}`",
            f"- Deterministic health: `{intelligence.health}`",
            "",
            "## AI Analysis",
            "",
        ]

        if ai_analysis is not None:
            lines.extend(_build_ai_section(ai_analysis))
        else:
            lines.extend(
                [
                    "**Status:** unavailable",
                    "",
                    f"Error: `{ai_error or 'unknown error'}`",
                ]
            )

        lines.extend(["", "## Project Issues", ""])
        for state in project_state.issues:
            issue = state.issue
            m = state.metrics
            signal_codes = sorted({s.code for s in state.signals if s.code})
            lines.extend(
                [
                    f"### {issue.key} — {issue.summary}",
                    "",
                    f"- Status: {issue.status}",
                    f"- Assignee: {issue.assignee or 'Unassigned'}",
                    f"- Priority: {issue.priority or 'None'}",
                    f"- Days in status: {m.days_in_status}",
                    f"- Days since update: {m.days_since_update}",
                    f"- Days to due: {m.days_to_due}",
                    f"- Deterministic delivery risk: {state.risk.level if state.risk else 'NONE'}",
                    f"- Signals: {', '.join(signal_codes) or 'None'}",
                ]
            )
            if issue.parent_key:
                lines.append(f"- Parent: {issue.parent_key}")
            if issue.dependencies:
                lines.append("- Dependencies:")
                for dep in issue.dependencies:
                    lines.append(
                        f"  - {dep.relation} {dep.related_issue_key} ({dep.direction})"
                    )
            lines.append("")

        lines.extend(
            [
                "## Project Metrics",
                "",
                f"- Total: {metrics.total_issues}",
                f"- Active: {metrics.active_issues}",
                f"- Done: {metrics.done_issues}",
                f"- Overdue: {metrics.overdue_issues}",
                f"- Near due: {metrics.near_due_issues}",
                f"- Stale: {metrics.stale_issues}",
                f"- Stuck: {metrics.stuck_issues}",
                f"- Unassigned: {metrics.unassigned_issues}",
                f"- Blocked: {metrics.blocked_issues}",
                f"- Blocking others: {metrics.blocking_issues}",
                f"- Hierarchy mismatches: {metrics.hierarchy_mismatches}",
                f"- Dependencies to verify: {metrics.dependencies_to_verify}",
                "",
                "## Hotspots",
                "",
            ]
        )

        if hotspots.items:
            for h in hotspots.items:
                lines.append(
                    f"- **{h.issue_key} — {h.level}** "
                    f"(risk-pressure score {h.score})"
                )
                for reason in h.reasons:
                    lines.append(f"  - {reason}")
                if h.delta_codes:
                    lines.append(f"  - Delta: {', '.join(h.delta_codes)}")
        else:
            lines.append("- None")

        lines.extend(["", "## Delta (raw audit)", ""])
        if delta.baseline_created:
            lines.append("- Baseline created")
        elif delta.events:
            for event in delta.events:
                lines.append(f"- `{event.code}` — {event.message}")
                for key, value in (event.metadata or {}).items():
                    lines.append(f"  - `{key}`: `{value}`")
        else:
            lines.append("- No changes")

        lines.extend(["", "## Risk Intelligence", ""])
        lines.extend(_build_risk_intelligence_section(risk_intelligence))

        lines.extend(["", "## Delivery", ""])
        lines.append(f"- Telegram: {delivery_status or 'UNKNOWN'}")
        if detailed_report_path:
            lines.append(f"- Detailed daily report: `{detailed_report_path}`")

        # Embed the exact human-readable daily report that is attached to
        # Telegram. This keeps the full run log self-contained: one technical
        # audit file can be opened later without depending on the retained
        # attachment file still being present.
        detailed_report_content = _read_text_file(detailed_report_path)
        lines.extend(["", "## Detailed Daily Report (embedded)", ""])
        if detailed_report_content:
            lines.extend([detailed_report_content.rstrip(), ""])
        elif detailed_report_path:
            lines.extend([
                f"_Detailed report could not be read from `{detailed_report_path}`._",
                "",
            ])
        else:
            lines.extend(["_No detailed daily report was generated._", ""])

        # Keep Telegram HTML completely untouched inside a code fence.
        lines.extend(["", "## Telegram Daily Message", "", "```html", daily_report, "```", ""])

        path.write_text("\n".join(lines), encoding="utf-8")
        self._cleanup(project_dir)
        return path

    def _cleanup(self, project_dir: Path) -> None:
        files = sorted(project_dir.glob("*.md"))
        excess = max(0, len(files) - self.retention)
        for path in files[:excess]:
            path.unlink(missing_ok=True)


def _read_text_file(path_value: str | None) -> str | None:
    if not path_value:
        return None

    try:
        path = Path(path_value)
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        # Run logging must never fail merely because the companion report
        # cannot be read. The path is still recorded in the Delivery section.
        return None


def _build_ai_section(ai_analysis) -> list[str]:
    lines = [
        f"**Health:** {ai_analysis.health}",
        "",
        ai_analysis.summary or "_No summary._",
        "",
        "### Risks",
        "",
    ]
    if not ai_analysis.risks:
        lines.append("- None")

    for risk in ai_analysis.risks:
        lines.append(
            f"- **{risk.issue_key} — {risk.level}** (confidence: {risk.confidence})"
        )
        if risk.impact:
            lines.append(f"  - Impact: {risk.impact}")
        if risk.evidence:
            lines.append("  - Evidence:")
            for evidence in risk.evidence:
                rendered = _render_evidence(evidence)
                if rendered:
                    lines.append(f"    - {rendered}")
        if risk.recommended_action:
            lines.append(f"  - Recommended action: {risk.recommended_action}")

    lines.extend(["", "### PM Actions", ""])
    if ai_analysis.pm_actions:
        lines.extend(
            f"{index}. {action}"
            for index, action in enumerate(ai_analysis.pm_actions, start=1)
        )
    else:
        lines.append("- None")

    lines.extend(["", "### Observations", ""])
    if ai_analysis.observations:
        lines.extend(f"- {item}" for item in ai_analysis.observations)
    else:
        lines.append("- None")
    return lines


def _build_risk_intelligence_section(risk_intelligence) -> list[str]:
    if risk_intelligence is None:
        return ["- Not available"]

    if risk_intelligence.previous_project_score is None:
        lines = [
            f"- Risk-pressure baseline: {risk_intelligence.project_score}",
            "- Project trend: BASELINE",
        ]
    else:
        lines = [
            "- Risk pressure: "
            f"{risk_intelligence.previous_project_score} → {risk_intelligence.project_score} "
            f"({risk_intelligence.project_trend})",
        ]

    lines.extend(["", "### Lifecycle changes", ""])
    changed = False
    for title, items in (
        ("NEW", risk_intelligence.new_risks),
        ("ESCALATING", risk_intelligence.escalations),
        ("IMPROVING", risk_intelligence.improvements),
        ("RESOLVED", risk_intelligence.resolved),
    ):
        for item in items:
            changed = True
            lines.append(
                f"- {item.issue_key}: {title}; "
                f"pressure={item.previous_score}→{item.current_score}; "
                f"delivery_risk={item.delivery_risk_level}"
            )
    if not changed:
        lines.append("- No lifecycle changes")

    lines.extend(["", "### Escalation policy", ""])
    if risk_intelligence.escalation_candidates:
        for item in risk_intelligence.escalation_candidates:
            lines.append(
                f"- {item.issue_key}: ESCALATE — "
                + "; ".join(item.escalation_reasons)
            )
    else:
        lines.append("- No escalation candidates")

    lines.extend(["", "### Current risk lifecycle", ""])
    active_items = [item for item in risk_intelligence.items if item.current_score > 0]
    if active_items:
        for item in sorted(
            active_items,
            key=lambda x: (-x.current_score, x.issue_key),
        ):
            lines.append(
                f"- {item.issue_key}: state={item.lifecycle_state}; "
                f"escalation={item.escalation_level}; "
                f"pressure={item.current_score}; "
                f"risk_age={item.risk_age_days}; "
                f"status_age={item.status_age_days}; "
                f"blocker_observed_age={item.blocker_observed_age_days}; "
                f"overdue_age={item.overdue_age_days}; "
                f"direct={item.direct_downstream}; "
                f"propagated={item.propagated_downstream}"
            )
    else:
        lines.append("- None")

    return lines

def _render_evidence(evidence: RiskEvidence) -> str | None:
    kind = evidence.type.upper()
    key = evidence.issue_key
    value = evidence.value
    related = evidence.related_issue_keys

    if kind == "STATUS" and key and value:
        return f"{key} status: **{value}**"
    if kind == "ASSIGNEE" and key:
        if not value or str(value).strip().lower() in {"unassigned", "none", "null"}:
            return f"{key} is unassigned"
        return f"{key} assigned to **{value}**"
    if kind == "OVERDUE" and key:
        if not value:
            return f"{key} is overdue"
        normalized = value.strip()
        if normalized.lower().endswith(" overdue"):
            return f"{key} is **{normalized}**"
        return f"{key} overdue by **{normalized}**"
    if kind == "NEAR_DUE" and key:
        return f"{key} due in **{value}**" if value else f"{key} is near due"
    if kind == "BLOCKS" and key and related:
        return f"{key} blocks {', '.join(related)}"
    if kind == "BLOCKED_BY" and key and related:
        return f"{key} is blocked by {', '.join(related)}"
    if kind == "PERSISTENT_BLOCKER" and key:
        return f"{key} remains a blocker across snapshots"
    if kind == "STALE" and key:
        return f"{key} stale for **{value}**" if value else f"{key} is stale"
    if kind == "STUCK" and key:
        return f"{key} stuck for **{value}**" if value else f"{key} is stuck"
    if kind == "PARENT_STATUS" and key and related and value:
        return f"{key} parent {related[0]} status: **{value}**"
    if kind == "DEPENDENCY_VERIFICATION" and key:
        suffix = f": {', '.join(related)}" if related else ""
        return f"{key} dependency requires verification{suffix}"
    # PRIORITY is intentionally not surfaced as delivery-risk evidence.
    return None
