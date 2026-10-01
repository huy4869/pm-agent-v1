# Operations

## 1. Normal run

A production run should follow this sequence: load configuration, fetch current Jira state, normalize issues, load previous snapshot, compute graph/delta/signals, build AI context, call AI, validate structured response, render artifacts, persist current snapshot/run log and deliver the concise message.

## 2. Idempotency

Running the agent twice without Jira changes should not invent a new lifecycle event. The second run should normally report no material delivery changes while retaining current unresolved risks.

## 3. Failure behavior

Fail loudly on missing required Jira credentials, invalid Jira responses, malformed AI structured output after retries or inability to persist the snapshot when persistence is required for lifecycle correctness.

Delivery failure should not erase a successfully generated report. Record generation and delivery status separately so a message can be retried without recomputing project judgement unnecessarily.

## 4. Logs

Keep technical run logs with collection counts, API errors, normalization warnings, raw/normalized delta, deterministic signals, dependency hygiene, AI request metadata without secrets, AI validation errors, artifact paths and delivery status.

Do not log API tokens or full authorization headers.

## 5. Daily scheduling

Schedule only after manual runs are stable. Use the project timezone and run before the team's daily meeting. Ensure only one run owns the snapshot update for a given execution window, or use a run ID/lock to prevent races.

## 6. Incident checklist

When a report looks wrong, inspect in this order: Jira source facts, normalized issue, dependency direction, previous snapshot selection, deterministic signal/pressure, AI context, AI structured response, renderer. This identifies whether the defect is data, deterministic analysis, AI judgement or presentation.

## 7. Secret hygiene

If a credential appears in chat/source/logs, rotate it. Do not rely on deleting the visible message as credential remediation.
