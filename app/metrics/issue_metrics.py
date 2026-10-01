from datetime import datetime, timezone
from app.domain.models import IssueMetrics, ProjectIssue
from app.time_utils import local_today

def parse_jira_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    return datetime.fromisoformat(value)


def calculate_days_between(
    earlier: str | None,
    now: datetime | None = None,
) -> float | None:
    dt = parse_jira_datetime(earlier)

    if not dt:
        return None

    if now is None:
        now = datetime.now(timezone.utc)

    delta = now - dt.astimezone(timezone.utc)

    return round(delta.total_seconds() / 86400, 2)


def calculate_days_to_due(
    due_date: str | None,
    now: datetime | None = None,
) -> int | None:
    if not due_date:
        return None

    due = datetime.fromisoformat(due_date).date()
    return (due - local_today(now)).days

def calculate_issue_metrics(
    issue: ProjectIssue,
) -> IssueMetrics:
    return IssueMetrics(
        days_in_status=calculate_days_between(issue.status_since),
        days_since_update=calculate_days_between(issue.updated_at),
        days_to_due=calculate_days_to_due(issue.due_date),
    )