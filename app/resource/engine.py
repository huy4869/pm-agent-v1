from __future__ import annotations

import json
import os
from pathlib import Path

from app.domain.models import ProjectState
from app.resource.models import ResourceProfile

DONE = {"done", "closed", "resolved", "cancelled", "canceled"}


def load_profiles(path: str | None = None) -> list[ResourceProfile]:
    profile_path = Path(path or os.getenv("RESOURCE_PROFILE_FILE", "data/resources.json"))
    if not profile_path.exists():
        return []
    raw = json.loads(profile_path.read_text(encoding="utf-8"))
    items = raw.get("resources", []) if isinstance(raw, dict) else raw
    return [ResourceProfile(**item) for item in items]


def describe_member(state: ProjectState, query: str) -> str | None:
    owners = sorted(
        {item.issue.assignee for item in state.issues if item.issue.assignee},
        key=len,
        reverse=True,
    )
    target = next((owner for owner in owners if owner.lower() in query.lower()), None)
    if not target:
        return None
    active = [
        item for item in state.issues
        if item.issue.assignee == target and item.issue.status.lower() not in DONE
    ]
    lines = [f"👤 <b>{target}</b> — {len(active)} task active"]
    for item in active[:8]:
        due = f" · due {item.issue.due_date}" if item.issue.due_date else ""
        lines.append(
            f"• <b>{item.issue.key}</b> — {item.issue.status}{due} — {item.issue.summary}"
        )
    return "\n".join(lines)
