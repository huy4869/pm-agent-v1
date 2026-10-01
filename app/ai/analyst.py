import json

from app.ai.context_builder import (
    build_ai_context,
)
from app.ai.models import (
    AIRisk,
    ProjectAIAnalysis,
    RiskEvidence,
)
from app.domain.models import (
    ProjectState,
)
from app.memory.delta import (
    ProjectDelta,
)
from app.intelligence.hotspots import (
    ProjectHotspots,
)
from app.i18n import report_language


# ============================================================
# ALLOWED VALUES
# ============================================================

ALLOWED_HEALTH = {
    "HEALTHY",
    "WATCH",
    "AT_RISK",
    "CRITICAL",
}


ALLOWED_RISK = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
}


ALLOWED_CONFIDENCE = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


ALLOWED_EVIDENCE_TYPES = {
    "STATUS",
    "ASSIGNEE",
    "OVERDUE",
    "NEAR_DUE",
    "BLOCKS",
    "BLOCKED_BY",
    "PERSISTENT_BLOCKER",
    "STALE",
    "STUCK",
    "PARENT_STATUS",
    "DEPENDENCY_VERIFICATION",
}


# ============================================================
# GEMINI RESPONSE SCHEMA
# ============================================================

EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": sorted(
                ALLOWED_EVIDENCE_TYPES
            ),
        },
        "issue_key": {
            "type": [
                "string",
                "null",
            ],
        },
        "value": {
            "type": [
                "string",
                "null",
            ],
        },
        "related_issue_keys": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },
    "required": [
        "type",
        "issue_key",
        "value",
        "related_issue_keys",
    ],
}


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "health": {
            "type": "string",
            "enum": [
                "HEALTHY",
                "WATCH",
                "AT_RISK",
                "CRITICAL",
            ],
        },

        "summary": {
            "type": "string",
        },

        "risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                    },

                    "level": {
                        "type": "string",
                        "enum": [
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "CRITICAL",
                        ],
                    },

                    "evidence": {
                        "type": "array",
                        "items": EVIDENCE_SCHEMA,
                    },

                    "impact": {
                        "type": "string",
                    },

                    "confidence": {
                        "type": "string",
                        "enum": [
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                        ],
                    },

                    "recommended_action": {
                        "type": "string",
                    },
                },
                "required": [
                    "issue_key",
                    "level",
                    "evidence",
                    "impact",
                    "confidence",
                    "recommended_action",
                ],
            },
        },

        "observations": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },

        "pm_actions": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
    },

    "required": [
        "health",
        "summary",
        "risks",
        "observations",
        "pm_actions",
    ],
}


# ============================================================
# SYSTEM INSTRUCTION
# ============================================================

