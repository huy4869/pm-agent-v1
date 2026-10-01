from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ============================================================
# DOMAIN CONSTANTS
# ============================================================

DONE_STATUSES = {
    "done",
    "closed",
    "resolved",
}

TODO_STATUSES = {
    "to do",
    "todo",
    "backlog",
    "open",
    "idea",
}

ACTIVE_STATUSES = {
    "in progress",
    "in review",
    "review",
    "testing",
    "qa",
    "ready for review",
}

BLOCKING_SIGNAL = "BLOCKING_OTHERS"

DEFAULT_NO_PROGRESS_DAYS = 3.0


# ============================================================
# MODELS
# ============================================================

@dataclass
class DeltaEvent:
    code: str
    message: str
    issue_key: str | None = None
    severity: str = "info"

    # progress | direct | impact | ongoing | resolved
    category: str = "direct"

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ProjectDelta:
    baseline_created: bool = False
    events: list[DeltaEvent] = field(
        default_factory=list
    )


# ============================================================
# PUBLIC API
# ============================================================

def calculate_project_delta(
    previous_snapshot: dict | None,
    current_snapshot: dict,
    *,
    no_progress_days: float = (
        DEFAULT_NO_PROGRESS_DAYS
    ),
) -> ProjectDelta:
    delta = ProjectDelta()

    if previous_snapshot is None:
        delta.baseline_created = True
        return delta

    previous_issues = previous_snapshot.get(
        "issues",
        {},
    )

    current_issues = current_snapshot.get(
        "issues",
        {},
    )

    previous_keys = set(
        previous_issues.keys()
    )

    current_keys = set(
        current_issues.keys()
    )

    # ========================================================
    # ISSUE ADDED
    # ========================================================

    for issue_key in sorted(
        current_keys - previous_keys
    ):
        delta.events.append(
            DeltaEvent(
                code="ISSUE_ADDED",
                issue_key=issue_key,
                category="direct",
                message=(
                    f"{issue_key}: "
                    "new issue added"
                ),
            )
        )

    # ========================================================
    # ISSUE REMOVED
    # ========================================================

    for issue_key in sorted(
        previous_keys - current_keys
    ):
        delta.events.append(
            DeltaEvent(
                code="ISSUE_REMOVED",
                issue_key=issue_key,
                category="direct",
                message=(
                    f"{issue_key}: "
                    "issue removed from project"
                ),
            )
        )

    # ========================================================
    # EXISTING ISSUES
    # ========================================================

    for issue_key in sorted(
        previous_keys & current_keys
    ):
        previous_issue = previous_issues[
            issue_key
        ]

        current_issue = current_issues[
            issue_key
        ]

        _compare_status(
            delta,
            issue_key,
            previous_issue,
            current_issue,
        )

        _compare_assignee(
            delta,
            issue_key,
            previous_issue,
            current_issue,
        )

        _compare_due_date(
            delta,
            issue_key,
            previous_issue,
            current_issue,
        )

        _compare_dependencies(
            delta,
            issue_key,
            previous_issue,
            current_issue,
        )

        _compare_signals(
            delta,
            issue_key,
            previous_issue,
            current_issue,
        )

        _detect_persistent_blocker(
            delta,
            issue_key,
            previous_issue,
            current_issue,
        )

        _detect_no_progress(
            delta,
            issue_key,
            previous_issue,
            current_issue,
            no_progress_days=no_progress_days,
        )

    _sort_events(delta)

    return delta


# ============================================================
# STATUS
# ============================================================

