# Changelog

## V6 — Interactive Resource Allocation

- Added Telegram long-polling mode via `python main.py bot`.
- Added natural-language resource-allocation reasoning and member workload lookup.
- Added an optional skill profile via `RESOURCE_PROFILE_FILE`.
- Resource decisions are AI-first and do not use a deterministic allocation score.
- Interactive analysis uses the configured Jira or Redmine source.

## V6 — AI-first baseline — 2026-08-23

V6 establishes the final baseline architecture for the current iteration.

### Changed

- Final project health is an AI PM assessment rather than a direct deterministic mapping.
- Priority risks expose separate `AI Delivery Risk` and `Rule-based Hint` values.
- Deterministic analysis is retained for factual guardrails, candidate ranking, lifecycle, dependency topology and auditability.
- AI receives richer downstream context and is responsible for contextual delivery-risk judgement, impact, observations and PM actions.
- Active dependency hotspots are separated from dependency-hygiene/verification cases.
- Repeated runs without Jira changes report no material delivery changes instead of replaying old transitions.

### Validated behavior

A V6 run on project DEV produced `AT_RISK` while deterministic health remained `CRITICAL`, demonstrating that AI judgement is no longer a simple copy of rule-based severity. The same run differentiated deterministic-CRITICAL candidates into HIGH, MEDIUM and LOW AI delivery risk based on downstream context.

### Follow-up

Do not patch individual AI judgements with issue-specific rules. Tune general context, grounding and risk-calibration instructions using a multi-day evaluation set.
