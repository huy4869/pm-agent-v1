from app.domain.models import ProjectState
from app.reports.helpers import (
    blocking_targets,
    issue_ref,
    signal_codes,
    unique,
)


def build_actions_section(
    project_state: ProjectState,
) -> list[str]:
    lines = [
        "🎯 <b>PM Actions</b>"
    ]

    actions: list[str] = []

    _add_hierarchy_actions(
        actions,
        project_state,
    )

    _add_blocker_actions(
        actions,
        project_state,
    )

    _add_dependency_actions(
        actions,
        project_state,
    )

    _add_overdue_actions(
        actions,
        project_state,
    )

    _add_stale_actions(
        actions,
        project_state,
    )

    actions = unique(actions)

    if not actions:
        lines.append(
            "• No immediate PM action detected"
        )

    else:
        for index, action in enumerate(
            actions[:5],
            start=1,
        ):
            lines.append(
                f"{index}. {action}"
            )

    lines.append("")

    return lines


def _add_hierarchy_actions(
    actions: list[str],
    project_state: ProjectState,
) -> None:
    children = []

    for state in project_state.issues:
        if (
            "PARENT_DONE_CHILD_OPEN"
            in signal_codes(state)
        ):
            children.append(
                state.issue.key
            )

    if not children:
        return

    actions.append(
        "Verify/update status of "
        + ", ".join(
            issue_ref(key)
            for key in children
        )
        + " because their parent is already Done"
    )


def _add_blocker_actions(
    actions: list[str],
    project_state: ProjectState,
) -> None:
    for state in project_state.issues:
        issue = state.issue

        if (
            "BLOCKING_OTHERS"
            not in signal_codes(state)
        ):
            continue

        targets = blocking_targets(issue)

        if not targets:
            continue

        target_refs = ", ".join(
            issue_ref(key)
            for key in targets
        )

        if not issue.assignee:
            actions.append(
                f"Assign an owner to "
                f"{issue_ref(issue.key)}; "
                f"it currently blocks {target_refs}"
            )

        actions.append(
            f"Confirm ETA and unblock plan for "
            f"{issue_ref(issue.key)}; "
            f"downstream impact: {target_refs}"
        )


def _add_dependency_actions(
    actions: list[str],
    project_state: ProjectState,
) -> None:
    for state in project_state.issues:
        issue = state.issue

        if (
            "STALE_DEPENDENCY_CANDIDATE"
            not in signal_codes(state)
        ):
            continue

        targets = blocking_targets(issue)

        if not targets:
            continue

        actions.append(
            f"Verify {issue_ref(issue.key)} "
            "and clean up stale dependency links "
            "if the work is already complete"
        )

        if issue.parent_key:
            actions.append(
                f"If {issue_ref(issue.key)} "
                "is still open, verify whether parent "
                f"{issue_ref(issue.parent_key)} "
                "should remain Done"
            )


def _add_overdue_actions(
    actions: list[str],
    project_state: ProjectState,
) -> None:
    for state in project_state.issues:
        if (
            "OVERDUE"
            not in signal_codes(state)
        ):
            continue

        actions.append(
            "Confirm recovery plan and new ETA for "
            f"{issue_ref(state.issue.key)}"
        )


def _add_stale_actions(
    actions: list[str],
    project_state: ProjectState,
) -> None:
    stale = [
        state.issue.key
        for state in project_state.issues
        if "STALE" in signal_codes(state)
    ]

    if stale:
        actions.append(
            "Follow up stale active work: "
            + ", ".join(
                issue_ref(key)
                for key in stale
            )
        )