def _compare_status(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
) -> None:
    old_status = previous_issue.get(
        "status"
    )

    new_status = current_issue.get(
        "status"
    )

    if old_status == new_status:
        return

    old_normalized = _normalize_status(
        old_status
    )

    new_normalized = _normalize_status(
        new_status
    )

    # --------------------------------------------------------
    # Newly completed
    # --------------------------------------------------------

    if (
        new_normalized in DONE_STATUSES
        and old_normalized not in DONE_STATUSES
    ):
        delta.events.append(
            DeltaEvent(
                code="NEWLY_DONE",
                issue_key=issue_key,
                category="progress",
                message=(
                    f"{issue_key}: "
                    f"{old_status} → {new_status}"
                ),
                metadata={
                    "old_status": old_status,
                    "new_status": new_status,
                },
            )
        )

        return

    # --------------------------------------------------------
    # Reopened
    # --------------------------------------------------------

    if (
        old_normalized in DONE_STATUSES
        and new_normalized not in DONE_STATUSES
    ):
        delta.events.append(
            DeltaEvent(
                code="ISSUE_REOPENED",
                issue_key=issue_key,
                severity="warning",
                category="impact",
                message=(
                    f"{issue_key}: "
                    f"{old_status} → {new_status}"
                ),
                metadata={
                    "old_status": old_status,
                    "new_status": new_status,
                },
            )
        )

        return

    # --------------------------------------------------------
    # Work started / meaningful forward movement
    # --------------------------------------------------------

    if (
        old_normalized in TODO_STATUSES
        and new_normalized
        in ACTIVE_STATUSES
    ):
        delta.events.append(
            DeltaEvent(
                code="WORK_STARTED",
                issue_key=issue_key,
                category="progress",
                message=(
                    f"{issue_key}: "
                    f"{old_status} → {new_status}"
                ),
                metadata={
                    "old_status": old_status,
                    "new_status": new_status,
                },
            )
        )

        return

    # --------------------------------------------------------
    # Other status changes
    # --------------------------------------------------------

    delta.events.append(
        DeltaEvent(
            code="STATUS_CHANGED",
            issue_key=issue_key,
            category="direct",
            message=(
                f"{issue_key}: "
                f"{old_status} → {new_status}"
            ),
            metadata={
                "old_status": old_status,
                "new_status": new_status,
            },
        )
    )


# ============================================================
# ASSIGNEE
# ============================================================

def _compare_assignee(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
) -> None:
    old_assignee = previous_issue.get(
        "assignee"
    )

    new_assignee = current_issue.get(
        "assignee"
    )

    if old_assignee == new_assignee:
        return

    old_display = (
        old_assignee
        if old_assignee
        else "Unassigned"
    )

    new_display = (
        new_assignee
        if new_assignee
        else "Unassigned"
    )

    category = "direct"
    severity = "info"

    if (
        old_assignee
        and not new_assignee
    ):
        category = "impact"
        severity = "warning"

    delta.events.append(
        DeltaEvent(
            code="ASSIGNEE_CHANGED",
            issue_key=issue_key,
            category=category,
            severity=severity,
            message=(
                f"{issue_key}: assignee "
                f"{old_display} → "
                f"{new_display}"
            ),
            metadata={
                "old_assignee": old_assignee,
                "new_assignee": new_assignee,
            },
        )
    )


# ============================================================
# DUE DATE
# ============================================================

def _compare_due_date(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
) -> None:
    old_due = previous_issue.get(
        "due_date"
    )

    new_due = current_issue.get(
        "due_date"
    )

    if old_due == new_due:
        return

    old_display = (
        old_due
        if old_due
        else "None"
    )

    new_display = (
        new_due
        if new_due
        else "None"
    )

    category = "direct"
    severity = "info"

    old_date = _parse_datetime(
        old_due
    )

    new_date = _parse_datetime(
        new_due
    )

    # Due date moved later
    if (
        old_date is not None
        and new_date is not None
        and new_date > old_date
    ):
        category = "impact"
        severity = "warning"

    # Due date removed
    elif (
        old_due
        and not new_due
    ):
        category = "impact"
        severity = "warning"

    delta.events.append(
        DeltaEvent(
            code="DUE_DATE_CHANGED",
            issue_key=issue_key,
            category=category,
            severity=severity,
            message=(
                f"{issue_key}: due date "
                f"{old_display} → "
                f"{new_display}"
            ),
            metadata={
                "old_due_date": old_due,
                "new_due_date": new_due,
            },
        )
    )


# ============================================================
# DEPENDENCIES
# ============================================================

def _dependency_key(
    dependency: dict,
) -> tuple:
    return (
        dependency.get(
            "related_issue_key"
        ),
        dependency.get(
            "relation"
        ),
        dependency.get(
            "direction"
        ),
    )


