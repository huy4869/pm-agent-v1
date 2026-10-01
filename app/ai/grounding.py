from __future__ import annotations

import re

from app.ai.models import ProjectAIAnalysis
from app.i18n import is_vi

DONE_STATUSES = {"done", "closed", "resolved"}
ISSUE_KEY_RE = re.compile(r"\b[A-Z][A-Z0-9_]*-\d+\b")


def _is_done_status(status: str | None) -> bool:
    return (status or "").strip().lower() in DONE_STATUSES


def _dependency_maps(project_state):
    """Return EFFECTIVE active dependency maps, not raw Jira link maps.

    Jira links can remain after an upstream issue is Done. Those historical
    links are useful for audit, but they must not be rendered as current
    blockers or sent to the LLM as active dependency evidence.
    """
    states = {s.issue.key: s for s in project_state.issues}
    blocks: dict[str, list[str]] = {}
    blocked_by: dict[str, list[str]] = {}

    def is_done(key: str) -> bool:
        st = states.get(key)
        return bool(st and _is_done_status(st.issue.status))

    for state in project_state.issues:
        key = state.issue.key
        if _is_done_status(state.issue.status):
            continue
        for dep in state.issue.dependencies or []:
            related = dep.related_issue_key
            rel = (dep.relation or "").strip().lower()
            if is_done(related):
                continue
            if rel == "blocks" or ("blocks" in rel and "blocked by" not in rel):
                blocks.setdefault(key, []).append(related)
            elif "blocked by" in rel or "is blocked by" in rel:
                blocked_by.setdefault(key, []).append(related)
    return (
        {k: sorted(set(v)) for k, v in blocks.items()},
        {k: sorted(set(v)) for k, v in blocked_by.items()},
    )


def ground_ai_analysis(analysis: ProjectAIAnalysis, project_state, deterministic_health: str):
    """Make deterministic Jira facts authoritative over LLM wording.

    The model still performs prioritization and synthesis, but cannot override
    project health, ownership, status, due-state, or direct dependency facts.
    """
    # AI owns project-health judgment in AI-first mode. The deterministic
    # health is retained elsewhere as a fallback/audit signal, not forced over
    # a valid model conclusion.
    states = {s.issue.key: s for s in project_state.issues}
    blocks, blocked_by = _dependency_maps(project_state)

    # Completed issues cannot remain current AI risks merely because Jira keeps
    # historical dependency links.
    analysis.risks = [
        risk for risk in analysis.risks
        if not (states.get(risk.issue_key) and _is_done_status(states[risk.issue_key].issue.status))
    ]

    for risk in analysis.risks:
        state = states.get(risk.issue_key)
        if not state:
            continue
        issue = state.issue
        for ev in risk.evidence:
            typ = (ev.type or "").upper()
            if typ == "STATUS":
                ev.value = issue.status
                ev.related_issue_keys = []
            elif typ == "ASSIGNEE":
                ev.value = issue.assignee
                ev.related_issue_keys = []
            elif typ == "OVERDUE":
                days = state.metrics.days_to_due
                if days is None or days >= 0:
                    ev.value = None
                else:
                    ev.value = f"{abs(days)} day" + ("s" if abs(days) != 1 else "")
            elif typ == "BLOCKS":
                ev.related_issue_keys = blocks.get(issue.key, [])
            elif typ == "BLOCKED_BY":
                ev.related_issue_keys = blocked_by.get(issue.key, [])

        # A common model error is "assign owner" for already assigned work.
        if issue.assignee and _asks_to_assign(risk.recommended_action, issue.key):
            risk.recommended_action = (
                f"Theo dõi với {issue.assignee} về {issue.key} và xác nhận ETA/kế hoạch xử lý."
                if is_vi()
                else f"Follow up with {issue.assignee} on {issue.key} and confirm the ETA/recovery plan."
            )

    corrected_actions: list[str] = []
    for action in analysis.pm_actions:
        replacement = action
        refs = ISSUE_KEY_RE.findall(replacement or "")
        known_refs = [k for k in refs if k in states]
        # Never chase ETA/recovery/ownership for an action whose referenced
        # Jira work is already entirely completed. This deterministically
        # prevents stale LLM actions such as "follow up on DEV-1" after Done.
        if known_refs and all(_is_done_status(states[k].issue.status) for k in known_refs):
            continue

        for key, state in states.items():
            if _is_done_status(state.issue.status):
                continue
            if state.issue.assignee and _asks_to_assign(replacement, key):
                replacement = (
                    f"Theo dõi với {state.issue.assignee} về {key} và xác nhận ETA/kế hoạch xử lý."
                    if is_vi()
                    else f"Follow up with {state.issue.assignee} on {key} and confirm the ETA/recovery plan."
                )
                break
        if replacement not in corrected_actions:
            corrected_actions.append(replacement)
    analysis.pm_actions = corrected_actions

    # Terminology cleanup after reasoning. Keep this deliberately tiny: it
    # fixes known wording drift without rewriting the model's judgment.
    analysis.summary = _normalize_pm_terms(analysis.summary)
    analysis.observations = [_normalize_pm_terms(x) for x in analysis.observations]
    analysis.pm_actions = [_normalize_pm_terms(x) for x in analysis.pm_actions]
    for risk in analysis.risks:
        risk.impact = _normalize_pm_terms(risk.impact)
        risk.recommended_action = _normalize_pm_terms(risk.recommended_action)
    return analysis


def _asks_to_assign(text: str | None, issue_key: str) -> bool:
    if not text:
        return False
    t = text.lower()
    if issue_key.lower() not in t:
        return False
    return bool(re.search(r"\b(assign|owner|gán|phân công)\b", t))


def _normalize_pm_terms(text: str | None) -> str:
    if not text:
        return ""
    value = str(text)
    value = re.sub(r"\bescalade(?:d|s|ing)?\b", "escalate", value, flags=re.IGNORECASE)
    return value
