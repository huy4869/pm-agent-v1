from app.domain.models import (
    IssueSignal,
    ProjectIssue,
)
from app.signals.hierarchy_signals import (
    has_parent_done_child_open,
)


DONE_STATUSES = {
    "Done",
    "Closed",
    "Resolved",
}


def detect_dependency_signals(
    issue: ProjectIssue,
    issues_by_key: dict[str, ProjectIssue],
) -> list[IssueSignal]:
    signals: list[IssueSignal] = []

    if not issue.dependencies:
        return signals

    issue_has_hierarchy_mismatch = (
        has_parent_done_child_open(
            issue,
            issues_by_key,
        )
    )

    for dependency in issue.dependencies:
        related_issue = issues_by_key.get(
            dependency.related_issue_key
        )

        if not related_issue:
            continue

        relation = (
            dependency.relation.lower()
        )

        related_has_hierarchy_mismatch = (
            has_parent_done_child_open(
                related_issue,
                issues_by_key,
            )
        )

        # ----------------------------------
        # CURRENT ISSUE IS BLOCKED BY ANOTHER
        # ----------------------------------

        if "blocked by" in relation:
            if (
                related_issue.status
                in DONE_STATUSES
            ):
                continue

            # Example:
            #
            # ISSUE-9 is blocked by ISSUE-5
            #
            # but ISSUE-5 parent ISSUE-1 is Done.
            #
            # We cannot confidently treat ISSUE-5
            # as a real active blocker.
            if related_has_hierarchy_mismatch:
                signals.append(
                    IssueSignal(
                        code=(
                            "DEPENDENCY_NEEDS_VERIFICATION"
                        ),
                        severity="warning",
                        message=(
                            f"{issue.key} is linked "
                            f"as blocked by "
                            f"{related_issue.key}, "
                            f"but {related_issue.key} "
                            "has a parent/child "
                            "status mismatch"
                        ),
                    )
                )

                continue

            signals.append(
                IssueSignal(
                    code="BLOCKED",
                    severity="warning",
                    message=(
                        f"{issue.key} is blocked by "
                        f"{related_issue.key} "
                        f"({related_issue.status})"
                    ),
                )
            )

        # ----------------------------------
        # CURRENT ISSUE BLOCKS ANOTHER
        # ----------------------------------

        elif relation == "blocks":
            if (
                issue.status
                in DONE_STATUSES
            ):
                continue

            # Example:
            #
            # ISSUE-5 blocks ISSUE-6 / ISSUE-9
            #
            # but ISSUE-5 parent ISSUE-1 is Done.
            #
            # Treat dependency as potentially stale.
            if issue_has_hierarchy_mismatch:
                signals.append(
                    IssueSignal(
                        code=(
                            "STALE_DEPENDENCY_CANDIDATE"
                        ),
                        severity="warning",
                        message=(
                            f"{issue.key} still "
                            f"blocks "
                            f"{related_issue.key}, "
                            f"but parent "
                            f"{issue.parent_key} "
                            "is already Done"
                        ),
                    )
                )

                continue

            signals.append(
                IssueSignal(
                    code="BLOCKING_OTHERS",
                    severity="warning",
                    message=(
                        f"{issue.key} blocks "
                        f"{related_issue.key}"
                    ),
                )
            )

    return signals