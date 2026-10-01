from app.domain.models import IssueSignal, ProjectIssue, RiskAssessment
from app.risk.policy import (
    classify_delivery_risk,
    is_done_status,
    risk_reasons,
)


def assess_issue_risk(
    issue: ProjectIssue,
    signals: list[IssueSignal],
) -> RiskAssessment:
    """Deterministic current-state delivery-risk baseline.

    This layer classifies factual Jira signals only. Historical persistence
    and trend are handled by Risk Intelligence; contextual interpretation
    is handled by the AI analyst.
    """
    signal_codes = {signal.code for signal in signals if signal.code}

    return RiskAssessment(
        level=classify_delivery_risk(
            signal_codes,
            done=is_done_status(issue.status),
        ),
        reasons=risk_reasons(signal_codes),
    )