SYSTEM_INSTRUCTION = """
You are the primary PM reasoning agent for a software-delivery project.

ROLE SPLIT
- The application code is the truth/fact layer: Jira fields, due-state math,
  final status, ownership, effective dependency direction, snapshot delta and
  data-quality signals.
- YOU are the intelligence layer. You own the management judgment: project
  health, risk severity, prioritization, root-problem interpretation,
  escalation judgment, PM actions and executive narrative.
- deterministic_hints are heuristics for recall/sanity-checking only. They are
  NOT conclusions you must repeat. You may rank an issue above/below a hint
  when the supplied facts justify it.

GROUNDING
- Use ONLY PROJECT CONTEXT.
- Never invent release/milestone impact, commitments, team capacity, business
  criticality, critical-path membership, owners, dependencies or deadlines.
- Evidence is factual. Impact is cautious inference from those facts.
- active_dependencies and active_dependency_clusters are current delivery
  relationships. dependency_hygiene/raw topology is NOT an active blocker.
- Preserve dependency direction exactly. For A→B→C, A can have propagated
  impact on C, but B is C's direct upstream blocker.
- Done/Closed/Resolved work is not a current delivery risk unless a supplied
  inconsistency still has current impact.

PM REASONING
- Look across the whole board_overview before deciding the top risks. Use it to
  notice patterns such as risk concentration around one owner or several
  blockers converging on the same downstream issue.
- Then use detailed_issue_facts and active_dependency_clusters for evidence.
- Think in clusters/chains and management leverage, not isolated tickets.
- Prefer root problems that release multiple downstream items over duplicated
  symptoms, but do not call stale/verification topology a root blocker.
- Do not treat unassigned backlog in bulk as a risk. Unassigned matters when
  the issue is delivery-relevant (overdue, near due, active blocker, stuck,
  active execution, etc.).
- NO_PROGRESS alone is not a meaningful delivery risk without other pressure.
- A status change to In Progress is progress, but does not by itself resolve an
  overdue/blocking risk.
- A resolved upstream blocker may improve a downstream issue without fully
  resolving that downstream issue's own overdue/blocking risk.

SEVERITY / HEALTH
- Decide severity yourself from evidence; deterministic heuristic levels are
  advisory only.
- LOW: little/no current delivery threat.
- MEDIUM: concrete PM attention is useful, but delivery is not clearly at risk.
- HIGH: strong evidence of likely downstream/timeline impact.
- CRITICAL: major immediate delivery pressure requiring urgent intervention.
- Project health should reflect the combined delivery picture, not merely the
  highest single issue.

ESCALATION / ACTIONS
- Decide whether escalation is warranted; rule escalation candidates are hints.
- Never recommend assigning an owner if one already exists.
- If assigned and action is needed: follow up with that owner for ETA/recovery.
- If unassigned and delivery-relevant: assigning an owner can be the action.
- Do not chase ETA/action on completed issues.
- Actions must be prioritized, concrete and tied to current facts.

QUALITY CONTROL
- Avoid duplicate risks/actions/observations that describe the same problem.
- Do not mix aggregate counts. E.g. 5 overdue issues does not imply 5 CRITICAL
  blockers unless facts prove the same five satisfy both conditions.
- Do not claim downstream milestones/releases/features unless supplied.
- Before returning, verify every issue key, dependency direction, assignee,
  due-state and action against PROJECT CONTEXT.

Return structured JSON only.
"""


# ============================================================
# ANALYST
# ============================================================

