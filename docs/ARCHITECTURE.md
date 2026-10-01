# Architecture — PM Agent V6

## 1. Goal

V6 is an AI-first PM decision-support pipeline. Code collects and normalizes evidence; deterministic analysis computes reliable signals; AI performs the higher-level PM judgement.

## 2. Logical pipeline

```text
Jira Cloud
   |
   v
Jira Collector
   |  issues, status, owner, due date, links, priority, updates
   v
Normalized Project Snapshot
   |
   +--> Dependency Graph
   +--> Delta / Lifecycle Engine
   +--> Deterministic Signals & Pressure
   |
   v
AI Context Builder
   |
   v
LLM PM Reasoning
   |  project health, priority risks, impact, observations, actions
   v
Report Renderer
   +--> detailed Markdown report
   +--> concise Telegram/Teams-ready message
   |
   v
Run Log / Snapshots / Delivery
```

## 3. Responsibility boundary

### Code owns facts

Code should determine facts that must not be hallucinated: issue existence, Jira status/category, assignee, due dates, overdue age, links, dependency topology, previous snapshot, status transitions, resolved/new signals and deterministic pressure.

### AI owns PM judgement

AI should decide which facts matter most for delivery, final project health, contextual delivery-risk level, impact narrative, management leverage, PM actions and useful observations.

### Deterministic layer is a guardrail, not the PM

A heuristic `CRITICAL` hotspot is evidence supplied to AI. It is not automatically the final AI risk. This distinction is intentional in V6.

## 4. State and lifecycle

Each run should persist enough normalized state to compare with the next run. The previous snapshot is used to identify material delivery changes and lifecycle changes; it should not override current Jira truth.

Typical derived events include work started, newly done, owner changed, new/resolved blocker signals, overdue resolution and dependency-verification signals.

## 5. Dependency model

Jira linked issues are converted into directional relationships such as `blocks` and `is blocked by`. Active dependency hotspots should exclude completed roots from active delivery-risk ranking while retaining stale or questionable topology under dependency hygiene.

The graph layer may calculate direct downstream impact, propagated impact, graph depth and heuristic pressure. AI then evaluates whether that topology represents real delivery risk.

## 6. Delivery adapters

The renderer should produce channel-neutral structured content first. Adapters then transform it for Markdown, Telegram HTML, Microsoft Teams or another destination. Channel formatting must not change the underlying PM judgement.

## 7. Production boundary

Writes back to Jira should be separate from analysis. A future action executor can propose or perform assignment, comments, transitions or escalation only under explicit policy/approval. The reporting pipeline itself should remain safe to run repeatedly.
