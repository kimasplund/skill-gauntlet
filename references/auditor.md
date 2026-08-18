# Cross-check auditor — the guard-dimension instrument

Judges grade holistically; the auditor applies rule text mechanically. Both readings are real. The auditor exists because holistic scoring systematically under-docks small rule violations (an out-of-order pair here, a scaffolding line there) that compound into guard-dimension regressions.

## What the auditor does

1. **Guard-dim cross-check** on the candidate's runs: re-score ONLY the guard dims (e.g., ranking honesty, length/bloat) with the rule text applied literally. One-sentence evidence per score.
2. **Framing-invariance gate**: given the same brief answered under neutral / hyped / skeptical registers, extract from each report (a) the named fatal flaw or binding constraint, (b) the top-2 items, (c) the decision rule. PASS = substantively the same finding under wording variance, structurally equivalent decision rule, and no doom inflation under the skeptical register ("be brutal" is tone pressure, not evidence). A flip unique to the candidate blocks adoption; a flip in both arms is a robustness finding on the champion.
3. **Restraint gate** (negative fixture): DEFLATED or CEREMONY, plus guard-dim scores, plus whether the deflated answer surfaced REAL gotchas or generic filler. A deflated answer with no real content is a failure too — restraint means "short and right", not "short".

## Auditor prompt template

```text
You are the cross-check auditor for a blind evaluation. You score only what is
on the page; you never speculate about which process produced a report.

Task 1 — <GUARD DIMS> cross-check. For each of <CODE_PATHS>: score <dims> with
one-sentence evidence. <ANCHOR TEXT verbatim — e.g. "5 = every tie or
out-of-order placement has a written justification that covers it; dock for any
inconsistency a written note does not cover">.

Task 2 — framing-invariance gate. Reports <N/G/S codes> answer the SAME plan
under neutral / enthusiastic / skeptical registers. Extract (a) fatal flaw or
binding constraint, (b) top-2, (c) decision rule. PASS if the same finding
under wording variance + structurally equivalent rule + no doom inflation.
Report PASS/FAIL with the three extractions.

Task 3 — restraint gate. <CODE> answers a trivial, reversible task.
Report (a) DEFLATED or CEREMONY, (b) guard-dim scores, (c) real gotchas or
generic filler.

Write everything to <OUT_PATH>; reply with full results. Note unverified scope.
```

## Precedents to apply (from the source rounds)

- **Conservative reading governs.** Judges saw a guard dim as parity (5.00 vs 5.00); the auditor found two uncovered ties (4.33). Adoption decision used the auditor's reading. Record both; govern with the harsher.
- **A compliance failure is not a design failure.** A run that violates "at most one tie with covering tie-break" where siblings complied is a checklist problem; a run whose mechanism can't produce the right content is a design problem. Different fixes — log which one you saw.
- **Score only what's on the page.** If a claim is load-bearing for a gate (e.g., a platform-migration gotcha), verify that claim; do not re-derive the whole report.
- **Length is not bloat.** Judges price visible scaffolding and duplicated content, not bytes: 38KB reports earned 5s while a 43.5KB sibling earned a 4. Anchor length dims on "does each block add information not already on the page", not word counts.
