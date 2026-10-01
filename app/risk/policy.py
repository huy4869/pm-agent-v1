from __future__ import annotations


RISK_LEVEL_ORDER = {
    "NONE": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}

# Numeric pressure weights are for temporal/trend comparison only.
# They are NOT severity labels by themselves.
RISK_PRESSURE_WEIGHTS = {
    "OVERDUE": 4,
    "BLOCKING_OTHERS": 4,
    "BLOCKED": 3,
    "STUCK": 3,
    "NEAR_DUE": 2,
    "STALE": 2,
    "PARENT_DONE_CHILD_OPEN": 2,
    "DEPENDENCY_NEEDS_VERIFICATION": 1,
    "STALE_DEPENDENCY_CANDIDATE": 1,
}

RISK_REASON_ORDER = tuple(RISK_PRESSURE_WEIGHTS.keys())


def normalize_status(value: str | None) -> str:
    return (value or "").strip().lower()


def is_done_status(value: str | None) -> bool:
    return normalize_status(value) in {"done", "closed", "resolved"}


def classify_delivery_risk(
    signal_codes: set[str],
    *,
    done: bool = False,
) -> str:
    """Classify deterministic *delivery* risk from factual signals.

    Signal severity and risk-pressure score are intentionally separate from
    this label. In particular, a slightly overdue issue is MEDIUM while an
    issue actively blocking downstream work is HIGH.
    """
    if done:
        return "NONE"

    if "BLOCKING_OTHERS" in signal_codes and (
        "OVERDUE" in signal_codes or "STUCK" in signal_codes
    ):
        return "CRITICAL"

    if "BLOCKING_OTHERS" in signal_codes or "STUCK" in signal_codes:
        return "HIGH"

    if signal_codes.intersection(
        {
            "BLOCKED",
            "OVERDUE",
            "STALE",
            "NEAR_DUE",
            "PARENT_DONE_CHILD_OPEN",
            "DEPENDENCY_NEEDS_VERIFICATION",
            "STALE_DEPENDENCY_CANDIDATE",
        }
    ):
        return "MEDIUM"

    return "LOW"


def risk_reasons(signal_codes: set[str]) -> list[str]:
    return [code for code in RISK_REASON_ORDER if code in signal_codes]


def risk_pressure_score(signal_codes: set[str]) -> int:
    return sum(
        weight
        for code, weight in RISK_PRESSURE_WEIGHTS.items()
        if code in signal_codes
    )


def max_risk_level(*levels: str) -> str:
    return max(levels, key=lambda level: RISK_LEVEL_ORDER.get(level, 0))
