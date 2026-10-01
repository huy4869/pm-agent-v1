from html import escape

from app.domain.models import (
    ProjectMetrics,
    ProjectState,
)

from app.reports.helpers import (
    blocking_targets,
    issue_ref,
    signal_codes,
)


def build_delivery_section(
    project_state: ProjectState,
    metrics: ProjectMetrics,
) -> list[str]:
    lines: list[str] = []

    # ========================================================
    # ONLY SHOW SECTIONS THAT NEED PM ATTENTION
    # ========================================================

    lines.extend(
        _build_inconsistency_section(
            project_state
        )
    )

    lines.extend(
        _build_signal_summary(
            metrics
        )
    )

    lines.extend(
        _build_dependencies_to_verify(
            project_state
        )
    )

    lines.extend(
        _build_confirmed_blockers(
            project_state
        )
    )

    lines.extend(
        _build_top_concerns(
            project_state
        )
    )

    return lines


# ============================================================
# WORKFLOW INCONSISTENCIES
# ============================================================

def _build_inconsistency_section(
    project_state: ProjectState,
) -> list[str]:
    items: list[str] = []

    for state in project_state.issues:
        issue = state.issue
        codes = signal_codes(
            state
        )

        if (
            "PARENT_DONE_CHILD_OPEN"
            not in codes
            or not issue.parent_key
        ):
            continue

        items.append(
            f"• {issue_ref(issue.key)} is "
            f"<b>{escape(issue.status)}</b>, "
            f"while parent "
            f"{issue_ref(issue.parent_key)} "
            "is <b>Done</b>"
        )

        items.append(
            "  Evidence: child status = "
            f"{escape(issue.status)}; "
            "parent status = Done"
        )

    # Nothing to report -> hide section
    if not items:
        return []

    return [
        "⚠️ <b>Workflow Inconsistencies</b>",
        *items,
        "",
    ]


# ============================================================
# DELIVERY SIGNALS
# ============================================================

def _build_signal_summary(
    metrics: ProjectMetrics,
) -> list[str]:
    signals: list[str] = []

    if metrics.overdue_issues:
        signals.append(
            _count_phrase(
                metrics.overdue_issues,
                "overdue issue",
            )
        )

    if metrics.near_due_issues:
        signals.append(
            _count_phrase(
                metrics.near_due_issues,
                "issue near due",
                "issues near due",
            )
        )

    if metrics.stale_issues:
        signals.append(
            _count_phrase(
                metrics.stale_issues,
                "stale active issue",
            )
        )

    if metrics.stuck_issues:
        signals.append(
            _count_phrase(
                metrics.stuck_issues,
                "stuck issue",
            )
        )

    if metrics.blocked_issues:
        signals.append(
            _count_phrase(
                metrics.blocked_issues,
                "confirmed blocked issue",
            )
        )

    if metrics.blocking_issues:
        signals.append(
            _count_phrase(
                metrics.blocking_issues,
                "active blocker",
            )
        )

    if metrics.dependencies_to_verify:
        signals.append(
            _count_phrase(
                metrics.dependencies_to_verify,
                (
                    "dependency signal "
                    "needing verification"
                ),
                (
                    "dependency signals "
                    "needing verification"
                ),
            )
        )

    if metrics.unassigned_issues:
        signals.append(
            _count_phrase(
                metrics.unassigned_issues,
                "open issue unassigned",
                "open issues unassigned",
            )
        )

    # No delivery signals -> hide entire section
    if not signals:
        return []

    lines = [
        "⚠️ <b>Delivery Signals</b>"
    ]

    for signal in signals:
        lines.append(
            f"• {escape(signal)}"
        )

    lines.append("")

    return lines


# ============================================================
# DEPENDENCIES TO VERIFY
# ============================================================

