from __future__ import annotations

import json
import os

from app.domain.models import ProjectState
from app.intelligence.change_summary import build_change_summary, compact_count_lines
from app.intelligence.dependency_clusters import build_dependency_clusters
from app.intelligence.hotspots import ProjectHotspots
from app.intelligence.management_leverage import build_management_leverage
from app.memory.delta import ProjectDelta

DONE_STATUSES = {"done", "closed", "resolved"}


def _is_done(status: str | None) -> bool:
    return (status or "").strip().lower() in DONE_STATUSES


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def _signal_codes(state) -> set[str]:
    return {s.code for s in state.signals if s.code}


def _effective_dependencies(state, states: dict) -> list[dict]:
    """Return only dependencies that are active in the current delivery state."""
    if _is_done(state.issue.status):
        return []
    codes = _signal_codes(state)
    result = []
    for dep in state.issue.dependencies or []:
        related = states.get(dep.related_issue_key)
        if not related or _is_done(related.issue.status):
            continue
        relation = (dep.relation or "").strip().lower()
        active = (
            (relation == "blocks" and "BLOCKING_OTHERS" in codes)
            or ("blocked by" in relation and "BLOCKED" in codes)
        )
        if active:
            result.append({
                "related_issue_key": dep.related_issue_key,
                "relation": dep.relation,
                "direction": dep.direction,
            })
    return result


def _dependency_hygiene(state, states: dict) -> list[dict]:
    codes = _signal_codes(state)
    if not (codes & {"DEPENDENCY_NEEDS_VERIFICATION", "STALE_DEPENDENCY_CANDIDATE"}):
        return []
    return [
        {
            "related_issue_key": dep.related_issue_key,
            "relation": dep.relation,
            "direction": dep.direction,
        }
        for dep in state.issue.dependencies or []
        if dep.related_issue_key in states
    ]


