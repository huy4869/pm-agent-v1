import os

from app.ai.grounding import ground_ai_analysis
from app.ai.models import AIRisk, ProjectAIAnalysis, RiskEvidence
from app.domain.models import IssueDependency, IssueMetrics, ProjectIssue, ProjectIssueState, ProjectState, RiskAssessment
from app.i18n import health_label


def _state(key, assignee=None, deps=None, days_to_due=None, status="Idea"):
    issue=ProjectIssue(key=key,summary=key,status=status,assignee=assignee,priority=None,issue_type="Task",created_at=None,updated_at=None,due_date=None,parent_key=None,dependencies=deps or [])
    return ProjectIssueState(issue=issue,metrics=IssueMetrics(0,0,days_to_due),signals=[],risk=RiskAssessment("LOW",[]))


def test_grounding_health_assignee_and_dependency(monkeypatch):
    monkeypatch.setenv("REPORT_LANGUAGE","vi")
    p=ProjectState("DEV",[
        _state("DEV-25","tran huy",[IssueDependency("DEV-25","DEV-24","blocks","outward"),IssueDependency("DEV-25","DEV-26","is blocked by","inward")],-3),
        _state("DEV-27",None,[IssueDependency("DEV-27","DEV-26","blocks","outward")]),
    ])
    a=ProjectAIAnalysis("AT_RISK","x",[
        AIRisk("DEV-25","CRITICAL",[
            RiskEvidence("BLOCKED_BY","DEV-25",None,["DEV-27"]),
            RiskEvidence("ASSIGNEE","DEV-25",None,[]),
        ],recommended_action="Assign an owner to DEV-25")
    ],[],["Assign an owner to DEV-25"])
    out=ground_ai_analysis(a,p,"CRITICAL")
    assert out.health=="AT_RISK"  # AI-first: deterministic health is audit/fallback only
    assert out.risks[0].evidence[0].related_issue_keys==["DEV-26"]
    assert out.risks[0].evidence[1].value=="tran huy"
    assert "tran huy" in out.pm_actions[0]


def test_vietnamese_health_label(monkeypatch):
    monkeypatch.setenv("REPORT_LANGUAGE","vi")
    assert health_label("CRITICAL")=="CRITICAL"
    monkeypatch.setenv("REPORT_LANGUAGE","en")
    assert health_label("CRITICAL")=="CRITICAL"


def test_grounding_ignores_done_blocker_and_drops_done_only_action(monkeypatch):
    monkeypatch.setenv("REPORT_LANGUAGE", "vi")
    p = ProjectState("DEV", [
        _state("DEV-25", "tran huy", [IssueDependency("DEV-25", "DEV-26", "is blocked by", "inward")], -4),
        _state("DEV-26", None, [IssueDependency("DEV-26", "DEV-25", "blocks", "outward")], status="Done"),
        _state("DEV-1", "tran huy", status="Done"),
    ])
    a = ProjectAIAnalysis(
        "CRITICAL",
        "summary",
        [AIRisk("DEV-25", "CRITICAL", [RiskEvidence("BLOCKED_BY", "DEV-25", None, ["DEV-26"])])],
        [],
        ["Theo dõi với tran huy về DEV-1 và xác nhận ETA/kế hoạch xử lý."],
    )
    out = ground_ai_analysis(a, p, "CRITICAL")
    assert out.risks[0].evidence[0].related_issue_keys == []
    assert out.pm_actions == []


def test_grounding_removes_done_issue_from_current_risks():
    p = ProjectState("DEV", [_state("DEV-26", status="Done")])
    a = ProjectAIAnalysis(
        "CRITICAL", "summary",
        [AIRisk("DEV-26", "HIGH", [RiskEvidence("STATUS", "DEV-26", "Idea", [])])],
        [], [],
    )
    out = ground_ai_analysis(a, p, "CRITICAL")
    assert out.risks == []
