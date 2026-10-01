from app.domain.models import (
    IssueDependency,
    ProjectIssue,
    StatusChange,
)


def normalize_issue(issue: dict) -> ProjectIssue:
    fields = issue["fields"]

    status = fields.get("status")
    assignee = fields.get("assignee")
    priority = fields.get("priority")
    issue_type = fields.get("issuetype")
    parent = fields.get("parent")
    issue_links = fields.get("issuelinks", [])

    return ProjectIssue(
        key=issue["key"],
        summary=fields.get("summary", ""),
        status=status.get("name") if status else "Unknown",
        assignee=assignee.get("displayName") if assignee else None,
        priority=priority.get("name") if priority else None,
        issue_type=issue_type.get("name") if issue_type else None,
        created_at=fields.get("created"),
        updated_at=fields.get("updated"),
        due_date=fields.get("duedate"),
        parent_key=parent.get("key") if parent else None,
        dependencies=normalize_issue_links(
            issue["key"],
            issue_links,
        ),
    )


def normalize_issues(
    issues: list[dict],
) -> list[ProjectIssue]:
    return [
        normalize_issue(issue)
        for issue in issues
    ]


def normalize_status_history(
    changelogs: list[dict],
) -> list[StatusChange]:
    status_changes: list[StatusChange] = []

    for changelog in changelogs:
        changed_at = changelog.get("created")

        for item in changelog.get("items", []):
            if item.get("field") != "status":
                continue

            from_status = item.get("fromString")
            to_status = item.get("toString")

            if not to_status:
                continue

            if from_status == to_status:
                continue

            status_changes.append(
                StatusChange(
                    from_status=from_status,
                    to_status=to_status,
                    changed_at=changed_at,
                )
            )

    return status_changes


def get_status_since(
    issue: ProjectIssue,
    status_history: list[StatusChange],
) -> str | None:
    matching_changes = [
        change
        for change in status_history
        if change.to_status == issue.status
    ]

    if matching_changes:
        return matching_changes[-1].changed_at

    return issue.created_at


def normalize_issue_links(
    issue_key: str,
    issue_links: list[dict],
) -> list[IssueDependency]:
    dependencies: list[IssueDependency] = []

    for link in issue_links:
        link_type = link.get("type", {})

        inward_issue = link.get("inwardIssue")
        outward_issue = link.get("outwardIssue")

        if inward_issue:
            dependencies.append(
                IssueDependency(
                    issue_key=issue_key,
                    related_issue_key=inward_issue["key"],
                    relation=link_type.get(
                        "inward",
                        "related to",
                    ),
                    direction="inward",
                )
            )

        if outward_issue:
            dependencies.append(
                IssueDependency(
                    issue_key=issue_key,
                    related_issue_key=outward_issue["key"],
                    relation=link_type.get(
                        "outward",
                        "related to",
                    ),
                    direction="outward",
                )
            )

    return dependencies