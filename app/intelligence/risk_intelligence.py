from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.risk.policy import classify_delivery_risk, is_done_status, risk_pressure_score


@dataclass(frozen=True)
class RiskEscalationPolicy:
    blocker_escalation_days: float = 1.0
    overdue_escalation_days: int = 3
    dependency_escalation_count: int = 3
    critical_pressure_score: int = 8
    action_pressure_score: int = 4


@dataclass
class IssueRiskLifecycle:
    issue_key: str
    current_score: int
    previous_score: int | None
    delivery_risk_level: str
    lifecycle_state: str  # NEW | ACTIVE | ESCALATING | IMPROVING | RESOLVED
    escalation_level: str  # NONE | WATCH | ACTION_REQUIRED | ESCALATE
    escalation_reasons: list[str] = field(default_factory=list)
    risk_age_days: float | None = None
    blocker_observed_age_days: float | None = None
    status_age_days: float | None = None
    overdue_age_days: int | None = None
    direct_downstream: list[str] = field(default_factory=list)
    propagated_downstream: list[str] = field(default_factory=list)


@dataclass
class RiskIntelligence:
    project_score: int
    previous_project_score: int | None
    project_trend: str  # BASELINE | UP | DOWN | STABLE
    items: list[IssueRiskLifecycle] = field(default_factory=list)
    new_risks: list[IssueRiskLifecycle] = field(default_factory=list)
    escalations: list[IssueRiskLifecycle] = field(default_factory=list)
    improvements: list[IssueRiskLifecycle] = field(default_factory=list)
    resolved: list[IssueRiskLifecycle] = field(default_factory=list)
    escalation_candidates: list[IssueRiskLifecycle] = field(default_factory=list)
    persistent_blockers: list[IssueRiskLifecycle] = field(default_factory=list)
    overdue_items: list[IssueRiskLifecycle] = field(default_factory=list)
    dependency_hotspots: list[IssueRiskLifecycle] = field(default_factory=list)

    @property
    def has_material_change(self) -> bool:
        return bool(
            self.new_risks
            or self.escalations
            or self.improvements
            or self.resolved
        )


def build_risk_intelligence(
    current_snapshot: dict[str, Any],
    history: list[dict[str, Any]],
    *,
    policy: RiskEscalationPolicy | None = None,
) -> RiskIntelligence:
    policy = policy or RiskEscalationPolicy()
    previous = history[-1] if history else None

    current_issues = current_snapshot.get("issues", {})
    previous_issues = previous.get("issues", {}) if previous else {}
    graph = _blocking_graph(current_issues)

    issue_keys = sorted(set(current_issues) | set(previous_issues))
    items: list[IssueRiskLifecycle] = []

    for issue_key in issue_keys:
        current_issue = current_issues.get(issue_key)
        previous_issue = previous_issues.get(issue_key)

        current_score = _issue_score(current_issue)
        previous_score = _issue_score(previous_issue) if previous_issue else None
        lifecycle_state = _lifecycle_state(previous_score, current_score)

        signal_codes = set((current_issue or {}).get("signals") or [])
        delivery_risk_level = classify_delivery_risk(
            signal_codes,
            done=is_done_status((current_issue or {}).get("status")),
        ) if current_issue else "NONE"

        direct = sorted(graph.get(issue_key, set())) if current_issue else []
        propagated = (
            sorted(_descendants(issue_key, graph) - set(direct))
            if current_issue
            else []
        )

        blocker_age = _consecutive_signal_age_days(
            issue_key,
            "BLOCKING_OTHERS",
            current_snapshot,
            history,
        )
        risk_age = _consecutive_risk_age_days(
            issue_key,
            current_snapshot,
            history,
        )
        overdue_age = _overdue_age(current_issue or {})
        status_age = _metric_float(current_issue, "days_in_status")

        escalation_level, escalation_reasons = _evaluate_escalation(
            current_score=current_score,
            delivery_risk_level=delivery_risk_level,
            lifecycle_state=lifecycle_state,
            blocker_age_days=blocker_age,
            overdue_age_days=overdue_age,
            direct_dependency_count=len(direct),
            propagated_dependency_count=len(propagated),
            policy=policy,
        )

        items.append(
            IssueRiskLifecycle(
                issue_key=issue_key,
                current_score=current_score,
                previous_score=previous_score,
                delivery_risk_level=delivery_risk_level,
                lifecycle_state=lifecycle_state,
                escalation_level=escalation_level,
                escalation_reasons=escalation_reasons,
                risk_age_days=risk_age,
                blocker_observed_age_days=blocker_age,
                status_age_days=status_age,
                overdue_age_days=overdue_age,
                direct_downstream=direct,
                propagated_downstream=propagated,
            )
        )

    project_score = sum(
        _issue_score(issue)
        for issue in current_issues.values()
    )
    previous_project_score = (
        sum(_issue_score(issue) for issue in previous_issues.values())
        if previous is not None
        else None
    )

    def rank(item: IssueRiskLifecycle) -> tuple[int, int, str]:
        escalation_order = {
            "ESCALATE": 3,
            "ACTION_REQUIRED": 2,
            "WATCH": 1,
            "NONE": 0,
        }
        return (
            -escalation_order.get(item.escalation_level, 0),
            -item.current_score,
            item.issue_key,
        )

    current_risk_items = [item for item in items if item.current_score > 0]

    return RiskIntelligence(
        project_score=project_score,
        previous_project_score=previous_project_score,
        project_trend=(
            "BASELINE"
            if previous_project_score is None
            else _direction(previous_project_score, project_score)
        ),
        items=items,
        new_risks=sorted(
            [item for item in items if item.lifecycle_state == "NEW" and item.current_score > 0],
            key=rank,
        ),
        escalations=sorted(
            [item for item in items if item.lifecycle_state == "ESCALATING"],
            key=rank,
        ),
        improvements=sorted(
            [item for item in items if item.lifecycle_state == "IMPROVING"],
            key=rank,
        ),
        resolved=sorted(
            [item for item in items if item.lifecycle_state == "RESOLVED"],
            key=lambda item: item.issue_key,
        ),
        escalation_candidates=sorted(
            [
                item
                for item in current_risk_items
                if item.escalation_level == "ESCALATE"
            ],
            key=rank,
        ),
        persistent_blockers=sorted(
            [item for item in current_risk_items if item.blocker_observed_age_days is not None],
            key=lambda item: (
                -(item.blocker_observed_age_days or 0.0),
                -item.current_score,
                item.issue_key,
            ),
        ),
        overdue_items=sorted(
            [item for item in current_risk_items if item.overdue_age_days is not None],
            key=lambda item: (
                -(item.overdue_age_days or 0),
                -item.current_score,
                item.issue_key,
            ),
        ),
        dependency_hotspots=sorted(
            [item for item in current_risk_items if item.direct_downstream or item.propagated_downstream],
            key=lambda item: (
                -(len(item.direct_downstream) + len(item.propagated_downstream)),
                -item.current_score,
                item.issue_key,
            ),
        ),
    )


