from app.domain.models import (
    ProjectRiskSummary,
    ProjectState,
)


RISK_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "NONE": 0,
}


def calculate_project_risk_summary(
    project_state: ProjectState,
    top_n: int = 5,
) -> ProjectRiskSummary:
    critical = 0
    high = 0
    medium = 0
    low = 0

    risky_states = []

    for state in project_state.issues:
        risk = state.risk

        if risk is None:
            continue

        if risk.level == "CRITICAL":
            critical += 1

        elif risk.level == "HIGH":
            high += 1

        elif risk.level == "MEDIUM":
            medium += 1

        elif risk.level == "LOW":
            low += 1

        # NONE không tính vào risk summary

        if risk.level in {
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        }:
            risky_states.append(state)

    risky_states.sort(
        key=lambda state: RISK_ORDER.get(
            state.risk.level,
            0,
        ),
        reverse=True,
    )

    top_risk_issue_keys = [
        state.issue.key
        for state in risky_states[:top_n]
    ]

    total_risky_issues = (
        critical
        + high
        + medium
    )

    return ProjectRiskSummary(
        total_risky_issues=total_risky_issues,
        critical_issues=critical,
        high_issues=high,
        medium_issues=medium,
        low_issues=low,
        top_risk_issue_keys=top_risk_issue_keys,
    )