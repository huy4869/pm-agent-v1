from dataclasses import dataclass
from typing import Optional


@dataclass
class StatusChange:
    from_status: Optional[str]
    to_status: str
    changed_at: str


@dataclass
class IssueDependency:
    issue_key: str
    related_issue_key: str
    relation: str
    direction: str


@dataclass
class ProjectIssue:
    key: str
    summary: str
    status: str

    assignee: Optional[str]
    priority: Optional[str]
    issue_type: Optional[str]

    created_at: Optional[str]
    updated_at: Optional[str]
    due_date: Optional[str]

    parent_key: Optional[str]

    status_history: Optional[list[StatusChange]] = None
    status_since: Optional[str] = None

    dependencies: Optional[list[IssueDependency]] = None

    fixed_version_id: Optional[str] = None
    fixed_version_name: Optional[str] = None
    done_ratio: Optional[int] = None

    source: str = "jira"


@dataclass
class IssueMetrics:
    days_in_status: Optional[float]
    days_since_update: Optional[float]
    days_to_due: Optional[int]


@dataclass
class IssueSignal:
    code: str
    severity: str
    message: str


@dataclass
class RiskAssessment:
    level: str
    reasons: list[str]


@dataclass
class ProjectIssueState:
    issue: ProjectIssue
    metrics: IssueMetrics
    signals: list[IssueSignal]
    risk: Optional[RiskAssessment] = None


@dataclass
class ProjectMetrics:
    total_issues: int
    active_issues: int
    done_issues: int

    overdue_issues: int
    near_due_issues: int
    stale_issues: int
    stuck_issues: int
    unassigned_issues: int
    pending_issues: int

    blocked_issues: int
    blocking_issues: int
    dependency_links: int

    hierarchy_mismatches: int
    dependencies_to_verify: int


@dataclass
class ProjectState:
    project_key: str
    issues: list[ProjectIssueState]
    metrics: Optional[ProjectMetrics] = None


@dataclass
class ProjectRiskSummary:
    total_risky_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int

    top_risk_issue_keys: list[str]


@dataclass
class ProjectIntelligenceSummary:
    health: str
    headline: str
    top_concerns: list[str]
    observations: list[str]