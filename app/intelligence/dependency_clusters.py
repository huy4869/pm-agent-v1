from __future__ import annotations

from dataclasses import dataclass, field

from app.intelligence.risk_intelligence import RiskIntelligence


@dataclass(frozen=True)
class DependencyRiskCluster:
    root_issue_key: str
    direct_downstream: list[str] = field(default_factory=list)
    propagated_downstream: list[str] = field(default_factory=list)
    affected_issue_keys: list[str] = field(default_factory=list)
    max_depth: int = 0
    aggregate_pressure: int = 0


def build_dependency_clusters(
    risk_intelligence: RiskIntelligence | None,
) -> list[DependencyRiskCluster]:
    if risk_intelligence is None:
        return []

    blocker_items = {
        item.issue_key: item
        for item in risk_intelligence.items
        if item.current_score > 0 and item.direct_downstream
    }
    if not blocker_items:
        return []

    incoming = set()
    for item in blocker_items.values():
        incoming.update(key for key in item.direct_downstream if key in blocker_items)

    roots = [key for key in blocker_items if key not in incoming]
    if not roots:
        roots = list(blocker_items)

    score_by_key = {item.issue_key: item.current_score for item in risk_intelligence.items}
    graph = {key: set(item.direct_downstream) for key, item in blocker_items.items()}

    clusters = []
    for root in roots:
        direct = sorted(graph.get(root, set()))
        descendants, depth = _descendants_with_depth(root, graph)
        propagated = sorted(descendants - set(direct))
        affected = sorted(descendants)
        aggregate_pressure = score_by_key.get(root, 0) + sum(
            score_by_key.get(key, 0) for key in affected
        )
        clusters.append(
            DependencyRiskCluster(
                root_issue_key=root,
                direct_downstream=direct,
                propagated_downstream=propagated,
                affected_issue_keys=affected,
                max_depth=depth,
                aggregate_pressure=aggregate_pressure,
            )
        )

    return sorted(
        clusters,
        key=lambda c: (
            -len(c.affected_issue_keys),
            -c.max_depth,
            -c.aggregate_pressure,
            c.root_issue_key,
        ),
    )


def _descendants_with_depth(
    start: str, graph: dict[str, set[str]]
) -> tuple[set[str], int]:
    seen: set[str] = set()
    stack = [(key, 1) for key in graph.get(start, set())]
    max_depth = 0
    while stack:
        key, depth = stack.pop()
        if key == start:
            continue
        max_depth = max(max_depth, depth)
        if key in seen:
            continue
        seen.add(key)
        for child in graph.get(key, set()):
            stack.append((child, depth + 1))
    return seen, max_depth
