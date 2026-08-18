# skill-gauntlet

An agent skill for regression-guarded, blind, pre-registered A/B evaluation of other skills, prompts, and agent configurations. A candidate revision is adopted only when it beats the current champion on the dimensions it targets **without regressing anything you already have** — and the gate is written down, sealed, before a single cell runs.

Candidates that win every blind preference vote can still be correctly rejected. That is the harness working, not failing: totals measure added value; conjunctive guards protect existing value.

## What it does

Given a champion artifact and a candidate diff, the skill runs a six-phase evaluation:

1. **Scope & design** — fresh briefs hard enough that the skill matters, planted flaws with a sealed key matrix, a framing-invariance pair, and a negative fixture that prices restraint.
2. **Pre-register the gate** — a conjunctive adoption rule (guard dims on every instrument, value-dim floors, key-detection bars, fixture gates, instrument checks) written before execution, with a symmetric-loss clause and INCONCLUSIVE as a first-class verdict.
3. **Execute blind** — context-free executor agents per cell; no version names, no keys, no testing context; generic no-skill controls calibrate the floor.
4. **Blind & leak-scan** — outputs normalized to sealed codes (`scripts/normalize.py`), format tells neutralized (`--strip-h2-ordinals`), leak regexes inspected by hand.
5. **Score with three instrument classes** — persona-diverse judge panels (dimension-major, crossed design), a mechanical cross-check auditor for guard dims, and a strict planted-flaw key verifier. Pooled by `scripts/scorecard.py`.
6. **Apply the gate exactly** — margins vs the pre-registered text, conservative reading on instrument disagreement, no goalpost movement. Either outcome ships a deliverable: an adoption, or a research note with failure data and the next candidate specified.

## Install

Self-contained: `SKILL.md` + `references/` + `scripts/` (two dependency-free Python scripts). Copy into your agent's skills location:

```bash
# Claude Code
git clone https://github.com/kimasplund/skill-gauntlet.git ~/.claude/skills/skill-gauntlet

# Kimi Code
git clone https://github.com/kimasplund/skill-gauntlet.git ~/.agents/skills/skill-gauntlet
```

## Usage

Invoke when a candidate revision of a skill, system prompt, rubric, or agent config must prove itself against the shipped version and a silent regression would be costly:

- "A/B test this skill against the current one."
- "Make sure the new version doesn't regress anything."
- "Champion vs challenger, and be rigorous about it."

Not for simple factual QA or anything a single automated metric fully measures — use a test suite for that.

## What's in the box

| Path | Contents |
|---|---|
| `SKILL.md` | The six-phase workflow, three inviolable rules, and the hard-won operating rules (each one cost a real round to learn) |
| `references/protocol.md` | Pre-registration template, sealed mapping, statistical sufficiency, adjudication precedents |
| `references/judge-panel.md` | Panel design, rubric design, dimension-major mechanics, prompt template |
| `references/auditor.md` | The mechanical guard-dim instrument and its precedents |
| `references/key-verification.md` | Planted-flaw design and strict ✓/~/✗ grading |
| `references/fixtures.md` | Framing-invariance pairs and negative (restraint) fixtures |
| `scripts/normalize.py` | Blinder: sealed-code copies, leak scan, format-tell stripping |
| `scripts/scorecard.py` | Pools judge scores blocks into margin tables + instrument checks |

## Track record

Built by a Kimi agent swarm to evolve [premortem-skill](https://github.com/kimasplund/premortem-skill), then hardened in a third round run by Claude on fresh material. Across four candidate challenges in three rounds:

- Inter-judge agreement reached **100% of cells within 1 point** in every round (324/324 in round 3) using dimension-major scoring and anchored rubrics.
- Generic controls scored **17–31 points below** both arms on a 55-point scale — the instruments discriminate skill from base-model competence.
- **Every candidate beat the champion on totals and swept the blind forced choices; three of four were still correctly refused** by pre-registered guards — including one whose refusal exposed a mis-set statistical bar, reported as both readings rather than silently bent.
- The negative fixture caught a restraint hole shared by both arms in one round — the single most valuable finding of that round.

Round-3 evaluation record and the harness lessons that became this version's operating rules: [premortem-skill/evolution/round-3.md](https://github.com/kimasplund/premortem-skill/blob/main/evolution/round-3.md).

## License

[MIT](LICENSE)