def _compare_dependencies(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
) -> None:
    previous_dependencies = {
        _dependency_key(dependency)
        for dependency
        in previous_issue.get(
            "dependencies",
            [],
        )
    }

    current_dependencies = {
        _dependency_key(dependency)
        for dependency
        in current_issue.get(
            "dependencies",
            [],
        )
    }

    added = (
        current_dependencies
        - previous_dependencies
    )

    removed = (
        previous_dependencies
        - current_dependencies
    )

    for dependency in sorted(
        added,
        key=_safe_dependency_sort_key,
    ):
        related, relation, direction = (
            dependency
        )

        category = "direct"
        severity = "info"

        if _is_blocking_relation(
            relation
        ):
            category = "impact"
            severity = "warning"

        delta.events.append(
            DeltaEvent(
                code="DEPENDENCY_ADDED",
                issue_key=issue_key,
                category=category,
                severity=severity,
                message=(
                    f"{issue_key}: "
                    f"{relation} {related} "
                    "dependency added"
                ),
                metadata={
                    "related_issue_key": related,
                    "relation": relation,
                    "direction": direction,
                },
            )
        )

    for dependency in sorted(
        removed,
        key=_safe_dependency_sort_key,
    ):
        related, relation, direction = (
            dependency
        )

        category = (
            "resolved"
            if _is_blocking_relation(
                relation
            )
            else "direct"
        )

        delta.events.append(
            DeltaEvent(
                code="DEPENDENCY_REMOVED",
                issue_key=issue_key,
                category=category,
                message=(
                    f"{issue_key}: "
                    f"{relation} {related} "
                    "dependency removed"
                ),
                metadata={
                    "related_issue_key": related,
                    "relation": relation,
                    "direction": direction,
                },
            )
        )


# ============================================================
# SIGNALS
# ============================================================

def _signal_codes(
    issue_snapshot: dict,
) -> set[str]:
    signals = issue_snapshot.get(
        "signals",
        [],
    )

    codes: set[str] = set()

    for signal in signals:
        if isinstance(signal, str):
            codes.add(signal)

        elif isinstance(signal, dict):
            code = signal.get(
                "code"
            )

            if code:
                codes.add(code)

    return codes


def _compare_signals(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
) -> None:
    previous_signals = _signal_codes(
        previous_issue
    )

    current_signals = _signal_codes(
        current_issue
    )

    new_signals = (
        current_signals
        - previous_signals
    )

    resolved_signals = (
        previous_signals
        - current_signals
    )

    for signal in sorted(
        new_signals
    ):
        delta.events.append(
            DeltaEvent(
                code="SIGNAL_ADDED",
                issue_key=issue_key,
                severity="warning",
                category="impact",
                message=(
                    f"{issue_key}: "
                    f"new signal {signal}"
                ),
                metadata={
                    "signal": signal,
                },
            )
        )

    for signal in sorted(
        resolved_signals
    ):
        delta.events.append(
            DeltaEvent(
                code="SIGNAL_RESOLVED",
                issue_key=issue_key,
                severity="info",
                category="resolved",
                message=(
                    f"{issue_key}: "
                    f"{signal} resolved"
                ),
                metadata={
                    "signal": signal,
                },
            )
        )


# ============================================================
# PERSISTENT BLOCKER
# ============================================================

def _detect_persistent_blocker(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
) -> None:
    previous_signals = _signal_codes(
        previous_issue
    )

    current_signals = _signal_codes(
        current_issue
    )

    if (
        BLOCKING_SIGNAL
        not in previous_signals
        or BLOCKING_SIGNAL
        not in current_signals
    ):
        return

    targets = _blocking_targets(
        current_issue
    )

    if not targets:
        return

    delta.events.append(
        DeltaEvent(
            code="PERSISTENT_BLOCKER",
            issue_key=issue_key,
            severity="warning",
            category="ongoing",
            message=(
                f"{issue_key}: still blocking "
                + ", ".join(targets)
            ),
            metadata={
                "targets": targets,
            },
        )
    )


# ============================================================
# NO PROGRESS
# ============================================================

def _detect_no_progress(
    delta: ProjectDelta,
    issue_key: str,
    previous_issue: dict,
    current_issue: dict,
    *,
    no_progress_days: float,
) -> None:
    """
    Detect work that remains open and has not
    meaningfully progressed for a configurable
    amount of time.

    This does not hard-code project/team rules.
    It uses snapshot timestamps/metrics when
    available.
    """

    current_status = _normalize_status(
        current_issue.get(
            "status"
        )
    )

    if current_status in DONE_STATUSES:
        return

    # A status change is already meaningful progress.
    if (
        previous_issue.get("status")
        != current_issue.get("status")
    ):
        return

    age_days = _extract_no_progress_days(
        current_issue
    )

    if age_days is None:
        return

    if age_days < no_progress_days:
        return

    signals = _signal_codes(
        current_issue
    )

    blocked = (
        "BLOCKED" in signals
        or BLOCKING_SIGNAL in signals
    )

    severity = (
        "warning"
        if blocked
        else "info"
    )

    delta.events.append(
        DeltaEvent(
            code="NO_PROGRESS",
            issue_key=issue_key,
            severity=severity,
            category="ongoing",
            message=(
                f"{issue_key}: no meaningful "
                f"progress for {age_days:.1f} days"
            ),
            metadata={
                "days": age_days,
                "status": current_issue.get(
                    "status"
                ),
                "blocked": blocked,
            },
        )
    )


