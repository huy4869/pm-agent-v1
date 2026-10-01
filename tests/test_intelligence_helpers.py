from dataclasses import dataclass

from app.intelligence.change_summary import build_change_summary
from app.intelligence.dependency_clusters import build_dependency_clusters
from app.intelligence.risk_intelligence import IssueRiskLifecycle, RiskIntelligence
from app.memory.delta import DeltaEvent, ProjectDelta


def test_burst_change_summary():
    delta = ProjectDelta(events=[
        DeltaEvent(code="ISSUE_ADDED", issue_key=f"DEV-{i}", category="direct", message="added")
        for i in range(25)
    ])
    summary = build_change_summary(delta, detail_limit=5, burst_threshold=20)
    assert summary.mode == "BURST"
    assert summary.material_events == 25
    assert summary.counts_by_code["ISSUE_ADDED"] == 25


def test_dependency_root_cluster():
    def item(key, direct, propagated, score=4):
        return IssueRiskLifecycle(
            issue_key=key,
            current_score=score,
            previous_score=score,
            delivery_risk_level="HIGH",
            lifecycle_state="ACTIVE",
            escalation_level="ACTION_REQUIRED",
            direct_downstream=direct,
            propagated_downstream=propagated,
        )

    risk = RiskIntelligence(
        project_score=12,
        previous_project_score=12,
        project_trend="STABLE",
        items=[
            item("DEV-27", ["DEV-26"], ["DEV-25", "DEV-24"]),
            item("DEV-26", ["DEV-25"], ["DEV-24"]),
            item("DEV-25", ["DEV-24"], []),
            item("DEV-24", [], [], 1),
        ],
    )
    clusters = build_dependency_clusters(risk)
    assert clusters[0].root_issue_key == "DEV-27"
    assert clusters[0].affected_issue_keys == ["DEV-24", "DEV-25", "DEV-26"]
    assert clusters[0].max_depth == 3


def test_effective_dependency_graph_excludes_stale_verification_link():
    from app.intelligence.risk_intelligence import build_risk_intelligence

    snapshot = {
        "captured_at": "2026-08-23T01:00:00+00:00",
        "issues": {
            "DEV-5": {
                "status": "To Do",
                "signals": ["STALE_DEPENDENCY_CANDIDATE"],
                "dependencies": [
                    {"relation": "blocks", "direction": "outward", "related_issue_key": "DEV-6"}
                ],
                "metrics": {},
            },
            "DEV-6": {
                "status": "Idea",
                "signals": ["DEPENDENCY_NEEDS_VERIFICATION"],
                "dependencies": [
                    {"relation": "is blocked by", "direction": "inward", "related_issue_key": "DEV-5"}
                ],
                "metrics": {},
            },
        },
    }
    ri = build_risk_intelligence(snapshot, [])
    by_key = {x.issue_key: x for x in ri.items}
    assert by_key["DEV-5"].direct_downstream == []
    assert build_dependency_clusters(ri) == []


def test_effective_dependency_graph_keeps_confirmed_active_blocker():
    from app.intelligence.risk_intelligence import build_risk_intelligence

    snapshot = {
        "captured_at": "2026-08-23T01:00:00+00:00",
        "issues": {
            "DEV-15": {
                "status": "In Progress",
                "signals": ["BLOCKING_OTHERS", "OVERDUE"],
                "dependencies": [
                    {"relation": "blocks", "direction": "outward", "related_issue_key": "DEV-12"}
                ],
                "metrics": {"days_to_due": -4},
            },
            "DEV-12": {
                "status": "In Progress",
                "signals": ["BLOCKED"],
                "dependencies": [
                    {"relation": "is blocked by", "direction": "inward", "related_issue_key": "DEV-15"}
                ],
                "metrics": {},
            },
        },
    }
    ri = build_risk_intelligence(snapshot, [])
    by_key = {x.issue_key: x for x in ri.items}
    assert by_key["DEV-15"].direct_downstream == ["DEV-12"]
    clusters = build_dependency_clusters(ri)
    assert clusters and clusters[0].root_issue_key == "DEV-15"
