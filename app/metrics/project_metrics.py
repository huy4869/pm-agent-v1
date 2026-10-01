from app.domain.models import ProjectMetrics, ProjectState
from app.domain.statuses import is_active_status, is_done_status, is_pending_status


def calculate_project_metrics(project_state: ProjectState) -> ProjectMetrics:
    total_issues = len(project_state.issues)
    active_issues = 0
    done_issues = 0
    overdue_issues = 0
    near_due_issues = 0
    stale_issues = 0
    stuck_issues = 0
    unassigned_issues = 0
    pending_issues = 0
    blocked_issues = 0
    blocking_issues = 0
    hierarchy_mismatches = 0
    dependencies_to_verify = 0
    dependency_pairs: set[tuple[str, str]] = set()

    for state in project_state.issues:
        issue = state.issue
        pending = is_pending_status(issue.status)
        done = is_done_status(issue.status)

        if is_active_status(issue.status):
            active_issues += 1
        if done:
            done_issues += 1
        if pending and not done:
            pending_issues += 1

        # Pending/Held is not actionable merely because it has no owner.
        if not done and not pending and not issue.assignee:
            unassigned_issues += 1

        signal_codes = {signal.code for signal in state.signals}
        if "OVERDUE" in signal_codes:
            overdue_issues += 1
        if "NEAR_DUE" in signal_codes:
            near_due_issues += 1
        if "STALE" in signal_codes:
            stale_issues += 1
        if "STUCK" in signal_codes:
            stuck_issues += 1

        # A Held/Pending status is intentionally parked work. Do not present it
        # as a Blocked hot spot solely because a Redmine dependency relation is
        # still attached. It can still surface through overdue or blocking-others.
        if "BLOCKED" in signal_codes and not pending:
            blocked_issues += 1
        if "BLOCKING_OTHERS" in signal_codes:
            blocking_issues += 1
        if "PARENT_DONE_CHILD_OPEN" in signal_codes:
            hierarchy_mismatches += 1
        if "DEPENDENCY_NEEDS_VERIFICATION" in signal_codes or "STALE_DEPENDENCY_CANDIDATE" in signal_codes:
            dependencies_to_verify += 1

        for dependency in issue.dependencies or []:
            dependency_pairs.add(tuple(sorted((issue.key, dependency.related_issue_key))))

    return ProjectMetrics(
        total_issues=total_issues,
        active_issues=active_issues,
        done_issues=done_issues,
        overdue_issues=overdue_issues,
        near_due_issues=near_due_issues,
        stale_issues=stale_issues,
        stuck_issues=stuck_issues,
        unassigned_issues=unassigned_issues,
        pending_issues=pending_issues,
        blocked_issues=blocked_issues,
        blocking_issues=blocking_issues,
        dependency_links=len(dependency_pairs),
        hierarchy_mismatches=hierarchy_mismatches,
        dependencies_to_verify=dependencies_to_verify,
    )
