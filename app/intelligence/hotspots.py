from dataclasses import dataclass, field

from app.domain.models import ProjectState
from app.memory.delta import DeltaEvent, ProjectDelta
from app.risk.policy import (
    RISK_LEVEL_ORDER,
    classify_delivery_risk,
    is_done_status,
    max_risk_level,
    risk_pressure_score,
)


@dataclass
class Hotspot:
    issue_key: str
    score: int
    level: str
    reasons: list[str] = field(default_factory=list)
    delta_codes: list[str] = field(default_factory=list)


@dataclass
class ProjectHotspots:
    items: list[Hotspot] = field(default_factory=list)
    significant_issue_keys: set[str] = field(default_factory=set)

    def is_significant(self, issue_key: str | None) -> bool:
        return bool(issue_key and issue_key in self.significant_issue_keys)

    def is_significant_event(self, event: DeltaEvent) -> bool:
        # Raw NO_PROGRESS remains in audit history, but only reaches AI/report
        # when the affected issue is already a meaningful hotspot.
        if event.code != "NO_PROGRESS":
            return True
        return self.is_significant(event.issue_key)


def build_project_hotspots(
    project_state: ProjectState,
    delta: ProjectDelta,
    *,
    min_score: int = 3,
    max_items: int = 8,
) -> ProjectHotspots:
    delta_by_issue: dict[str, set[str]] = {}
    for event in delta.events:
        if event.issue_key:
            delta_by_issue.setdefault(event.issue_key, set()).add(event.code)

    hotspots: list[Hotspot] = []

    for state in project_state.issues:
        issue = state.issue
        signal_codes = {signal.code for signal in state.signals if signal.code}
        delta_codes = delta_by_issue.get(issue.key, set())

        score = risk_pressure_score(signal_codes)
        reasons: list[str] = []

        reason_by_signal = {
            "OVERDUE": "overdue",
            "BLOCKING_OTHERS": "blocking downstream work",
            "BLOCKED": "blocked",
            "STUCK": "stuck in active work",
            "NEAR_DUE": "near due",
            "STALE": "stale active work",
            "PARENT_DONE_CHILD_OPEN": "workflow inconsistency",
            "DEPENDENCY_NEEDS_VERIFICATION": "dependency needs verification",
            "STALE_DEPENDENCY_CANDIDATE": "dependency needs verification",
        }
        for code, reason in reason_by_signal.items():
            if code in signal_codes:
                reasons.append(reason)

        # Historical pressure bonuses. These affect hotspot ranking/trend, not
        # the factual current-state issue-risk classification.
        if "PERSISTENT_BLOCKER" in delta_codes:
            score += 2
            reasons.append("persistent blocker")
        if "ISSUE_REOPENED" in delta_codes:
            score += 2
            reasons.append("reopened")
        if "NO_PROGRESS" in delta_codes and score > 0:
            score += 1
            reasons.append("no recent progress")

        if score < min_score:
            continue

        baseline_level = classify_delivery_risk(
            signal_codes,
            done=is_done_status(issue.status),
        )
        temporal_level = (
            "CRITICAL" if score >= 8
            else "HIGH" if score >= 5
            else "MEDIUM"
        )
        level = max_risk_level(baseline_level, temporal_level)

        hotspots.append(
            Hotspot(
                issue_key=issue.key,
                score=score,
                level=level,
                reasons=list(dict.fromkeys(reasons)),
                delta_codes=sorted(delta_codes),
            )
        )

    hotspots.sort(
        key=lambda item: (
            -RISK_LEVEL_ORDER.get(item.level, 0),
            -item.score,
            item.issue_key,
        )
    )
    hotspots = hotspots[:max_items]

    return ProjectHotspots(
        items=hotspots,
        significant_issue_keys={item.issue_key for item in hotspots},
    )
