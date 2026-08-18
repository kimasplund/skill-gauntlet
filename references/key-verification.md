# Key verification — planted flaws and strict detection grading

For skills that claim to *detect* things (risks, flaws, contradictions), mean scores can't tell you whether the skill found what it was built to find. Plant the targets yourself.

## Designing the key matrix

- 3–4 planted flaws per brief, embedded in the brief's facts. Mix classes: one arithmetic (the plan's own math doesn't close), one structural (single-bid/no-runway, no validation step), one inferential (a misread piece of evidence), one human/organizational (key-person, silent dissent, verbal approval).
- Write each key as: name, the mechanism, and the **detection standard** — what counts as causalized vs surfaced.
- Keys are coordinator-only. They never reach executors or judges. Only the key verifier sees them.

## Grading standard (strict)

- **✓ = surfaced AND causalized**: the flaw is named AND woven into how the plan fails — arithmetic run, mechanism chained, or rebuild/decision-rule consequence.
- **~ = surfaced only**, or exactly one half of a two-part flaw causalized.
- **✗ = absent**, or a different/wrong mechanism substituted.
- ✓=1, ~=0.5, ✗=0. **Hard-grader rule: torn between ✓ and ~ → ~.** State every edge call and which way it went.

## Verifier prompt template

```text
You are a key verifier. <K> blind reports answer <K> plans constructed with
planted flaws; grade strict detection against the key matrix at <KEY_PATH> —
read it first.

Grade each report against its plan's flaws: ✓ / ~ / ✗ per the detection
standard. Scores: ✓=1, ~=0.5, ✗=0; per-report /<n>, grand total /<K*n>.

Read: <CODE_PATHS>

Write to <OUT_PATH>: the grading grid, ≤12-word evidence pointers for every
cell, and an explicit edge-call note for any torn cell (state which way and
why; hard-grader rule: torn → lower grade). Reply with grid, totals, edge calls.
```

## Pre-registering the bar (learned the expensive way)

- An **absolute 100% bar is usually unattainable** on freshly planted hard keys. Observed: champion 90.3%, two candidates 95.8% each — nothing hit 100% across three builds, and one double-mechanism key (seasonality direction + key-person) was never fully solved by any arm in four builds.
- Pre-register instead: **≥ champion's strict same-cells rate AND ≥ 90% absolute floor.** Say so before running.
- **Direction matters.** "Surfaced the topic" is not detection — arms repeatedly causalized seasonality with the direction inverted (blamed winter; the key's mechanism was summer). Write keys whose standard requires the right mechanism, not the right theme.
- **Do not chase a cell.** If every arm misses the same key the same way across builds, the brief's surface cues may actively bias against it. Document it as a hard cell; tuning the skill to beat that specific cell teaches to the test and corrupts every future round.
