from dataclasses import dataclass, field


@dataclass
class RiskEvidence:
    type: str

    issue_key: str | None = None
    value: str | None = None

    related_issue_keys: list[str] = field(
        default_factory=list
    )


@dataclass
class AIRisk:
    issue_key: str
    level: str

    evidence: list[RiskEvidence] = field(
        default_factory=list
    )

    impact: str = ""
    confidence: str = "MEDIUM"
    recommended_action: str = ""


@dataclass
class ProjectAIAnalysis:
    health: str
    summary: str

    risks: list[AIRisk] = field(
        default_factory=list
    )

    observations: list[str] = field(
        default_factory=list
    )

    pm_actions: list[str] = field(
        default_factory=list
    )