# Protocol — pre-registration, sealed mapping, adjudication

## Pre-registration file (write BEFORE any execution)

```markdown
## Pre-registration — round <N>
- Candidate = champion + <exact deltas, verified by diff>
- Cells: <candidate/champion> × <briefs> × <runs>, fixtures <list>, controls <list>
- Blind codes: <recorded in SEALED-MAPPING.json>
- Instruments: judges <ids+personas>, auditor, key verifier; rubric <path, frozen hash>
- Comparison set: <which runs are pooled against which>
- **Candidate passes iff ALL of:**
  1. ≥ champion on every guard dim, on BOTH instruments (judges pooled + auditor)
  2. Value-dim margins ≥ <floors, e.g. ≥ half the prior round's margin>
  3. Key detection ≥ champion's strict same-cells rate AND ≥ 90% absolute
  4. Framing invariant (auditor gate)
  5. Negative fixture DEFLATES with real gotchas
  6. Instrument checks: controls gap ≥ <floor>, inter-judge agreement, variance gate
- Anything less → champion ships unchanged; deltas ship only as a research note.
  Symmetric-loss clause: the candidate branch is discarded, not patched-and-rejudged.
- INCONCLUSIVE clause: if any decisive margin lands inside the pre-registered
  noise band (see Statistical sufficiency), the round returns INCONCLUSIVE —
  collect more cells with the identical gate; do not force a verdict.
```

## Sealed mapping (coordinator-only)

```json
{
  "main": {"D": {"champion-r1": "E8", "...": "..."}, "E": {}, "F": {}},
  "framing": {"champion-hype": "W1", "champion-skeptical": "F1"},
  "fixture": {"champion": "K8", "candidate": "J7"},
  "controls": {"D": "E5"},
  "judge_panels": {"J1": {"D": ["..."], "E": ["..."]}}
}
```

Rules: codes are short random letter+digit; check for collisions across ALL rounds (codes accumulate); judges get file paths in a fixed order, never the mapping; record the judge→codes assignment for later decoding.

## Statistical sufficiency (decide with uncertainty, not raw margins)

Small-cell rounds (3–6 runs/arm) cannot support bare-mean adoption calls. Pre-register how the gate handles noise:

- **INCONCLUSIVE is a first-class verdict.** If a margin is inside the noise band, the gate returns "collect more cells" — never forced to PASS/FAIL on underpowered evidence.
- **Noise band, cheap version**: within-arm spread (max−min) per dim. A margin smaller than the larger arm's spread is inside the band. (`scripts/scorecard.py` prints both.)
- **Noise band, better version** (when cells ≥ ~20): cluster-bootstrap the margin, resampling by brief; read the 95% CI. For paired cells (same brief, both arms), a paired Wilcoxon signed-rank per dimension or a binomial test on forced choices are the concrete defaults. Guard dims use a non-inferiority reading (CI lower bound ≥ −δ, pre-registered δ); value dims use superiority (CI lower bound > floor).
- **Power note in the pre-registration**: state the N per arm and the smallest margin the design can detect. If the claimed effect is smaller than that, enlarge the design before running, not after.
- **Operational guard dims** (production artifacts only): cost per run, latency, invalid-output rate, downstream schema compatibility. Pre-register as guard dims; a regression blocks adoption like any other guard.

## Adjudication rules (pre-commit to these too)

1. **Conservative reading governs** cross-instrument disagreement on guard dims.
2. **Both readings reported** when a bar turns out mis-set (e.g., an absolute bar nothing can meet); the pre-registered text decides the condition.
3. **Within-instrument fairness**: retest panels re-score champion cells alongside candidate cells — pooled comparisons are only valid within an instrument.
4. **Instrument checks**: generic controls must land a large fixed gap below both arms (observed ~28–31 pts on a 55-pt scale) or the rubric doesn't discriminate; inter-judge agreement target ~100% of cells within 1 pt; within-arm variance must be small vs margins.
5. **No goalpost movement.** A bar can only be re-registered for a FUTURE round, with the rationale written before that round's execution.

## Verdict and aftermath

- PASS → repackage + reinstall the candidate; round report with full scorecard; archive instruments.
- FAIL → champion ships unchanged (verify hashes); research note with: validated wins (dims + margins), failure autopsies (which condition, which instrument, root cause: design vs compliance), specified fixes for the next candidate, and any hard cells deliberately not chased.
- Either way, the round's primary product is knowledge. A clean NO with a specified next candidate is worth more than a muddy yes.
