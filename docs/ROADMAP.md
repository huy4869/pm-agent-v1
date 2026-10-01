# Roadmap

## V6 — Baseline

- Jira collection and normalized project snapshot
- dependency analysis
- deterministic signals/hotspots/pressure
- snapshot-to-snapshot lifecycle and material changes
- AI-first project health and delivery-risk judgement
- AI PM actions/observations
- detailed Markdown report
- concise delivery message
- test utilities using repository `.env`

## V6.1 — Stabilization

Focus on evaluation rather than adding more rules: collect several days of runs, label good/bad AI judgements, tune context and general prompt instructions, reduce report duplication and add schema/grounding validation.

## V6.2 — Team context

Add sprint goal/milestone context, component/team ownership, capacity/workload indicators, comments/activity freshness and richer downstream release context. These improve AI judgement without hard-coding issue-specific rules.

## V6.3 — Microsoft Teams

Publish the concise report to the daily channel, preserve a thread for follow-up discussion and optionally generate owner-specific follow-up prompts/actions.

## V7 — PM Copilot

Move from reporting toward controlled action: propose Jira comments/assignments/status changes, create follow-up actions, track whether PM actions were completed and measure forecast/risk accuracy over time. Writes should use explicit approval/policy controls.

## Production hardening

Add secret management, retries/backoff, observability, structured run IDs, concurrency protection, multi-project configuration, provider fallback, cost/token telemetry, evaluation datasets and retention/privacy controls.
