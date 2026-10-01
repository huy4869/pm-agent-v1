"""Synchronize only BA/DEV/TEST start and due dates for the BCY scope."""

from __future__ import annotations

from setup_ngoai_giao_scope import SCOPE, TASK_SUBJECT_OVERRIDES
from setup_redmine_spmm_hierarchy import (
    EPIC_SUBJECT,
    FEATURE_ID,
    find_issue,
    get_issue,
    request,
)


BASE_DATES = {
    "BA": (None, "2026-08-19"),
    "DEV": ("2026-08-19", "2026-08-25"),
    "TEST": ("2026-08-26", None),
}


def update_dates(issue_id: int, start: str | None, due: str | None) -> dict:
    fields = {}
    if start is not None:
        fields["start_date"] = start
    if due is not None:
        fields["due_date"] = due
    if not fields:
        return get_issue(issue_id)
    request(
        "PUT",
        f"/issues/{issue_id}.json",
        json={"issue": fields},
    )
    issue = get_issue(issue_id)
    if (
        start is not None and issue.get("start_date") != start
    ) or (
        due is not None and issue.get("due_date") != due
    ):
        raise RuntimeError(
            f"#{issue_id}: expected dates {(start, due)}, got "
            f"{(issue.get('start_date'), issue.get('due_date'))}"
        )
    return issue


def main() -> None:
    epic = find_issue(EPIC_SUBJECT)
    if not epic:
        raise RuntimeError(f"Epic not found: {EPIC_SUBJECT}")
    epic_id = int(epic["id"])
    updated: list[dict] = []

    for phase, (start, due) in BASE_DATES.items():
        task = find_issue(f"{phase} - Phiếu đề nghị SPMM", FEATURE_ID)
        if not task:
            raise RuntimeError(f"Missing task: {phase} - Phiếu đề nghị SPMM")
        updated.append(update_dates(int(task["id"]), start, due))

    for item in SCOPE:
        feature = find_issue(str(item["subject"]), epic_id)
        if not feature:
            raise RuntimeError(f"Missing Feature: {item['subject']}")
        feature_id = int(feature["id"])
        for phase, key in (("BA", "ba"), ("DEV", "dev"), ("TEST", "test")):
            task_subject = TASK_SUBJECT_OVERRIDES.get(
                (phase, str(item["subject"])), f"{phase} - {item['subject']}"
            )
            task = find_issue(task_subject, feature_id)
            if not task:
                continue
            data = item[key]
            updated.append(
                update_dates(int(task["id"]), data.get("start"), data.get("due"))
            )

    print(f"Synchronized dates for {len(updated)} tasks.")


if __name__ == "__main__":
    main()
