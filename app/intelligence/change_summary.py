from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from app.memory.delta import ProjectDelta


EVENT_WEIGHT = {
    "SIGNAL_ADDED": 7,
    "ISSUE_REOPENED": 7,
    "DEPENDENCY_ADDED": 6,
    "DEPENDENCY_REMOVED": 5,
    "DUE_DATE_CHANGED": 5,
    "ASSIGNEE_CHANGED": 4,
    "NEWLY_DONE": 4,
    "WORK_STARTED": 3,
    "STATUS_CHANGED": 3,
    "SIGNAL_RESOLVED": 3,
    "ISSUE_REMOVED": 2,
    "ISSUE_ADDED": 1,
    "PERSISTENT_BLOCKER": 1,
    "NO_PROGRESS": 1,
}


@dataclass(frozen=True)
class ChangeSummary:
    mode: str
    total_events: int
    material_events: int
    counts_by_code: dict[str, int] = field(default_factory=dict)
    top_events: list = field(default_factory=list)

    @property
    def is_burst(self) -> bool:
        return self.mode == "BURST"


def build_change_summary(
    delta: ProjectDelta,
    *,
    detail_limit: int = 5,
    burst_threshold: int = 20,
) -> ChangeSummary:
    if delta.baseline_created:
        return ChangeSummary("BASELINE", 0, 0, {}, [])

    # NO_PROGRESS and persistent blockers are ongoing state. They remain in the
    # audit log but do not inflate the perceived change volume.
    material = [
        event
        for event in delta.events
        if event.code not in {"NO_PROGRESS", "PERSISTENT_BLOCKER"}
    ]
    counts = Counter(event.code for event in material)

    if len(material) > burst_threshold:
        mode = "BURST"
    elif len(material) > detail_limit:
        mode = "SUMMARIZED"
    else:
        mode = "DETAILED"

    ranked = sorted(
        material,
        key=lambda e: (
            -EVENT_WEIGHT.get(e.code, 2),
            0 if e.severity == "warning" else 1,
            e.issue_key or "",
        ),
    )
    return ChangeSummary(
        mode=mode,
        total_events=len(delta.events),
        material_events=len(material),
        counts_by_code=dict(counts),
        top_events=ranked[:detail_limit],
    )


def compact_count_lines(summary: ChangeSummary) -> list[str]:
    if summary.mode == "BASELINE":
        return ["Baseline created — no previous snapshot"]
    if summary.material_events == 0:
        return ["No material delivery changes since previous run"]

    c = summary.counts_by_code
    lines = []
    added = c.get("ISSUE_ADDED", 0)
    removed = c.get("ISSUE_REMOVED", 0)
    status = c.get("STATUS_CHANGED", 0) + c.get("WORK_STARTED", 0) + c.get("NEWLY_DONE", 0) + c.get("ISSUE_REOPENED", 0)
    signals = c.get("SIGNAL_ADDED", 0)
    resolved = c.get("SIGNAL_RESOLVED", 0)
    dependency = c.get("DEPENDENCY_ADDED", 0) + c.get("DEPENDENCY_REMOVED", 0)
    assignment = c.get("ASSIGNEE_CHANGED", 0)
    due = c.get("DUE_DATE_CHANGED", 0)

    for count, text in (
        (added, "new issues added"),
        (removed, "issues removed"),
        (status, "status transitions"),
        (signals, "new delivery signals"),
        (resolved, "delivery signals resolved"),
        (dependency, "dependency changes"),
        (assignment, "assignee changes"),
        (due, "due-date changes"),
    ):
        if count:
            lines.append(f"{count} {text}")
    return lines or [f"{summary.material_events} material changes"]
