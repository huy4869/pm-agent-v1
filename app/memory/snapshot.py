from datetime import datetime, timezone
from typing import Any

from app.domain.models import ProjectState


# ============================================================
# SNAPSHOT SCHEMA
#
# v1:
# - issue basic fields
# - dependencies
# - signals
#
# v2:
# - updated_at
# - created_at
# - status_since
# - issue metrics
#
# Old v1 snapshots remain readable.
# ============================================================

SNAPSHOT_VERSION = 2


def build_project_snapshot(
    project_state: ProjectState,
) -> dict[str, Any]:
    issues: dict[str, dict[str, Any]] = {}

    for state in project_state.issues:
        issue = state.issue
        metrics = state.metrics

        # ====================================================
        # DEPENDENCIES
        # ====================================================

        dependencies: list[
            dict[str, Any]
        ] = []

        for dependency in (
            issue.dependencies or []
        ):
            dependencies.append(
                {
                    "related_issue_key": (
                        dependency.related_issue_key
                    ),
                    "relation": (
                        dependency.relation
                    ),
                    "direction": (
                        dependency.direction
                    ),
                }
            )

        # Deterministic snapshot output.
        dependencies.sort(
            key=lambda item: (
                item.get(
                    "related_issue_key",
                    "",
                )
                or "",
                item.get(
                    "relation",
                    "",
                )
                or "",
                item.get(
                    "direction",
                    "",
                )
                or "",
            )
        )

        # ====================================================
        # SIGNALS
        # ====================================================

        signal_codes = sorted(
            {
                signal.code
                for signal in state.signals
                if signal.code
            }
        )

        # ====================================================
        # ISSUE METRICS
        #
        # Keep calculated facts in the snapshot so the next
        # run can reason about movement without recalculating
        # historical state.
        # ====================================================

        issue_metrics = {
            "days_in_status": (
                metrics.days_in_status
            ),
            "days_since_update": (
                metrics.days_since_update
            ),
            "days_to_due": (
                metrics.days_to_due
            ),
        }

        # ====================================================
        # ISSUE SNAPSHOT
        # ====================================================

        issues[issue.key] = {
            "key": issue.key,
            "summary": issue.summary,
            "status": issue.status,
            "assignee": issue.assignee,
            "priority": issue.priority,
            "issue_type": issue.issue_type,

            # ----------------------------------------------
            # Dates / activity
            # ----------------------------------------------

            "created_at": (
                issue.created_at
            ),
            "updated_at": (
                issue.updated_at
            ),
            "status_since": (
                issue.status_since
            ),
            "due_date": (
                issue.due_date
            ),

            # ----------------------------------------------
            # Hierarchy
            # ----------------------------------------------

            "parent_key": (
                issue.parent_key
            ),

            # ----------------------------------------------
            # Calculated state
            # ----------------------------------------------

            "metrics": (
                issue_metrics
            ),

            # ----------------------------------------------
            # Relationships / signals
            # ----------------------------------------------

            "dependencies": (
                dependencies
            ),
            "signals": (
                signal_codes
            ),
        }

    # ========================================================
    # PROJECT SNAPSHOT
    # ========================================================

    return {
        "version": (
            SNAPSHOT_VERSION
        ),
        "project_key": (
            project_state.project_key
        ),
        "captured_at": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "issues": issues,
    }