def _build_dependencies_to_verify(
    project_state: ProjectState,
) -> list[str]:
    items: list[str] = []

    for state in project_state.issues:
        issue = state.issue
        codes = signal_codes(
            state
        )

        if (
            "STALE_DEPENDENCY_CANDIDATE"
            not in codes
        ):
            continue

        targets = blocking_targets(
            issue
        )

        if not targets:
            continue

        target_refs = ", ".join(
            issue_ref(key)
            for key in targets
        )

        items.append(
            f"• {issue_ref(issue.key)} "
            "still has blocking links to "
            f"{target_refs}"
        )

        if issue.parent_key:
            items.append(
                "  Evidence: parent "
                f"{issue_ref(issue.parent_key)} "
                "is already Done"
            )

        items.append(
            "  → Verify issue status and "
            "dependency links before treating "
            "this as an active blocker."
        )

    # Nothing needs verification -> hide section
    if not items:
        return []

    return [
        "🔗 <b>Dependencies to verify</b>",
        *items,
        "",
    ]


# ============================================================
# CONFIRMED BLOCKERS
# ============================================================

def _build_confirmed_blockers(
    project_state: ProjectState,
) -> list[str]:
    items: list[str] = []

    for state in project_state.issues:
        issue = state.issue
        codes = signal_codes(
            state
        )

        if (
            "BLOCKING_OTHERS"
            not in codes
        ):
            continue

        targets = blocking_targets(
            issue
        )

        if not targets:
            continue

        target_refs = ", ".join(
            issue_ref(key)
            for key in targets
        )

        items.append(
            f"• {issue_ref(issue.key)} "
            f"blocks {target_refs}"
        )

        items.append(
            "  Evidence: Jira linked work items"
        )

    # No blocker -> don't waste report space
    if not items:
        return []

    return [
        "⛔️ <b>Confirmed Blockers</b>",
        *items,
        "",
    ]


# ============================================================
# TOP CONCERNS
#
# Used as deterministic fallback when AI is unavailable.
# daily_report.py removes this section when Gemini succeeds.
# ============================================================

def _build_top_concerns(
    project_state: ProjectState,
) -> list[str]:
    concerns: list[str] = []

    for state in project_state.issues:
        issue = state.issue
        codes = signal_codes(
            state
        )

        # ----------------------------------------------------
        # OVERDUE
        # ----------------------------------------------------

        if "OVERDUE" in codes:
            concerns.append(
                f"• {issue_ref(issue.key)} — "
                "<b>overdue</b>"
            )

        # ----------------------------------------------------
        # CONFIRMED BLOCKER
        # ----------------------------------------------------

        if "BLOCKING_OTHERS" in codes:
            targets = blocking_targets(
                issue
            )

            if targets:
                target_refs = ", ".join(
                    issue_ref(key)
                    for key in targets
                )

                concerns.append(
                    f"• {issue_ref(issue.key)} — "
                    f"blocking {target_refs}"
                )

        # ----------------------------------------------------
        # PARENT DONE / CHILD OPEN
        # ----------------------------------------------------

        if (
            "PARENT_DONE_CHILD_OPEN"
            in codes
            and issue.parent_key
        ):
            concerns.append(
                f"• {issue_ref(issue.key)} — "
                f"{escape(issue.status)}, "
                "while parent "
                f"{issue_ref(issue.parent_key)} "
                "is Done"
            )

        # ----------------------------------------------------
        # STALE DEPENDENCY
        # ----------------------------------------------------

        if (
            "STALE_DEPENDENCY_CANDIDATE"
            in codes
        ):
            targets = blocking_targets(
                issue
            )

            if targets:
                target_refs = ", ".join(
                    issue_ref(key)
                    for key in targets
                )

                concerns.append(
                    f"• {issue_ref(issue.key)} — "
                    "blocking links need "
                    f"verification: {target_refs}"
                )

    # Remove duplicates, preserve order
    concerns = list(
        dict.fromkeys(
            concerns
        )
    )

    if not concerns:
        return []

    return [
        "🔎 <b>Top Concerns</b>",
        *concerns[:5],
        "",
    ]


# ============================================================
# HELPERS
# ============================================================

def _count_phrase(
    count: int,
    singular: str,
    plural: str | None = None,
) -> str:
    if count == 1:
        return (
            f"1 {singular}"
        )

    if plural:
        return (
            f"{count} {plural}"
        )

    return (
        f"{count} {singular}s"
    )