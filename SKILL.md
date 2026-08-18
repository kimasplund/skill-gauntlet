---
name: skill-gauntlet
description: >
  Regression-guarded blind A/B evaluation for skills, prompts, and agent
  configurations. Use when a candidate revision of a skill (or system prompt,
  rubric, or agent config) must prove it beats the current champion WITHOUT
  regressing guard dimensions before adoption — champion/challenger testing,
  pre-registered conjunctive adoption gates, blind persona-diverse judge
  panels, cross-check auditors, planted-flaw key verification, framing
  fixtures, negative fixtures, and generic controls. Triggers: "A/B test this
  skill", "extreme testing", "make sure we're not regressing", "test before
  adopting", "compare these two prompts/skills rigorously", "champion vs
  challenger", evolving an installed skill where a silent regression would be
  costly. Do NOT use for: simple factual QA, one-shot content generation, or
  evals where a single automated metric fully defines quality (use a test
  suite instead).
---

# Skill Gauntlet — regression-guarded A/B evaluation

Adopt a candidate only when it beats the champion **on value dimensions and does not regress on guard dimensions**. Totals and preference votes measure added value; conjunctive guards protect existing value. Candidates that win every blind forced choice can still be correctly rejected — that is the harness working, not failing.

Three inviolable rules:

1. **Pre-register everything before running any cell** — the adoption gate, the cells, the instruments, the comparison set. No goalpost movement after results arrive. If a bar turns out to be mis-set, report both readings; the pre-registered text decides.
2. **Blind everything scoreable.** Judges, auditors, and executors never see version names, the sealed mapping, or planted-flaw keys. Only the coordinator holds the mapping.
3. **The champion is frozen.** Never modify the champion artifact during a round, not even "harmless" fixes. Hash it (md5) before and after.

## The workflow

### Phase 0 — Scope and design

- Define the **champion** (current shipped artifact) and the **candidate** (exact diff from champion; verify by `diff` that nothing else changed).
- Design **briefs**: 2–4 realistic tasks hard enough that the skill should matter, in fresh domains the skill has never seen. For skills with detection claims, plant 3–4 flaws per brief and write the **key matrix** (see [references/key-verification.md](references/key-verification.md)).
- Design **fixtures** (see [references/fixtures.md](references/fixtures.md)): a framing-invariance pair (same facts, hyped vs skeptical register) and a negative fixture (a task too small for the skill — the highest-information single cell; every evolution round ratchets toward more machinery, so price restraint).
- Freeze the **rubric**: 7–9 dimensions split into value dims (where the candidate claims gains) and guard dims (where regression is fatal). Anchor every odd rung. See [references/judge-panel.md](references/judge-panel.md).

### Phase 1 — Pre-register the gate

Write the adoption rule into the results file BEFORE any execution. Conjunctive template (adapt dims; full template in [references/protocol.md](references/protocol.md)):

> Candidate passes iff ALL of: (1) ≥ champion on every guard dim, on every instrument; (2) value-dim margins ≥ pre-set floors; (3) key detection ≥ relative-to-champion AND ≥ 90% absolute floor; (4) framing invariant; (5) negative fixture behaves; (6) instrument checks pass (controls gap, inter-judge agreement). Anything less → champion ships unchanged, candidate's deltas ship only as a research note.

Add the **symmetric-loss clause**: on failure the candidate branch is discarded; its deltas return to an inventory with failure data attached. Never "fix and re-judge the same run" — that is goalpost movement.

### Phase 2 — Execute cells blind

Spawn one executor subagent per cell. Each executor gets only: the skill path (champion or candidate), the brief verbatim, an output path. No testing context, no keys, no version names. Cells: candidate × briefs × N runs (N≥2 for variance), champion × same, plus fixtures for both, plus 1 **generic control** per brief (no skill at all) — controls calibrate the discrimination floor.

### Phase 3 — Blind and leak-scan

Copy raw outputs to anonymized codes via `scripts/normalize.py` (mapping JSON → blind codes; runs a leak regex scan; inspect hits manually, never auto-fix). Codes and judge panel assignments go in a coordinator-only sealed mapping file.

### Phase 4 — Score with three instrument classes

