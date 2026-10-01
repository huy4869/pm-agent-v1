# AI Design — PM Agent V6

## 1. Design objective

The LLM is the PM reasoning layer, not a text formatter for deterministic rules.

Bad pattern:

```text
rules decide risk -> LLM rewrites rules
```

V6 pattern:

```text
facts + heuristic hints + history -> LLM evaluates delivery context -> PM judgement
```

## 2. AI responsibilities

The model should:

1. Assess overall project health.
2. Select a small set of priority delivery risks.
3. Assign contextual AI delivery risk independently of the heuristic hint.
4. Explain impact using concrete downstream evidence.
5. Detect concentration risks such as several critical tasks on one owner.
6. Identify management leverage/root causes.
7. Recommend executable PM actions.
8. Explain meaningful change since the previous run.
9. Avoid elevating technical hygiene signals into delivery risks unless they materially affect delivery.

## 3. Inputs the AI should receive

Prefer structured JSON/context over a giant pre-rendered report. Include project snapshot, current issues relevant to risk, dependency graph summary, deterministic hotspots, lifecycle/delta, escalation hints, previous pressure, owner workload context and data-quality warnings.

For each candidate issue, include enough context to reason: key/summary, status and status category, priority, assignee, due date/overdue age, direct blockers, direct downstream issues, relevant downstream status/due date, persistence/history and heuristic score/reasons.

## 4. Guardrails

The AI must not invent issue keys, owners, dates, links, status transitions or dependency edges. Every factual claim should be grounded in supplied evidence.

The model may disagree with a heuristic severity, but should be able to explain why. Example: an overdue persistent blocker may be deterministic CRITICAL but AI LOW/MEDIUM when the downstream item has no delivery deadline; conversely, a modest heuristic can be elevated if the downstream task is release-critical tomorrow.

## 5. Health judgement

Use semantic health values such as `HEALTHY`, `WATCH`, `AT_RISK`, `CRITICAL`. Do not derive them by a single pressure threshold. Consider deadline proximity, critical-path impact, number and persistence of blockers, recovery evidence, ownership concentration, material trend and downstream urgency.

## 6. Risk calibration

AI risk should answer: **How likely and consequential is this issue to hurt delivery now?**

`CRITICAL`: immediate/major delivery threat requiring escalation or intervention.

`HIGH`: significant delivery threat with near-term downstream impact.

`MEDIUM`: real delivery concern but impact/timing is less immediate or uncertain.

`LOW`: limited current delivery impact; continue monitoring.

Persistent overdue/blocking evidence should prevent casual downgrading. A LOW classification for such an issue should require strong contextual justification.

## 7. Output contract

Prefer schema-constrained structured output, for example:

```json
{
  "project_health": "AT_RISK",
  "assessment": "...",
  "priority_risks": [
    {
      "issue_key": "DEV-25",
      "ai_risk": "HIGH",
      "impact": "...",
      "evidence": ["..."]
    }
  ],
  "pm_actions": ["..."],
  "observations": ["..."]
}
```

Rendering links and Markdown/HTML belongs in code.

## 8. Prompting rule

Do not add one-off rules such as `if DEV-35 then MEDIUM`. Improve the context and general reasoning instructions instead. V6 should generalize to new projects without issue-specific prompt patches.