# ============================================================
# HELPERS
# ============================================================

def _normalize_status(
    status: str | None,
) -> str:
    if not status:
        return ""

    return (
        str(status)
        .strip()
        .lower()
    )


def _is_blocking_relation(
    relation: str | None,
) -> bool:
    if not relation:
        return False

    normalized = (
        str(relation)
        .strip()
        .lower()
    )

    return normalized in {
        "blocks",
        "is blocked by",
        "blocked by",
    }


def _blocking_targets(
    issue_snapshot: dict,
) -> list[str]:
    targets: list[str] = []

    for dependency in issue_snapshot.get(
        "dependencies",
        [],
    ):
        relation = (
            dependency.get(
                "relation",
                "",
            )
            or ""
        ).strip().lower()

        direction = (
            dependency.get(
                "direction",
                "",
            )
            or ""
        ).strip().lower()

        # We only want issues this issue blocks.
        if relation != "blocks":
            continue

        # If direction exists, outward is the
        # blocking direction in the current model.
        if (
            direction
            and direction != "outward"
        ):
            continue

        related = dependency.get(
            "related_issue_key"
        )

        if related:
            targets.append(
                str(related)
            )

    return sorted(
        set(targets)
    )


def _extract_no_progress_days(
    issue_snapshot: dict,
) -> float | None:
    metrics = issue_snapshot.get(
        "metrics"
    )

    # ========================================================
    # BEST SOURCE:
    # days_since_update calculated by our metrics engine.
    # ========================================================

    if isinstance(
        metrics,
        dict,
    ):
        parsed = _to_float(
            metrics.get(
                "days_since_update"
            )
        )

        if parsed is not None:
            return parsed

    # ========================================================
    # BACKWARD / ALTERNATE SNAPSHOT FORMATS
    # ========================================================

    for key in (
        "days_since_update",
        "days_since_updated",
        "updated_days",
        "updated_age_days",
    ):
        parsed = _to_float(
            issue_snapshot.get(
                key
            )
        )

        if parsed is not None:
            return parsed

    # ========================================================
    # TIMESTAMP FALLBACK
    # ========================================================

    updated_at = (
        issue_snapshot.get(
            "updated_at"
        )
        or issue_snapshot.get(
            "updated"
        )
    )

    updated_dt = _parse_datetime(
        updated_at
    )

    if updated_dt is None:
        return None

    if updated_dt.tzinfo is None:
        updated_dt = (
            updated_dt.replace(
                tzinfo=timezone.utc
            )
        )

    now = datetime.now(
        timezone.utc
    )

    age = (
        now
        - updated_dt.astimezone(
            timezone.utc
        )
    )

    return max(
        0.0,
        age.total_seconds()
        / 86400.0,
    )


def _parse_datetime(
    value: Any,
) -> datetime | None:
    if not value:
        return None

    if isinstance(
        value,
        datetime,
    ):
        return value

    text = str(value).strip()

    if not text:
        return None

    try:
        parsed = datetime.fromisoformat(
            text.replace(
                "Z",
                "+00:00",
            )
        )

        return parsed

    except ValueError:
        pass

    try:
        return datetime.strptime(
            text,
            "%Y-%m-%d",
        ).replace(
            tzinfo=timezone.utc
        )

    except ValueError:
        return None


def _to_float(
    value: Any,
) -> float | None:
    if value is None:
        return None

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return None


def _safe_dependency_sort_key(
    dependency: tuple,
) -> tuple[str, str, str]:
    related, relation, direction = (
        dependency
    )

    return (
        str(related or ""),
        str(relation or ""),
        str(direction or ""),
    )


def _sort_events(
    delta: ProjectDelta,
) -> None:
    category_order = {
        "progress": 0,
        "impact": 1,
        "ongoing": 2,
        "direct": 3,
        "resolved": 4,
    }

    severity_order = {
        "critical": 0,
        "warning": 1,
        "info": 2,
    }

    delta.events.sort(
        key=lambda event: (
            category_order.get(
                event.category,
                99,
            ),
            severity_order.get(
                event.severity,
                99,
            ),
            event.issue_key or "",
            event.code,
        )
    )