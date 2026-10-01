# Testing — V6

## 1. Objective

Test both deterministic correctness and AI reasoning. A passing deterministic engine is not sufficient if the AI merely mirrors its severity.

## 2. Baseline test

Run twice without Jira changes. Expected: snapshot metrics stable, pressure stable, no fake material changes, unresolved risks remain visible and no status transition is repeated.

## 3. Status transition scenario

Move one seeded issue from an open/idea state to In Progress. Expected: exactly one work-started/status-transition delta on the next run; subsequent unchanged run should not repeat it.

Move it to Done. Expected: newly-done event, active blocker contribution removed when appropriate, blocked/downstream facts recalculated and pressure adjusted.

## 4. Blocker-resolution scenario

Use a chain such as `A blocks B`, optionally `B blocks C`. Resolve A. Expected: A disappears from active dependency hotspots; B's blocked signal resolves when no other active blocker remains; stale Jira links may be reported under dependency hygiene rather than as active delivery blockers.

## 5. Multiple blockers

Let A and X both block B. Resolve only A. Expected: B remains blocked because X is still active. This protects against the common bug where resolving one incoming dependency incorrectly clears the whole blocked state.

## 6. Overdue scenario

Create/seed an issue with due date in the past. Verify overdue age, pressure and escalation hint. Then mark Done and verify `OVERDUE` resolves and the issue no longer contributes active overdue pressure.

## 7. Near-due downstream scenario

Create an overdue blocker whose downstream task is due tomorrow. Expected: AI should normally rank this above an equivalent blocker whose downstream item has no meaningful deadline, even if deterministic scores are similar.

## 8. AI independence test

Provide several deterministic CRITICAL candidates with materially different delivery context. Expected: AI may produce different contextual risk levels and must explain them. If every AI risk always equals the rule hint, the architecture has regressed toward rule-first.

## 9. AI safety test

Assert that every issue key, owner, dependency and due-date fact in the AI output exists in the supplied context. Reject or repair output containing unsupported facts.

## 10. Ownership concentration

Assign several overdue/blocking issues to one owner. Expected: AI may identify a resource bottleneck and recommend workload review/rebalancing, but should phrase this as an evidence-based risk rather than certainty about the person's capacity.

## 11. Test utilities

Repository test scripts should load `.env` and be safe to re-run. Seeded test issues should have an obvious marker such as `[PMTEST]`. Sprint setup utilities should reuse an existing named test sprint where possible instead of creating duplicates.

## 12. Regression suite

Keep fixture-based tests for normalization, dependency direction, graph traversal, delta generation, pressure, completed-root filtering, multiple blockers and rendering. Keep a smaller set of LLM integration/evaluation cases for PM judgement because model output is semantic rather than byte-for-byte deterministic.
