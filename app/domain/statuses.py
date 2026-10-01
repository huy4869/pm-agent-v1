from __future__ import annotations

DONE_STATUSES = {"Done", "Closed", "Resolved"}
ACTIVE_STATUSES = {"In Progress", "Doing", "In Review"}
PENDING_STATUSES = {"Held", "Pending", "On Hold", "On-Hold", "Paused", "Deferred"}


def normalize_status(value: str | None) -> str:
    return (value or "").strip().lower().replace("_", " ")


def is_done_status(value: str | None) -> bool:
    normalized = normalize_status(value)
    return any(normalized == item.lower() for item in DONE_STATUSES)


def is_active_status(value: str | None) -> bool:
    normalized = normalize_status(value)
    return any(normalized == item.lower() for item in ACTIVE_STATUSES)


def is_pending_status(value: str | None) -> bool:
    normalized = normalize_status(value)
    return any(normalized == item.lower() for item in PENDING_STATUSES)
