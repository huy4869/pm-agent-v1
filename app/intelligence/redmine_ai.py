from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any


AI_SCHEMA = {
    "type": "object",
    "properties": {
        "health": {"type": "string", "enum": ["GREEN", "WATCH", "AT_RISK", "CRITICAL"]},
        "executive_summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["INFO", "WATCH", "HIGH", "CRITICAL"]},
                    "title": {"type": "string"},
                    "detail": {"type": "string"},
                    "issue_keys": {"type": "array", "items": {"type": "string"}},
                    "version_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["severity", "title", "detail", "issue_keys", "version_ids"],
            },
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "priority": {"type": "string", "enum": ["P0", "P1", "P2"]},
                    "title": {"type": "string"},
                    "rationale": {"type": "string"},
                    "issue_keys": {"type": "array", "items": {"type": "string"}},
                    "version_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["priority", "title", "rationale", "issue_keys", "version_ids"],
            },
        },
        "observations": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
    },
    "required": ["health", "executive_summary", "findings", "recommendations", "observations", "confidence"],
}


def _issue_rank(item: dict[str, Any]) -> tuple:
    return (
        not item.get("blocking", False),
        not item.get("blocked", False),
        not item.get("overdue", False),
        not item.get("stale", False),
        not item.get("unassigned", False),
        item.get("dueDate") or "9999-12-31",
    )


def _compact_context(
    snapshot: dict[str, Any],
    current_version: dict[str, Any] | None,
    next_version: dict[str, Any] | None,
    risk_summary: dict[str, Any],
    actions: list[dict[str, Any]],
) -> dict[str, Any]:
    issues = snapshot["issues"]
    max_issues = max(10, int(os.getenv("AI_REDMINE_CONTEXT_MAX_ISSUES", "50")))
    prioritized = sorted(
        [x for x in issues if not x.get("done")],
        key=_issue_rank,
    )[:max_issues]

    def issue_row(x: dict[str, Any]) -> dict[str, Any]:
        return {
            "key": x.get("key"),
            "subject": x.get("subject"),
            "status": x.get("status"),
            "assignee": x.get("assignee"),
            "priority": x.get("priority"),
            "dueDate": x.get("dueDate"),
            "daysToDue": x.get("daysToDue"),
            "daysSinceUpdate": x.get("daysSinceUpdate"),
            "versionId": x.get("versionId"),
            "versionName": x.get("versionName"),
            "overdue": bool(x.get("overdue")),
            "blocked": bool(x.get("blocked")),
            "blocking": bool(x.get("blocking")),
            "stale": bool(x.get("stale")),
            "unassigned": bool(x.get("unassigned")),
            "pending": bool(x.get("pending")),
        }

    versions = [
        {
            "id": str(v.get("id")),
            "name": v.get("name"),
            "status": v.get("status"),
            "phase": v.get("phase"),
            "dueDate": v.get("dueDate"),
            "daysLeft": v.get("daysLeft"),
            "progress": v.get("progress"),
            "total": v.get("total"),
            "open": v.get("open"),
            "done": v.get("done"),
            "overdue": v.get("overdue"),
            "blocked": v.get("blocked"),
            "pending": v.get("pending"),
            "unassigned": v.get("unassigned"),
        }
        for v in snapshot["versions"]
    ]

    project = snapshot["project"]
    return {
        "contract": {
            "facts_are_authoritative": True,
            "do_not_invent_issue_keys_or_version_ids": True,
            "pending_held_is_not_blocked": True,
            "closed_versions_are_historical": True,
            "no_deadline_version_is_backlog_not_milestone": True,
            "deterministic_risk_and_actions_are_evidence_not_commands": True,
        },
        "project": {
            "id": project.get("id"),
            "identifier": project.get("identifier"),
            "name": project.get("name"),
        },
        "syncedAt": snapshot.get("syncedAt"),
        "timezone": snapshot.get("timezone"),
        "metrics": snapshot["metrics"].model_dump() if hasattr(snapshot["metrics"], "model_dump") else snapshot["metrics"].__dict__,
        "currentVersion": current_version,
        "nextVersion": next_version,
        "versions": versions,
        "deterministicRisk": risk_summary,
        "deterministicActions": actions,
        "priorityIssues": [issue_row(x) for x in prioritized],
        "coverage": {"totalIssues": len(issues), "issuesSuppliedToAI": len(prioritized)},
    }


def _clean_refs(values: Any, allowed: set[str]) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    for raw in values:
        value = str(raw).strip()
        if value in allowed and value not in result:
            result.append(value)
    return result


