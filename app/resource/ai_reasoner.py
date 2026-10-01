from __future__ import annotations

import json
from dataclasses import asdict

from app.domain.models import ProjectState
from app.resource.engine import DONE, load_profiles

RA_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "understood_request": {"type": "string"},
        "assessment": {"type": "string"},
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "verdict": {"type": "string", "enum": ["RECOMMENDED", "POSSIBLE", "NOT_RECOMMENDED", "NEEDS_VERIFICATION"]},
                    "reasoning": {"type": "array", "items": {"type": "string"}},
                    "risks": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "verdict", "reasoning", "risks"],
            },
        },
        "recommendation": {"type": "string"},
        "alternatives": {"type": "array", "items": {"type": "string"}},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
    },
    "required": ["understood_request", "assessment", "candidates", "recommendation", "alternatives", "missing_information", "confidence"],
}

SYSTEM_PROMPT = """
You are the Resource Allocation Copilot for a Project Manager.

The application supplies facts. YOU make the allocation judgment.
Do not use, invent, or request a deterministic score. Do not rank people by a formula.
Reason holistically from the user's natural-language request and the supplied resource/task facts.

Consider when supported by facts:
- requested role/skills and evidence of skill suitability
- current assignments and their statuses
- due dates, overdue work, priority, blockers/dependencies and delivery impact
- requested start timing and duration
- workload across the supplied sources
- whether interrupting a person would create more delivery risk than it solves
- uncertainty and missing data

IMPORTANT:
- Do NOT blindly prefer the person with the fewest active tasks.
- Missing skill data is NOT proof that a person lacks the skill. Say it is unverified.
- A skill listed in a resource profile is evidence, not an absolute guarantee of proficiency.
- Do not fabricate availability percentages, capacity percentages, estimates, deadlines, skills, or project impact.
- Do not infer that N active tasks means a precise utilization percentage.
- If nobody is genuinely suitable, explicitly say so; never force a recommendation.
- If evidence is insufficient, recommend what the PM should verify next.
- Prefer management reasoning over arithmetic.
- Clearly separate facts from inference in your reasoning.
- Answer in Vietnamese, concise and useful for a PM in Telegram.
"""


def build_ra_context(state: ProjectState) -> dict:
    profiles = load_profiles()
    profile_by_name = {profile.name.lower(): profile for profile in profiles}
    names = {profile.name for profile in profiles}
    names.update(item.issue.assignee for item in state.issues if item.issue.assignee)

    resources = []
    for name in sorted(names, key=str.lower):
        profile = profile_by_name.get(name.lower())
        tasks = []
        for item in state.issues:
            issue = item.issue
            if not issue.assignee or issue.assignee.lower() != name.lower():
                continue
            if issue.status.strip().lower() in DONE:
                continue
            tasks.append({
                "key": issue.key,
                "source": issue.source,
                "summary": issue.summary,
                "status": issue.status,
                "priority": issue.priority,
                "due_date": issue.due_date,
                "days_to_due": item.metrics.days_to_due,
                "days_in_status": item.metrics.days_in_status,
                "days_since_update": item.metrics.days_since_update,
                "signals": [signal.code for signal in item.signals],
                "dependencies": [asdict(dep) for dep in (issue.dependencies or [])],
            })
        resources.append({
            "name": name,
            "profile": {
                "role": profile.role if profile else None,
                "skills": list(profile.skills) if profile else [],
                "skills_data_status": "AVAILABLE" if profile and profile.skills else "NOT_PROVIDED",
            },
            "active_tasks": tasks,
        })
    return {"project_key": state.project_key, "resources": resources}


def _build_ai_client():
    from app.ai.client_factory import build_ai_client
    return build_ai_client()


def analyze_allocation(state: ProjectState, user_request: str) -> tuple[dict, str]:
    prompt = (
        SYSTEM_PROMPT
        + "\n\nUSER REQUEST:\n" + user_request.strip()
        + "\n\nRESOURCE AND WORK FACTS (JSON):\n"
        + json.dumps(build_ra_context(state), ensure_ascii=False, indent=2)
        + "\n\nReturn only JSON matching the response schema."
    )
    client = _build_ai_client()
    data = json.loads(client.generate_json(prompt, RA_RESPONSE_SCHEMA))
    return data, (client.last_provider or "AI")