def risk_intelligence_to_dict(value: RiskIntelligence) -> dict[str, Any]:
    def item(x: IssueRiskLifecycle) -> dict[str, Any]:
        return {
            "issue_key": x.issue_key,
            "current_score": x.current_score,
            "previous_score": x.previous_score,
            "delivery_risk_level": x.delivery_risk_level,
            "lifecycle_state": x.lifecycle_state,
            "escalation_level": x.escalation_level,
            "escalation_reasons": x.escalation_reasons,
            "risk_age_days": x.risk_age_days,
            "blocker_observed_age_days": x.blocker_observed_age_days,
            "status_age_days": x.status_age_days,
            "overdue_age_days": x.overdue_age_days,
            "direct_downstream": x.direct_downstream,
            "propagated_downstream": x.propagated_downstream,
        }

    return {
        "version": 3,
        "project_score": value.project_score,
        "previous_project_score": value.previous_project_score,
        "project_trend": value.project_trend,
        "has_material_change": value.has_material_change,
        "new_risks": [item(x) for x in value.new_risks],
        "escalations": [item(x) for x in value.escalations],
        "improvements": [item(x) for x in value.improvements],
        "resolved": [item(x) for x in value.resolved],
        "escalation_candidates": [item(x) for x in value.escalation_candidates],
        "persistent_blockers": [item(x) for x in value.persistent_blockers],
        "overdue_items": [item(x) for x in value.overdue_items],
        "dependency_hotspots": [item(x) for x in value.dependency_hotspots],
    }


def _issue_score(issue: dict[str, Any] | None) -> int:
    if not issue:
        return 0
    return risk_pressure_score(set(issue.get("signals") or []))


def _direction(previous: int, current: int) -> str:
    if current > previous:
        return "UP"
    if current < previous:
        return "DOWN"
    return "STABLE"


def _lifecycle_state(previous: int | None, current: int) -> str:
    if previous is None:
        return "NEW" if current > 0 else "ACTIVE"
    if previous <= 0 < current:
        return "NEW"
    if previous > 0 and current <= 0:
        return "RESOLVED"
    if current > previous:
        return "ESCALATING"
    if 0 < current < previous:
        return "IMPROVING"
    return "ACTIVE"


