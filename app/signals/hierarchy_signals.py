from app.domain.models import (
    IssueSignal,
    ProjectIssue,
)


DONE_STATUSES = {
    "Done",
    "Closed",
    "Resolved",
}


def detect_hierarchy_signals(
    issue: ProjectIssue,
    issues_by_key: dict[str, ProjectIssue],
) -> list[IssueSignal]:
    signals: list[IssueSignal] = []

    if not issue.parent_key:
        return signals

    parent = issues_by_key.get(
        issue.parent_key
    )

    if not parent:
        return signals

    parent_done = (
        parent.status in DONE_STATUSES
    )

    child_done = (
        issue.status in DONE_STATUSES
    )

    if (
        parent_done
        and not child_done
    ):
        signals.append(
            IssueSignal(
                code="PARENT_DONE_CHILD_OPEN",
                severity="warning",
                message=(
                    f"{issue.key} is "
                    f"{issue.status}, but parent "
                    f"{parent.key} is "
                    f"{parent.status}"
                ),
            )
        )

    return signals


def has_parent_done_child_open(
    issue: ProjectIssue,
    issues_by_key: dict[str, ProjectIssue],
) -> bool:
    if not issue.parent_key:
        return False

    parent = issues_by_key.get(
        issue.parent_key
    )

    if not parent:
        return False

    return (
        parent.status in DONE_STATUSES
        and issue.status
        not in DONE_STATUSES
    )