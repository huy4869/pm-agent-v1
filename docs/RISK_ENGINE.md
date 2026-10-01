# Risk Engine — Deterministic Guardrails

## 1. Purpose

The deterministic engine provides stable, explainable evidence to the AI. It is deliberately conservative and may rate a condition more severely than the final AI PM assessment.

## 2. Typical signals

The implementation may expose signals such as:

- `OVERDUE`
- `NEAR_DUE`
- `BLOCKED`
- `BLOCKING_OTHERS`
- persistent blocker / blocker observed across snapshots
- `DEPENDENCY_NEEDS_VERIFICATION`
- `STALE_DEPENDENCY_CANDIDATE`
- `PARENT_DONE_CHILD_OPEN`
- unassigned/open ownership risk

Names should remain stable once external reports/tests depend on them.

## 3. Pressure

Pressure is a heuristic ranking mechanism. It is useful for candidate selection, escalation hints and trend comparison. It is not a probability and must not be presented as an objective business-risk percentage.

Project risk pressure can be compared between runs (`previous -> current`) to show direction: increasing, decreasing or stable.

## 4. Hotspots

Hotspots rank issues by management leverage using deterministic evidence such as overdue state, blocking downstream work, being blocked, near-due state, persistence and dependency impact.

The AI receives hotspot priority/pressure as `Rule-based Hint`, then makes its own `AI Delivery Risk` decision.

## 5. Dependency clusters

For each active root, derive direct downstream issues, propagated downstream issues, maximum depth and aggregate heuristic pressure. Completed roots should not continue to appear as active delivery blockers solely because Jira links remain.

If a completed relationship appears stale, move it to dependency hygiene/verification rather than active delivery hotspots.

## 6. Escalation signals

Rule-based escalation is an attention signal, not an automatic management action. Typical reasons include critical delivery pressure, overdue beyond a configured age and meaningful downstream impact.

AI should decide whether/how escalation appears in PM Actions.

## 7. Lifecycle correctness

A run must compare current normalized facts with the immediately relevant previous snapshot. Re-running without Jira changes should produce no material delivery changes. Status transitions and resolved signals must appear once when the underlying state changes, not repeatedly on every run.

## 8. Design constraint

Do not grow this module into a second PM brain. Add deterministic logic only when it improves factual correctness, candidate retrieval, topology, lifecycle, safety or explainability. Contextual prioritization belongs to AI.
