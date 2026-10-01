from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env", override=True)

from app.redmine.client import RedmineClient  # noqa: E402


def _task_row(issue: dict) -> dict:
    status = issue.get("status") or {}
    return {
        "id": issue.get("id"),
        "tracker": (issue.get("tracker") or {}).get("name", "-"),
        "status": status.get("name", "Unknown"),
        "closed": bool(status.get("is_closed")),
        "priority": (issue.get("priority") or {}).get("name", "-"),
        "assignee": (issue.get("assigned_to") or {}).get("name", "Unassigned"),
        "due_date": issue.get("due_date") or "-",
        "subject": issue.get("subject", ""),
    }


def _print_table(rows: list[dict]) -> None:
    columns = (
        ("id", "ID", 7),
        ("tracker", "Type", 12),
        ("status", "Status", 18),
        ("priority", "Priority", 10),
        ("assignee", "Assignee", 22),
        ("due_date", "Due date", 10),
        ("subject", "Subject", 60),
    )

    def cell(value: object, width: int) -> str:
        text = str(value).replace("\n", " ")
        return text if len(text) <= width else text[: width - 1] + "…"

    print(" | ".join(cell(label, width).ljust(width) for _, label, width in columns))
    print("-+-".join("-" * width for _, _, width in columns))
    for row in rows:
        print(" | ".join(cell(row[key], width).ljust(width) for key, _, width in columns))


def main() -> None:
    parser = argparse.ArgumentParser(description="List and summarize Redmine tasks for BCY SPMM.")
    parser.add_argument("--all", action="store_true", help="Include closed tasks in the list.")
    parser.add_argument("--status", help="Only list tasks whose status contains this text.")
    parser.add_argument("--assignee", help="Only list tasks whose assignee contains this text.")
    parser.add_argument("--format", choices=("table", "json"), default="table")
    args = parser.parse_args()

    project_id = os.getenv("REDMINE_PROJECT_ID")
    if not project_id:
        raise SystemExit("Missing REDMINE_PROJECT_ID in .env")

    client = RedmineClient()
    rows = [_task_row(issue) for issue in client.list_project_issues(project_id)]
    status_counts = Counter(row["status"] for row in rows)
    open_count = sum(not row["closed"] for row in rows)
    closed_count = len(rows) - open_count
    open_rows = [row for row in rows if not row["closed"]]
    tracker_counts = Counter(row["tracker"] for row in open_rows)
    assignee_counts = Counter(row["assignee"] for row in open_rows)
    unassigned_count = assignee_counts.get("Unassigned", 0)
    today = date.today().isoformat()
    overdue_count = sum(row["due_date"] != "-" and row["due_date"] < today for row in open_rows)

    selected = rows if args.all else open_rows
    if args.status:
        selected = [row for row in selected if args.status.lower() in row["status"].lower()]
    if args.assignee:
        selected = [row for row in selected if args.assignee.lower() in row["assignee"].lower()]

    if args.format == "json":
        print(json.dumps({
            "project_id": project_id,
            "summary": {
                "total": len(rows),
                "open": open_count,
                "closed": closed_count,
                "by_status": dict(status_counts.most_common()),
                "open_by_tracker": dict(tracker_counts.most_common()),
                "open_by_assignee": dict(assignee_counts.most_common()),
                "unassigned": unassigned_count,
                "overdue": overdue_count,
            },
            "listed": len(selected),
            "tasks": selected,
        }, ensure_ascii=False, indent=2))
        return

    print(f"BCY SPMM (Redmine project {project_id})")
    print(f"Total: {len(rows)} | Open: {open_count} | Closed: {closed_count}")
    print("By status: " + ", ".join(f"{name}: {count}" for name, count in status_counts.most_common()))
    print("Open by type: " + ", ".join(f"{name}: {count}" for name, count in tracker_counts.most_common()))
    print(f"Unassigned: {unassigned_count} | Overdue: {overdue_count}")
    print("Open by assignee: " + ", ".join(f"{name}: {count}" for name, count in assignee_counts.most_common()))
    print(f"Listing: {len(selected)} {'all' if args.all else 'open'} task(s)\n")
    _print_table(selected)


if __name__ == "__main__":
    main()