def build_ai_context(
    project_state: ProjectState,
    delta: ProjectDelta,
    hotspots: ProjectHotspots | None = None,
    risk_intelligence=None,
) -> str:
    """Build an AI-first PM context with deterministic facts and advisory hints.

    Design goals:
    - Give the model broad board awareness with a lightweight row for most/all
      issues, so it can discover owner concentration, related risk patterns and
      cross-board themes that a hard-coded top-N selector may miss.
    - Give richer detail only for delivery-relevant issues to control token use.
    - Keep Jira facts/effective dependencies authoritative.
    - Keep deterministic hotspot/pressure/escalation outputs as *advisory
      heuristics*, not conclusions the model must repeat.
    """
    max_detailed = max(8, _int_env("AI_CONTEXT_MAX_ISSUES", 24))
    max_board = max(max_detailed, _int_env("AI_CONTEXT_BOARD_MAX_ISSUES", 100))
    max_hotspots = max(4, _int_env("AI_CONTEXT_MAX_HOTSPOTS", 10))
    max_clusters = max(3, _int_env("AI_CONTEXT_MAX_CLUSTERS", 6))
    max_deltas = max(4, _int_env("AI_CONTEXT_MAX_DELTAS", 12))
    max_escalations = max(3, _int_env("AI_CONTEXT_MAX_ESCALATIONS", 8))
    max_chars = max(10000, _int_env("AI_CONTEXT_MAX_CHARS", 16000))

    states = {s.issue.key: s for s in project_state.issues}
    selected: list[str] = []

    def add(key: str | None) -> None:
        if key and key in states and key not in selected:
            selected.append(key)

    # Deterministic heuristics are useful for recall, but they do not own the
    # final PM judgment. Use them to decide which issues deserve *detail*.
    for h in (hotspots.items[:max_hotspots] if hotspots else []):
        add(h.issue_key)

    leverage = build_management_leverage(risk_intelligence)
    for item in leverage[:max_hotspots]:
        add(item.issue_key)

    if risk_intelligence is not None:
        for item in risk_intelligence.escalation_candidates[:max_escalations]:
            add(item.issue_key)
            for key in item.direct_downstream + item.propagated_downstream:
                add(key)

    clusters = build_dependency_clusters(risk_intelligence)[:max_clusters]
    for cluster in clusters:
        add(cluster.root_issue_key)
        for key in cluster.affected_issue_keys:
            add(key)

    material_delta = []
    for event in delta.events:
        if event.category == "ongoing":
            continue
        material_delta.append({
            "code": event.code,
            "issue_key": event.issue_key,
            "severity": event.severity,
            "category": event.category,
            "metadata": event.metadata,
        })
        add(event.issue_key)
        if len(material_delta) >= max_deltas:
            break

    # Any issue with a concrete current delivery signal deserves detail before
    # plain healthy/backlog issues.
    for state in project_state.issues:
        if _signal_codes(state):
            add(state.issue.key)

    selected = selected[:max_detailed]

    def detailed_issue_payload(key: str) -> dict:
        state = states[key]
        issue = state.issue
        return {
            "key": issue.key,
            "summary": issue.summary,
            "status": issue.status,
            "assignee": issue.assignee,
            "issue_type": issue.issue_type,
            "due_date": issue.due_date,
            "parent_key": issue.parent_key,
            "metrics": {
                "days_in_status": state.metrics.days_in_status,
                "days_since_update": state.metrics.days_since_update,
                "days_to_due": state.metrics.days_to_due,
            },
            "signals": sorted(_signal_codes(state)),
            "active_dependencies": _effective_dependencies(state, states),
            "dependency_hygiene": _dependency_hygiene(state, states),
        }

    # Broad but cheap board awareness. This deliberately avoids summaries,
    # historical details and raw dependency links.
    board_overview = []
    for state in project_state.issues[:max_board]:
        issue = state.issue
        board_overview.append({
            "key": issue.key,
            "status": issue.status,
            "assignee": issue.assignee,
            "days_to_due": state.metrics.days_to_due,
            "signals": sorted(_signal_codes(state)),
        })

    metrics = project_state.metrics
    project_metrics = None if metrics is None else {
        "total_issues": metrics.total_issues,
        "active_issues": metrics.active_issues,
        "done_issues": metrics.done_issues,
        "overdue_issues": metrics.overdue_issues,
        "near_due_issues": metrics.near_due_issues,
        "stale_issues": metrics.stale_issues,
        "stuck_issues": metrics.stuck_issues,
        "unassigned_open_issues": metrics.unassigned_issues,
        "blocked_issues": metrics.blocked_issues,
        "blocking_issues": metrics.blocking_issues,
        "hierarchy_mismatches": metrics.hierarchy_mismatches,
        "dependencies_to_verify": metrics.dependencies_to_verify,
    }

    risk_by_key = {
        item.issue_key: item for item in (risk_intelligence.items if risk_intelligence else [])
    }
    lifecycle_facts = []
    for key in selected:
        item = risk_by_key.get(key)
        if not item or item.current_score <= 0:
            continue
        lifecycle_facts.append({
            "issue_key": key,
            "risk_age_days": item.risk_age_days,
            "overdue_age_days": item.overdue_age_days,
            "blocker_observed_age_days": item.blocker_observed_age_days,
            "direct_downstream": item.direct_downstream,
            "propagated_downstream": item.propagated_downstream,
            # These are rule-engine hints, not AI conclusions.
            "heuristic_pressure": item.current_score,
            "previous_heuristic_pressure": item.previous_score,
            "heuristic_lifecycle_state": item.lifecycle_state,
        })

    change_summary = build_change_summary(delta, detail_limit=8, burst_threshold=20)
    context = {
        "context_contract": {
            "jira_facts_are_authoritative": True,
            "active_dependencies_are_authoritative": True,
            "dependency_hygiene_is_not_active_blocking": True,
            "deterministic_hints_are_advisory_only": True,
            "ai_owns_health_severity_priority_escalation_and_actions": True,
        },
        "project_key": project_state.project_key,
        "project_metrics": project_metrics,
        "board_overview": board_overview,
        "detailed_issue_facts": [detailed_issue_payload(k) for k in selected],
        "active_dependency_clusters": [
            {
                "root_issue_key": c.root_issue_key,
                "direct_downstream": c.direct_downstream,
                "propagated_downstream": c.propagated_downstream,
                "affected_issue_keys": c.affected_issue_keys,
                "max_depth": c.max_depth,
            }
            for c in clusters
        ],
        "lifecycle_facts": lifecycle_facts,
        "material_final_state_changes": material_delta,
        "change_volume": {
            "mode": change_summary.mode,
            "material_events": change_summary.material_events,
            "summary": compact_count_lines(change_summary),
        },
        "deterministic_hints": {
            "project_pressure": None if risk_intelligence is None else {
                "previous": risk_intelligence.previous_project_score,
                "current": risk_intelligence.project_score,
                "trend": risk_intelligence.project_trend,
            },
            "hotspots": [
                {
                    "issue_key": h.issue_key,
                    "heuristic_pressure": h.score,
                    "heuristic_level": h.level,
                    "reasons": h.reasons,
                }
                for h in (hotspots.items[:max_hotspots] if hotspots else [])
            ],
            "management_leverage": [
                {"issue_key": x.issue_key, "score": x.score, "reasons": x.reasons}
                for x in leverage[:max_hotspots]
            ],
            "rule_escalation_candidates": [
                {
                    "issue_key": x.issue_key,
                    "reasons": x.escalation_reasons,
                }
                for x in (
                    risk_intelligence.escalation_candidates[:max_escalations]
                    if risk_intelligence is not None else []
                )
            ],
        },
        "coverage": {
            "board_issue_rows": len(board_overview),
            "detailed_issue_rows": len(selected),
            "total_project_issues": len(project_state.issues),
        },
    }

    # Hard JSON-safe budget. Preserve board breadth as long as possible, then
    # reduce low-ranked detail. Never truncate JSON text mid-object.
    while True:
        text = json.dumps(context, ensure_ascii=False, separators=(",", ":"), default=str)
        if len(text) <= max_chars:
            return text
        if len(context["detailed_issue_facts"]) > 10:
            context["detailed_issue_facts"].pop()
            context["coverage"]["detailed_issue_rows"] -= 1
            continue
        if len(context["board_overview"]) > 30:
            context["board_overview"].pop()
            context["coverage"]["board_issue_rows"] -= 1
            continue
        # Last-resort: remove advisory hints before factual data.
        hints = context.get("deterministic_hints", {})
        if hints.get("hotspots"):
            hints["hotspots"] = []
            hints["management_leverage"] = []
            hints["rule_escalation_candidates"] = []
            continue
        return text
