"""Data-driven BCY synchronization from a Google Sheet snapshot.

The input is JSON generated from the ``Thông tin chung`` sheet. The script:
- updates only status, start date, due date, assignee, and Done percentage;
- preserves Redmine values when a sheet cell is blank;
- never updates description or priority and never creates missing issues;
- cascades BA Pending to DEV/TEST Held;
- closes BA/DEV only when both are Done; TEST Done remains Resolved.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sync_task_schedule_status import all_project_issues, set_status
from setup_redmine_spmm_hierarchy import get_issue, request


DEFAULT_INPUT = Path(__file__).with_name("master_control_snapshot.json")

PIC_IDS = {
    "Quynhdtn17": 117,
    "Huongntm62": 119,
    "Anhdv76": 114,
    "Lampt45": 118,
    "Hanglt102": 115,
    "Anhnt634": None,
}

STATUS_IDS = {
    "to do": 1,
    "todo": 1,
    "doing": 2,
    "review": 4,
    "pending": 10,
}

SUBJECT_OVERRIDES = {
    ("BA", "Đơn vị và Đơn vị sản xuất"):
        "BA - Chỉnh sửa Master data Đơn vị sản xuất & Đơn vị",
}


def clean(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def iso_date(value: Any) -> str | None:
    value = clean(value)
    if not value:
        return None
    for pattern in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, pattern).date().isoformat()
        except ValueError:
            pass
    raise ValueError(f"Unsupported date: {value}")


def issue_subject(stage: str, feature: str) -> str:
    return SUBJECT_OVERRIDES.get((stage, feature), f"{stage} - {feature}")


def desired_status(stage: str, row: dict[str, Any]) -> int | None:
    ba_status = clean(row.get("ba", {}).get("status")).casefold()
    stage_status = clean(row.get(stage.casefold(), {}).get("status")).casefold()
    if stage in {"DEV", "TEST"} and ba_status == "pending":
        return 10
    if not stage_status:
        return None
    if stage_status == "done":
        dev_status = clean(row.get("dev", {}).get("status")).casefold()
        if stage in {"BA", "DEV"} and ba_status == "done" and dev_status == "done":
            return 5
        return 3
    if stage_status not in STATUS_IDS:
        raise ValueError(f"Unsupported status: {stage_status}")
    return STATUS_IDS[stage_status]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    issues = all_project_issues()
    by_subject = {clean(issue["subject"]): issue for issue in issues}
    changes = 0
    missing: list[str] = []
    unmapped: list[str] = []

    for row in rows:
        feature = clean(row.get("feature"))
        if not feature:
            continue
        for stage in ("BA", "DEV", "TEST"):
            source = row.get(stage.casefold(), {}) or {}
            subject = issue_subject(stage, feature)
            issue = by_subject.get(clean(subject))
            if not issue:
                if any(clean(source.get(key)) for key in ("pic", "start", "due", "status")):
                    missing.append(subject)
                continue

            fields: dict[str, Any] = {}
            start = iso_date(source.get("start"))
            due = iso_date(source.get("due"))
            pic = clean(source.get("pic"))
            if start:
                fields["start_date"] = start
            if due:
                fields["due_date"] = due
            if pic:
                user_id = PIC_IDS.get(pic)
                if user_id is None:
                    unmapped.append(f"{subject}: {pic}")
                else:
                    fields["assigned_to_id"] = user_id

            target_status = desired_status(stage, row)
            current_status = int(issue["status"]["id"])
            current_assignee = int(issue.get("assigned_to", {}).get("id", 0))
            field_changed = (
                (start and issue.get("start_date") != start)
                or (due and issue.get("due_date") != due)
                or (fields.get("assigned_to_id") and current_assignee != fields["assigned_to_id"])
            )
            status_changed = target_status is not None and current_status != target_status
            source_done = clean(source.get("status")).casefold() == "done"
            ratio_changed = source_done and int(issue.get("done_ratio", 0)) != 100

            if not (field_changed or status_changed or ratio_changed):
                continue
            print(
                f"{'APPLY' if args.apply else 'WOULD UPDATE'} #{issue['id']} | {subject} | "
                f"fields={fields or '-'} status={target_status or '-'} "
                f"done_ratio={100 if source_done else '-'}"
            )
            changes += 1
            if not args.apply:
                continue
            if fields:
                request("PUT", f"/issues/{issue['id']}.json", json={"issue": fields})
                issue = get_issue(int(issue["id"]))
            if target_status is not None:
                try:
                    issue = set_status(issue, target_status)
                except RuntimeError as error:
                    print(f"BLOCKED: {error}")
                    issue = get_issue(int(issue["id"]))
            if source_done and int(issue.get("done_ratio", 0)) != 100:
                request(
                    "PUT",
                    f"/issues/{issue['id']}.json",
                    json={"issue": {"done_ratio": 100}},
                )

    print(f"{'Applied' if args.apply else 'Planned'} changes for {changes} task(s).")
    if missing:
        print("Missing Redmine tasks:")
        for item in sorted(set(missing)):
            print(f"- {item}")
    if unmapped:
        print("Unmapped PIC values:")
        for item in sorted(set(unmapped)):
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
