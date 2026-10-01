from app.domain.models import IssueMetrics, IssueSignal, ProjectIssue, ProjectIssueState, ProjectState
from app.intelligence.redmine_delivery import build_project_delivery
from app.metrics.project_metrics import calculate_project_metrics


def _held_state(*signals: str) -> ProjectIssueState:
    issue = ProjectIssue(
        key="RM-1",
        summary="Held task",
        status="Held",
        assignee=None,
        priority=None,
        issue_type="Task",
        created_at=None,
        updated_at=None,
        due_date=None,
        parent_key=None,
        dependencies=[],
        fixed_version_id=None,
        fixed_version_name=None,
        done_ratio=0,
        source="redmine",
    )
    return ProjectIssueState(
        issue=issue,
        metrics=IssueMetrics(days_in_status=None, days_since_update=None, days_to_due=None),
        signals=[IssueSignal(code=code, severity="warning", message=code) for code in signals],
    )


def test_held_is_pending_not_blocked_or_unassigned_metric():
    state = ProjectState(project_key="demo", issues=[_held_state("BLOCKED")])
    metrics = calculate_project_metrics(state)
    assert metrics.pending_issues == 1
    assert metrics.blocked_issues == 0
    assert metrics.unassigned_issues == 0


def test_pending_alone_does_not_create_project_hotspot():
    issues = [{
        "done": False,
        "pending": True,
        "overdue": False,
        "blocked": False,
        "blocking": False,
        "stale": False,
        "unassigned": False,
        "nearDue": False,
        "assignee": None,
    }]
    risk, actions = build_project_delivery(issues, None)
    assert risk["level"] == "GREEN"
    assert actions == []
