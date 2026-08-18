# Judge panels — design, rubric, prompt pattern

## Panel design

- **2–3 judges**, personas chosen for diverse priors (e.g., operator/CFO, founder, enterprise risk officer, early-stage investor). Persona diversity is what turns "a judge liked it" into "the field likes it."
- **Crossed design**: every brief is scored by at least two judges; every judge's panel mixes both arms. Example for 3 briefs × (3 champion + 1 candidate): J1 scores D+E, J2 scores E+F, J3 scores D+F; retest panels score candidate runs interleaved among champion runs.
- Judges are blind: anonymized codes only, no mapping, no keys, no other judges' scores.

## Rubric design

- 7–9 dimensions total. Split into **value dims** (where the candidate claims gains) and **guard dims** (where regression blocks adoption — typically probability/ranking honesty, length discipline, tone).
- Anchor every odd rung with a behavioral description. Unanchored scales produce judge drift; anchored odd rungs produce ~100% inter-judge agreement within 1 pt.
- Mix sensitivities: at least one dim near ceiling (catches regressions), one dim with headroom (measures gains), one gate dim (restraint/tone).

Worked example — the premortem rubric (9 dims, max 55): D1 specificity (1–7), D2 causal chaining (1–7), D3 probability honesty (1–5, GUARD), D4 flaw detection (1–5), D5 rebuild actionability (1–7, VALUE), D6 adversarial depth (1–7), D7 tripwires (1–7, VALUE), D8 cold tone (1–5, GUARD), D9 length/bloat (1–5, GUARD).

## Scoring mechanics that make agreement happen

- **Dimension-major**: score D1 across all reports in the panel, then D2 across all, etc. Never report-by-report.
- Read ALL reports before scoring anything.
- One-sentence evidence note per score — forces page-grounded calls and makes adjudication possible later.
- **Forced choice** per brief group: which single report the judge would hand the decision-maker. (Forces a holistic preference that totals can miss. In every round of the source project, forced choices and dimension means told different stories — report both.)
- **Suspected-generic call**: any report that could apply to any plan gets flagged (calibrates against boilerplate).
- End with 3–5 sentences on what separated best from worst.

## Judge prompt template

```text
You are Judge <ID>, <persona: role, years, what you price>. You score blind reports.

Read the rubric at <RUBRIC_PATH> and follow its mechanics exactly
(dimension-major scoring; anchored odd rungs; scales per dim; max total <N>).

Score these <K> reports, in this order:
<CODE_PATHS — arms interleaved, e.g. V2, U2, N9, E8>
(The first four are one plan; the next four …; the last four …)

Write full results to <OUT_PATH>: per report, all dimension scores with a
one-sentence evidence note each, and the total. Then: (a) one forced choice
per plan group — which single report you would hand the decision-maker, and
why; (b) suspected-generic reports; (c) 3–5 sentences on best-vs-worst.

MANDATORY: end the file with a machine-readable block:
```scores
judge,code,D1,D2,...,D9,total
<ID>,<CODE>,...
```
```

## Anti-patterns

- Judges seeing raw (non-anonymized) outputs — version strings leak.
- A judge scoring only one arm — kills the crossed design.
- Letting judges see each other's work — anchor contamination.
- Comparing pooled scores across different panels as if calibrated: pooled comparisons are only fair WITHIN an instrument (one judge re-scored champion cells at a harsher anchor than another; within-judge margins stayed valid).
