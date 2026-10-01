from app.domain.models import (
    ProjectIssueState,
    ProjectState,
)
from app.sources import ProjectCollector
from app.metrics.issue_metrics import (
    calculate_issue_metrics,
)
from app.risk.assessment import (
    assess_issue_risk,
)
from app.signals.dependency_signals import (
    detect_dependency_signals,
)
from app.signals.hierarchy_signals import (
    detect_hierarchy_signals,
)
from app.signals.issue_signals import (
    detect_issue_signals,
)


def build_project_state(
    collector: ProjectCollector,
    *,
    include_changelog: bool = True,
) -> ProjectState:
    raw_issues = (
        collector.collect_project_issues()
    )

    # ==================================
    # PASS 1
    # Normalize all source issues first.
    # ==================================

    issues = [
        collector.normalize_issue(
            raw_issue
        )
        for raw_issue in raw_issues
    ]

    issues_by_key = {
        issue.key: issue
        for issue in issues
    }

    issue_states: list[
        ProjectIssueState
    ] = []

    # ==================================
    # PASS 2
    #
    # History
    # → Metrics
    # → Signals
    # → Hierarchy
    # → Dependencies
    # → Baseline risk
    # ==================================

    for issue in issues:
        # Full changelog requires one Redmine HTTP request per issue.
        # That is appropriate for deep analysis/report generation, but makes a
        # dashboard overview O(N) network calls (hundreds of requests on large
        # projects).  Overview callers can disable changelog loading and use
        # updated_at as a conservative status-age fallback.
        if include_changelog:
            raw_changelog = collector.collect_issue_changelog(issue.key)
            status_history = collector.normalize_status_history(raw_changelog)
            issue.status_history = status_history
            issue.status_since = collector.get_status_since(issue, status_history)
        else:
            issue.status_history = []
            issue.status_since = issue.updated_at

        # ----------------------------------
        # Metrics
        # ----------------------------------

        metrics = (
            calculate_issue_metrics(
                issue
            )
        )

        # ----------------------------------
        # Generic deterministic signals
        # ----------------------------------

        issue_signals = (
            detect_issue_signals(
                issue,
                metrics,
            )
        )

        # ----------------------------------
        # Parent / child consistency
        # ----------------------------------

        hierarchy_signals = (
            detect_hierarchy_signals(
                issue,
                issues_by_key,
            )
        )

        # ----------------------------------
        # Dependency analysis
        # ----------------------------------

        dependency_signals = (
            detect_dependency_signals(
                issue,
                issues_by_key,
            )
        )

        signals = (
            issue_signals
            + hierarchy_signals
            + dependency_signals
        )

        # ----------------------------------
        # Deterministic baseline risk
        #
        # This is NOT the final AI risk.
        # Keep it only as a fallback/baseline.
        # ----------------------------------

        risk = assess_issue_risk(
            issue,
            signals,
        )

        issue_states.append(
            ProjectIssueState(
                issue=issue,
                metrics=metrics,
                signals=signals,
                risk=risk,
            )
        )

    return ProjectState(
        project_key=(
            collector.project_key
        ),
        issues=issue_states,
    )
