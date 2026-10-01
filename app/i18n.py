from __future__ import annotations

import os


def report_language() -> str:
    value = os.getenv("REPORT_LANGUAGE", "vi").strip().lower()
    return "en" if value.startswith("en") else "vi"


def is_vi() -> bool:
    return report_language() == "vi"


def health_label(value: str) -> str:
    # Domain enum: stable across report languages.
    return (value or "WATCH").upper()


def risk_label(value: str) -> str:
    # Domain enum: stable across report languages.
    return (value or "MEDIUM").upper()


def trend_label(value: str) -> str:
    value = (value or "STABLE").upper()
    if not is_vi():
        return value.lower()
    return {
        "UP": "tăng",
        "DOWN": "giảm",
        "STABLE": "ổn định",
        "BASELINE": "mốc ban đầu",
    }.get(value, value.lower())