Run all three in parallel; they are blind to each other and to the mapping.

- **Judge panels** (2–3 persona-diverse judges, crossed design: every brief scored by ≥2 judges, every judge sees both arms mixed): dimension-major scoring, forced choice per brief, suspected-generic call. Prompt patterns and persona design: [references/judge-panel.md](references/judge-panel.md).
- **Cross-check auditor**: re-scores the guard dims mechanically (rule-text applied literally), runs the framing and restraint gates. When judges and auditor disagree on a guard dim, **the conservative reading governs**. See [references/auditor.md](references/auditor.md).
- **Key verifier**: grades planted-flaw detection (✓/~/✗ with evidence pointers, hard-grader rule: torn → lower grade). See [references/key-verification.md](references/key-verification.md).

Pool judges with `scripts/scorecard.py` (judges must emit a machine-readable scores block — required by the panel prompt).

### Phase 5 — Apply the gate exactly

Compute margins per dimension, check every conjunctive condition, write the verdict. On PASS: repackage/reinstall the candidate, write the round report. On FAIL: champion ships unchanged; write the research note capturing validated wins, failure autopsies, and the next candidate's specified fixes. Either outcome is a deliverable.

## Hard-won operating rules (each cost a round to learn)

- **Dimension-major scoring** (score dim 1 across all reports, then dim 2…) is what makes inter-judge agreement reach ~100% cell-level within-1pt. Do not let judges score report-by-report.
- **The negative fixture is the highest-information cell.** Skills drift toward ceremony; both champion and candidate once ran full machinery on a trivial task. Keep one in every round.
- **Absolute 100% detection bars are usually unattainable** on freshly planted hard keys — pre-register relative-to-champion plus a 90% floor instead, and say so before running.
- **Instruments will disagree.** Judges grade holistically; the auditor applies rule text mechanically. Both readings are real. Pre-commit to the conservative one for adoption decisions.
- **Prose bans do not stop template-driven leaks.** If the report template is organized as numbered stages, executors will cross-reference "Stage 4" no matter how strongly the skill forbids it. Enforce with a mechanical pre-delivery grep gate, or de-ordinal the template.
- **A compliance failure is not a design failure** — log which one you saw. A candidate whose mechanism works but whose self-check missed a case needs a checklist fix, not a re-mine.
- **Do not chase a specific key.** If every arm misses the same planted flaw the same way across builds, document it as a hard cell; tuning the skill to that cell teaches to the test and corrupts the harness.
- **Margins are not decision-grade without uncertainty.** With the small N these rounds run, pre-register an INCONCLUSIVE verdict (collect more cells) alongside PASS/FAIL, and treat any margin inside the noise band as "not yet evidence." Details in [references/protocol.md](references/protocol.md).
- **Guard dims include operational ones when the artifact ships to production** — cost, latency, output-schema compatibility. A candidate that triples cost or breaks downstream consumers must fail the gate even when quality dims pass.
- **Delete subagents after their results arrive; never spawn judges who can see each other's scores.**
- **Normalize format tells in the blinder.** When arms differ in template format (numbered vs unnumbered headers), every judge can identify the arm at a glance. Strip the tell from ALL blind copies (`normalize.py --strip-h2-ordinals`) while leaving prose leaks intact — those are auditor evidence.
- **A fixture is burned the moment its answer enters any candidate's text.** Quoting the expected fixture answer inside a skill (even as an example) means restraint on that fixture can never be measured again. Rotate fixtures every round; grep candidates for fixture content before running.
- **Auditor prompts quote the pre-registered rule text verbatim — never paraphrase.** A paraphrase that adds one category ("tag or class names") can charge rubric-required content as violations and split your instruments; score any extra category separately as exploratory, never in the binding number.
- **The cheap spread noise-band is direction-blind.** A candidate above the champion in every single cell can still read as "inside the band". Wherever cell-level dominance is plausible, pre-register a paired sign test alongside the spread heuristic.
- **Blind codes, judge IDs, and rubric dimension names share one namespace across ALL rounds.** Keep them disjoint (no D5 code when D5 is a dimension; no J3 code when J3 is a judge).
