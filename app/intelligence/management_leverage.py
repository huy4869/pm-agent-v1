from __future__ import annotations

from dataclasses import dataclass

from app.intelligence.dependency_clusters import build_dependency_clusters


@dataclass(frozen=True)
class ManagementLeverage:
    issue_key: str
    score: int
    reasons: list[str]


def build_management_leverage(risk_intelligence) -> list[ManagementLeverage]:
    """Rank issues by PM leverage, not only by how painful the issue itself is.

    A root blocker can therefore outrank a downstream critical symptom when
    resolving the root is likely to release multiple dependent issues.
    """
    if risk_intelligence is None:
        return []

    cluster_by_root = {
        c.root_issue_key: c for c in build_dependency_clusters(risk_intelligence)
    }
    results: list[ManagementLeverage] = []

    for item in risk_intelligence.items:
        if item.current_score <= 0:
            continue
        score = item.current_score
        reasons: list[str] = [f"risk pressure {item.current_score}"]

        direct = len(item.direct_downstream)
        propagated = len(item.propagated_downstream)
        if direct:
            score += direct * 2
            reasons.append(f"{direct} direct downstream")
        if propagated:
            score += propagated * 3
            reasons.append(f"{propagated} propagated downstream")
        if item.issue_key in cluster_by_root and propagated:
            score += 4
            reasons.append("root-cause leverage")
        if item.escalation_level == "ESCALATE":
            score += 3
            reasons.append("escalation candidate")
        elif item.escalation_level == "ACTION_REQUIRED":
            score += 1
        if item.overdue_age_days:
            score += min(item.overdue_age_days, 3)
            reasons.append(f"overdue {item.overdue_age_days}d")

        results.append(ManagementLeverage(item.issue_key, score, reasons))

    return sorted(results, key=lambda x: (-x.score, x.issue_key))
