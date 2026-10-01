from app.domain.models import (
    IssueMetrics,
    IssueSignal,
    ProjectIssue,
)


ACTIVE_STATUSES = {
    "In Progress",
    "Doing",
    "In Review",
}

DONE_STATUSES = {
    "Done",
    "Closed",
    "Resolved",
}


def detect_issue_signals(
    issue: ProjectIssue,
    metrics: IssueMetrics,
) -> list[IssueSignal]:
    signals: list[IssueSignal] = []

    is_active = issue.status in ACTIVE_STATUSES
    is_done = issue.status in DONE_STATUSES

    # Active issue nằm quá lâu ở cùng status
    if (
        is_active
        and metrics.days_in_status is not None
        and metrics.days_in_status >= 3
    ):
        signals.append(
            IssueSignal(
                code="STUCK",
                severity="warning",
                message=(
                    f"{issue.key} has been in "
                    f"{issue.status} for "
                    f"{metrics.days_in_status} days"
                ),
            )
        )

    # Chỉ active work mới coi là stale
    if (
        is_active
        and metrics.days_since_update is not None
        and metrics.days_since_update >= 2
    ):
        signals.append(
            IssueSignal(
                code="STALE",
                severity="warning",
                message=(
                    f"{issue.key} has not been updated "
                    f"for {metrics.days_since_update} days"
                ),
            )
        )

    if (
        not is_done
        and metrics.days_to_due is not None
        and metrics.days_to_due < 0
    ):
        signals.append(
            IssueSignal(
                code="OVERDUE",
                severity="critical",
                message=(
                    f"{issue.key} is overdue by "
                    f"{abs(metrics.days_to_due)} days"
                ),
            )
        )

    if (
        not is_done
        and metrics.days_to_due is not None
        and 0 <= metrics.days_to_due <= 2
    ):
        signals.append(
            IssueSignal(
                code="NEAR_DUE",
                severity="warning",
                message=(
                    f"{issue.key} is due in "
                    f"{metrics.days_to_due} days"
                ),
            )
        )

    return signals