def _evaluate_escalation(
    *,
    current_score: int,
    delivery_risk_level: str,
    lifecycle_state: str,
    blocker_age_days: float | None,
    overdue_age_days: int | None,
    direct_dependency_count: int,
    propagated_dependency_count: int,
    policy: RiskEscalationPolicy,
) -> tuple[str, list[str]]:
    if current_score <= 0:
        return "NONE", []

    reasons: list[str] = []

    if delivery_risk_level == "CRITICAL" or current_score >= policy.critical_pressure_score:
        reasons.append("critical delivery pressure")

    if (
        blocker_age_days is not None
        and blocker_age_days >= policy.blocker_escalation_days
    ):
        reasons.append(
            f"blocker observed for >= {policy.blocker_escalation_days:g}d"
        )

    if (
        overdue_age_days is not None
        and overdue_age_days >= policy.overdue_escalation_days
    ):
        reasons.append(
            f"overdue for >= {policy.overdue_escalation_days}d"
        )

    dependency_count = direct_dependency_count + propagated_dependency_count
    if dependency_count >= policy.dependency_escalation_count:
        if propagated_dependency_count:
            reasons.append(
                f"affects {direct_dependency_count} direct and "
                f"{propagated_dependency_count} propagated downstream issues"
            )
        else:
            reasons.append(
                f"affects {direct_dependency_count} direct downstream issues"
            )

    if reasons:
        return "ESCALATE", reasons

    if current_score >= policy.action_pressure_score or lifecycle_state in {"NEW", "ESCALATING"}:
        action_reasons = []
        if lifecycle_state == "NEW":
            action_reasons.append("new risk")
        elif lifecycle_state == "ESCALATING":
            action_reasons.append("risk pressure increased")
        if current_score >= policy.action_pressure_score:
            action_reasons.append("actionable delivery pressure")
        return "ACTION_REQUIRED", action_reasons

    return "WATCH", ["delivery signal requires monitoring"]


def _blocking_graph(issues: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    """Return the EFFECTIVE active blocking graph.

    Jira links are topology and may outlive the actual blocking condition.
    An edge participates in delivery/root-cause reasoning only while the
    source issue is currently an active blocker (BLOCKING_OTHERS) and both
    endpoints are still open. Stale / needs-verification links remain in the
    raw snapshot for audit, but must not create an active root cause.
    """
    graph: dict[str, set[str]] = {}
    for issue_key, issue in issues.items():
        if is_done_status(issue.get("status")):
            continue
        signals = set(issue.get("signals") or [])
        if "BLOCKING_OTHERS" not in signals:
            continue
        for dep in issue.get("dependencies") or []:
            if (
                str(dep.get("relation", "")).lower() == "blocks"
                and str(dep.get("direction", "")).lower() == "outward"
            ):
                target = dep.get("related_issue_key")
                target_issue = issues.get(str(target)) if target else None
                if target and target_issue and not is_done_status(target_issue.get("status")):
                    graph.setdefault(issue_key, set()).add(str(target))
    return graph


def _descendants(start: str, graph: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    stack = list(graph.get(start, set()))
    while stack:
        key = stack.pop()
        if key in seen or key == start:
            continue
        seen.add(key)
        stack.extend(graph.get(key, set()))
    return seen


def _overdue_age(issue: dict[str, Any]) -> int | None:
    metrics = issue.get("metrics") or {}
    days_to_due = metrics.get("days_to_due")
    if isinstance(days_to_due, (int, float)) and days_to_due < 0:
        return int(abs(days_to_due))
    return None


def _metric_float(issue: dict[str, Any] | None, key: str) -> float | None:
    if not issue:
        return None
    value = (issue.get("metrics") or {}).get(key)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _consecutive_signal_age_days(
    issue_key: str,
    signal_code: str,
    current_snapshot: dict[str, Any],
    history: list[dict[str, Any]],
) -> float | None:
    current_issue = current_snapshot.get("issues", {}).get(issue_key, {})
    if signal_code not in set(current_issue.get("signals") or []):
        return None

    snapshots = [*history, current_snapshot]
    first_active = current_snapshot
    for snapshot in reversed(snapshots):
        issue = snapshot.get("issues", {}).get(issue_key)
        if not issue or signal_code not in set(issue.get("signals") or []):
            break
        first_active = snapshot

    return _snapshot_age(first_active, current_snapshot)


def _consecutive_risk_age_days(
    issue_key: str,
    current_snapshot: dict[str, Any],
    history: list[dict[str, Any]],
) -> float | None:
    current_issue = current_snapshot.get("issues", {}).get(issue_key)
    if _issue_score(current_issue) <= 0:
        return None

    snapshots = [*history, current_snapshot]
    first_active = current_snapshot
    for snapshot in reversed(snapshots):
        issue = snapshot.get("issues", {}).get(issue_key)
        if _issue_score(issue) <= 0:
            break
        first_active = snapshot

    return _snapshot_age(first_active, current_snapshot)


def _snapshot_age(start_snapshot: dict[str, Any], end_snapshot: dict[str, Any]) -> float:
    start = _parse_time(start_snapshot.get("captured_at"))
    end = _parse_time(end_snapshot.get("captured_at"))
    if start and end:
        return round(max(0.0, (end - start).total_seconds() / 86400), 2)
    return 0.0
