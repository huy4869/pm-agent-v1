from app.domain.models import (
    ProjectIntelligenceSummary,
    ProjectMetrics,
    ProjectRiskSummary,
    ProjectState,
)


DONE_STATUSES = {
    "Done",
    "Closed",
    "Resolved",
}


def build_project_intelligence_summary(
    project_state: ProjectState,
    project_metrics: ProjectMetrics,
    project_risk: ProjectRiskSummary,
) -> ProjectIntelligenceSummary:

    # ==================================
    # BASELINE PROJECT HEALTH
    #
    # Đây vẫn chỉ là deterministic
    # baseline.
    # ==================================

    if (
        project_risk.critical_issues
        > 0
    ):
        health = "CRITICAL"

    elif (
        project_risk.high_issues
        > 0
    ):
        health = "AT_RISK"

    elif (
        project_risk.medium_issues > 0
        or project_metrics.blocked_issues > 0
        or project_metrics.hierarchy_mismatches > 0
        or project_metrics.dependencies_to_verify > 0
    ):
        health = "WATCH"

    else:
        health = "HEALTHY"

    # ==================================
    # OBSERVATIONS
    # ==================================

    observations: list[str] = []

    if project_metrics.overdue_issues:
        observations.append(
            f"{project_metrics.overdue_issues} "
            "issue(s) overdue"
        )

    if project_metrics.near_due_issues:
        observations.append(
            f"{project_metrics.near_due_issues} "
            "issue(s) near due"
        )

    if project_metrics.stale_issues:
        observations.append(
            f"{project_metrics.stale_issues} "
            "active issue(s) stale"
        )

    if project_metrics.stuck_issues:
        observations.append(
            f"{project_metrics.stuck_issues} "
            "issue(s) stuck"
        )

    if project_metrics.blocked_issues:
        observations.append(
            f"{project_metrics.blocked_issues} "
            "confirmed blocked issue(s)"
        )

    if project_metrics.blocking_issues:
        observations.append(
            f"{project_metrics.blocking_issues} "
            "issue(s) blocking downstream work"
        )

    if (
        project_metrics.hierarchy_mismatches
    ):
        observations.append(
            f"{project_metrics.hierarchy_mismatches} "
            "parent/child status mismatch(es)"
        )

    if (
        project_metrics.dependencies_to_verify
    ):
        observations.append(
            f"{project_metrics.dependencies_to_verify} "
            "dependency signal(s) need verification"
        )

    if project_metrics.unassigned_issues:
        observations.append(
            f"{project_metrics.unassigned_issues} "
            "open issue(s) unassigned"
        )

    # ==================================
    # TOP CONCERNS
    # ==================================

    top_concerns: list[str] = []

    for state in project_state.issues:
        issue = state.issue

        signal_codes = {
            signal.code
            for signal in state.signals
        }

        if (
            "PARENT_DONE_CHILD_OPEN"
            in signal_codes
        ):
            top_concerns.append(
                (
                    f"{issue.key} — "
                    f"{issue.status}, but parent "
                    f"{issue.parent_key} is Done"
                )
            )

        stale_targets = []

        for dependency in (
            issue.dependencies or []
        ):
            if (
                dependency.relation.lower()
                == "blocks"
                and
                "STALE_DEPENDENCY_CANDIDATE"
                in signal_codes
            ):
                stale_targets.append(
                    dependency.related_issue_key
                )

        if stale_targets:
            top_concerns.append(
                (
                    f"{issue.key} — "
                    "blocking links need verification: "
                    + ", ".join(
                        stale_targets
                    )
                )
            )

    top_risk_keys = set(
        project_risk.top_risk_issue_keys
    )

    for state in project_state.issues:
        if (
            state.issue.key
            not in top_risk_keys
        ):
            continue

        reasons = ", ".join(
            state.risk.reasons
        )

        concern = (
            f"{state.issue.key} — "
            f"{state.risk.level} risk"
        )

        if reasons:
            concern += (
                f": {reasons}"
            )

        top_concerns.append(
            concern
        )

    top_concerns = list(
        dict.fromkeys(
            top_concerns
        )
    )

    # ==================================
    # HEADLINE
    # ==================================

    parts = [
        (
            f"Project "
            f"{project_state.project_key} "
            f"is {health}."
        )
    ]

    if (
        project_metrics
        .hierarchy_mismatches
    ):
        parts.append(
            (
                f"{project_metrics.hierarchy_mismatches} "
                "hierarchy mismatch(es)."
            )
        )

    if (
        project_metrics
        .dependencies_to_verify
    ):
        parts.append(
            (
                f"{project_metrics.dependencies_to_verify} "
                "dependency signal(s) "
                "need verification."
            )
        )

    if project_metrics.blocked_issues:
        parts.append(
            (
                f"{project_metrics.blocked_issues} "
                "confirmed blocked."
            )
        )

    return ProjectIntelligenceSummary(
        health=health,
        headline=" ".join(
            parts
        ),
        top_concerns=(
            top_concerns
        ),
        observations=(
            observations
        ),
    )