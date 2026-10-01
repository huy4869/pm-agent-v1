from app.domain.models import IssueDependency, ProjectIssue, StatusChange


def issue_key(issue_id: int | str) -> str:
    return f"RM-{issue_id}"


def normalize_issue(issue: dict) -> ProjectIssue:
    status = issue.get("status") or {}
    assignee = issue.get("assigned_to") or {}
    priority = issue.get("priority") or {}
    tracker = issue.get("tracker") or {}
    parent = issue.get("parent") or {}
    fixed_version = issue.get("fixed_version") or {}
    issue_id = issue["id"]
    return ProjectIssue(
        key=issue_key(issue_id),
        summary=issue.get("subject", ""),
        status="Closed" if status.get("is_closed") else status.get("name", "Unknown"),
        assignee=assignee.get("name"),
        priority=priority.get("name"),
        issue_type=tracker.get("name"),
        created_at=issue.get("created_on"),
        updated_at=issue.get("updated_on"),
        due_date=issue.get("due_date"),
        parent_key=issue_key(parent["id"]) if parent.get("id") is not None else None,
        dependencies=normalize_relations(issue_id, issue.get("relations", [])),
        fixed_version_id=str(fixed_version.get("id")) if fixed_version.get("id") is not None else None,
        fixed_version_name=fixed_version.get("name"),
        done_ratio=issue.get("done_ratio"),
        source="redmine",
    )


def normalize_relations(current_id: int | str, relations: list[dict]) -> list[IssueDependency]:
    current_id = str(current_id)
    result: list[IssueDependency] = []
    inverse = {
        "blocks": "blocked by", "blocked": "blocks",
        "precedes": "follows", "follows": "precedes",
        "duplicates": "duplicated by", "duplicated": "duplicates",
        "copied_to": "copied from", "copied_from": "copied to",
    }
    labels = {
        "blocked": "blocked by", "copied_to": "copied to",
        "copied_from": "copied from",
    }
    for relation in relations:
        source_id = str(relation.get("issue_id"))
        target_id = str(relation.get("issue_to_id"))
        relation_type = relation.get("relation_type", "relates")
        if current_id == source_id:
            related_id = target_id
            label = labels.get(relation_type, relation_type)
            direction = "outward"
        elif current_id == target_id:
            related_id = source_id
            label = inverse.get(relation_type, relation_type)
            direction = "inward"
        else:
            continue
        result.append(IssueDependency(
            issue_key=issue_key(current_id),
            related_issue_key=issue_key(related_id),
            relation=label,
            direction=direction,
        ))
    return result


def normalize_status_history(
    issue: dict,
    status_names: dict[str, str] | None = None,
) -> list[StatusChange]:
    status_names = status_names or {}
    changes: list[StatusChange] = []
    for journal in issue.get("journals", []):
        for detail in journal.get("details", []):
            if detail.get("property") != "attr" or detail.get("name") != "status_id":
                continue
            # Redmine journals expose status IDs. Newer servers may additionally
            # expose human-readable values; fall back to IDs without inventing names.
            old_id = detail.get("old_value")
            new_id = detail.get("new_value")
            old_value = detail.get("old_value_name") or status_names.get(str(old_id), old_id)
            new_value = detail.get("new_value_name") or status_names.get(str(new_id), new_id)
            if new_value and old_value != new_value:
                changes.append(StatusChange(
                    from_status=str(old_value) if old_value is not None else None,
                    to_status=str(new_value),
                    changed_at=journal.get("created_on"),
                ))
    return changes