class ProjectAIAnalyst:
    def __init__(
        self,
        client,
    ) -> None:
        self.client = client

    def analyze(
        self,
        project_state: ProjectState,
        delta: ProjectDelta,
        hotspots: ProjectHotspots | None = None,
        risk_intelligence=None,
    ) -> ProjectAIAnalysis:
        context = build_ai_context(
            project_state,
            delta,
            hotspots,
            risk_intelligence,
        )

        prompt = f"""
{SYSTEM_INSTRUCTION}

==================================================
PROJECT CONTEXT
==================================================

{context}


==================================================
TASK
==================================================

Analyze the current project delivery state.

OUTPUT LANGUAGE:
- If report_language is "vi", write natural Vietnamese prose, but KEEP common software/PM terminology in English: issue, task/tasks, blocker, owner, dependency, dependency chain, downstream, delivery, delivery risk, ETA, recovery plan, escalation/escalate, cluster, hotspot, snapshot, Risk Pressure, Risk Lifecycle, CRITICAL, HIGH, MEDIUM, LOW.
- Never translate severity/health enums. Use "escalate" (never "escalade"). Prefer "owner" over "người chịu trách nhiệm", "delivery risk" over "rủi ro giao hàng", and "downstream tasks" over "công việc downstream".
- If report_language is "en", write them in English.
- Keep Jira issue keys and enum values unchanged.
- Distinguish delivery risk from deterministic hotspot priority; never upgrade delivery-risk severity only because hotspot priority is higher.

report_language = {report_language()}

Return:

1. Overall project health.
2. Concise executive summary.
3. Meaningful delivery risks.
4. Structured factual evidence for each risk.
5. Delivery impact.
6. Confidence.
7. Concrete PM actions.
8. Useful observations.

Prioritize the delivery picture you infer from Jira facts. Use deterministic hints as advisory signals, not as the ranking authority.

If only one meaningful risk exists, return one risk.

If there are no meaningful observations, return [].

If there are no meaningful PM actions, return [].

Return structured output only.
"""

        raw_response = (
            self.client.generate_json(
                prompt,
                RESPONSE_SCHEMA,
            )
        )

        data = json.loads(
            raw_response
        )

        return self._parse_analysis(
            data
        )

    # ========================================================
    # PARSE ANALYSIS
    # ========================================================

    def _parse_analysis(
        self,
        data: dict,
    ) -> ProjectAIAnalysis:
        health = str(
            data.get(
                "health",
                "WATCH",
            )
        ).upper()

        if health not in ALLOWED_HEALTH:
            health = "WATCH"

        risks: list[AIRisk] = []

        raw_risks = data.get(
            "risks",
            [],
        )

        if not isinstance(
            raw_risks,
            list,
        ):
            raw_risks = []

        for raw_risk in raw_risks:
            risk = self._parse_risk(
                raw_risk
            )

            if risk is not None:
                risks.append(
                    risk
                )

        observations = self._clean_string_list(
            data.get(
                "observations",
                [],
            )
        )

        pm_actions = self._clean_string_list(
            data.get(
                "pm_actions",
                [],
            )
        )

        summary = str(
            data.get(
                "summary",
                "",
            )
        ).strip()

        return ProjectAIAnalysis(
            health=health,
            summary=summary,
            risks=risks[:5],
            observations=observations[:5],
            pm_actions=pm_actions[:5],
        )

    # ========================================================
    # PARSE RISK
    # ========================================================

    def _parse_risk(
        self,
        raw_risk,
    ) -> AIRisk | None:
        if not isinstance(
            raw_risk,
            dict,
        ):
            return None

        issue_key = str(
            raw_risk.get(
                "issue_key",
                "",
            )
        ).strip()

        if not issue_key:
            return None

        level = str(
            raw_risk.get(
                "level",
                "MEDIUM",
            )
        ).upper()

        if level not in ALLOWED_RISK:
            level = "MEDIUM"

        confidence = str(
            raw_risk.get(
                "confidence",
                "MEDIUM",
            )
        ).upper()

        if (
            confidence
            not in ALLOWED_CONFIDENCE
        ):
            confidence = "MEDIUM"

        evidence = self._parse_evidence_list(
            raw_risk.get(
                "evidence",
                [],
            )
        )

        impact = str(
            raw_risk.get(
                "impact",
                "",
            )
        ).strip()

        recommended_action = str(
            raw_risk.get(
                "recommended_action",
                "",
            )
        ).strip()

        return AIRisk(
            issue_key=issue_key,
            level=level,
            evidence=evidence,
            impact=impact,
            confidence=confidence,
            recommended_action=(
                recommended_action
            ),
        )

    # ========================================================
    # PARSE EVIDENCE
    # ========================================================

    def _parse_evidence_list(
        self,
        raw_evidence,
    ) -> list[RiskEvidence]:
        if not isinstance(
            raw_evidence,
            list,
        ):
            return []

        result: list[RiskEvidence] = []

        for item in raw_evidence:
            evidence = (
                self._parse_evidence(
                    item
                )
            )

            if evidence is not None:
                result.append(
                    evidence
                )

        return result

    def _parse_evidence(
        self,
        item,
    ) -> RiskEvidence | None:
        if not isinstance(
            item,
            dict,
        ):
            return None

        evidence_type = str(
            item.get(
                "type",
                "",
            )
        ).upper().strip()

        if (
            evidence_type
            not in ALLOWED_EVIDENCE_TYPES
        ):
            return None

        raw_issue_key = item.get(
            "issue_key"
        )

        issue_key = None

        if raw_issue_key:
            issue_key = str(
                raw_issue_key
            ).strip() or None

        raw_value = item.get(
            "value"
        )

        value = None

        if raw_value is not None:
            value = str(
                raw_value
            ).strip() or None

        related_issue_keys = (
            self._clean_string_list(
                item.get(
                    "related_issue_keys",
                    [],
                )
            )
        )

        return RiskEvidence(
            type=evidence_type,
            issue_key=issue_key,
            value=value,
            related_issue_keys=(
                related_issue_keys
            ),
        )

    # ========================================================
    # STRING LIST
    # ========================================================

    @staticmethod
    def _clean_string_list(
        value,
    ) -> list[str]:
        if not isinstance(
            value,
            list,
        ):
            return []

        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]