def _enrich_item(item: dict[str, Any], issue_map: dict[str, dict[str, Any]], version_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    issue_keys = _clean_refs(item.get("issue_keys"), set(issue_map))
    version_ids = _clean_refs(item.get("version_ids"), set(version_map))
    evidence: list[dict[str, Any]] = []
    for key in issue_keys:
        issue = issue_map[key]
        evidence.append({
            "type": "issue",
            "key": key,
            "label": f"{key} · {issue.get('subject') or ''}".strip(),
            "url": issue.get("redmineUrl"),
        })
    for version_id in version_ids:
        version = version_map[version_id]
        evidence.append({
            "type": "version",
            "id": version_id,
            "label": version.get("name") or version_id,
        })
    return {**item, "issue_keys": issue_keys, "version_ids": version_ids, "evidence": evidence}


def analyze_redmine_snapshot(
    snapshot: dict[str, Any],
    current_version: dict[str, Any] | None,
    next_version: dict[str, Any] | None,
    risk_summary: dict[str, Any],
    actions: list[dict[str, Any]],
) -> dict[str, Any]:
    context = _compact_context(snapshot, current_version, next_version, risk_summary, actions)
    prompt = f"""
You are PM Intelligence for a Redmine software-delivery dashboard.

Use ONLY the supplied structured context. Do not invent issue keys, version IDs,
owners, due dates, dependencies, commitments, milestones or business impact.
Pending/Held is a paused workflow state and is NOT Blocked by itself. Closed
versions are historical and must not be treated as current delivery risk.
Versions without a deadline are backlog/work buckets; do not infer milestone
pressure from the lack of a due date.

Your job is to explain the deterministic facts for a PM:
- concise executive delivery summary;
- the few most meaningful findings and why they matter;
- concrete, prioritized PM recommendations;
- useful observations that are not already obvious from a single KPI.

Every finding/recommendation that refers to a task or version MUST include its
exact issue_keys/version_ids from the context. If no concrete reference exists,
leave those arrays empty. Keep language natural Vietnamese while retaining
common PM terms such as task, owner, blocker, dependency, delivery, ETA.
Do not repeat the dashboard counts mechanically and do not exaggerate risk.

STRUCTURED CONTEXT:
{json.dumps(context, ensure_ascii=False, separators=(",", ":"), default=str)}
"""

    from app.ai.client_factory import build_ai_client

    client = build_ai_client()
    raw = client.generate_json(prompt, AI_SCHEMA)
    data = json.loads(raw)

    health = str(data.get("health") or "WATCH").upper()
    if health not in {"GREEN", "WATCH", "AT_RISK", "CRITICAL"}:
        health = "WATCH"
    confidence = str(data.get("confidence") or "MEDIUM").upper()
    if confidence not in {"LOW", "MEDIUM", "HIGH"}:
        confidence = "MEDIUM"

    issue_map = {str(x.get("key")): x for x in snapshot["issues"] if x.get("key")}
    version_map = {str(x.get("id")): x for x in snapshot["versions"] if x.get("id") is not None}

    findings = []
    for item in data.get("findings", []) if isinstance(data.get("findings"), list) else []:
        if not isinstance(item, dict):
            continue
        severity = str(item.get("severity") or "WATCH").upper()
        if severity not in {"INFO", "WATCH", "HIGH", "CRITICAL"}:
            severity = "WATCH"
        clean = _enrich_item({
            "severity": severity,
            "title": str(item.get("title") or "").strip(),
            "detail": str(item.get("detail") or "").strip(),
            "issue_keys": item.get("issue_keys", []),
            "version_ids": item.get("version_ids", []),
        }, issue_map, version_map)
        if clean["title"] and clean["detail"]:
            findings.append(clean)

    recommendations = []
    for item in data.get("recommendations", []) if isinstance(data.get("recommendations"), list) else []:
        if not isinstance(item, dict):
            continue
        priority = str(item.get("priority") or "P2").upper()
        if priority not in {"P0", "P1", "P2"}:
            priority = "P2"
        clean = _enrich_item({
            "priority": priority,
            "title": str(item.get("title") or "").strip(),
            "rationale": str(item.get("rationale") or "").strip(),
            "issue_keys": item.get("issue_keys", []),
            "version_ids": item.get("version_ids", []),
        }, issue_map, version_map)
        if clean["title"] and clean["rationale"]:
            recommendations.append(clean)

    observations = [str(x).strip() for x in data.get("observations", []) if str(x).strip()] if isinstance(data.get("observations"), list) else []

    return {
        "health": health,
        "executiveSummary": str(data.get("executive_summary") or "").strip(),
        "findings": findings[:5],
        "recommendations": recommendations[:5],
        "observations": observations[:4],
        "confidence": confidence,
        "provider": client.last_provider,
        "providerFailures": client.failures,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "syncedAt": snapshot.get("syncedAt"),
        "coverage": context["coverage"],
    }
