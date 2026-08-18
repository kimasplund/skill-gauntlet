#!/usr/bin/env python3
"""Pool judge scores into a margin table + instrument checks.

Judges must end their files with a machine-readable block (the panel prompt
requires it):

    ```scores
    judge,code,D1,D2,...,Dk,total
    RC,N9,6,7,...,53
    ```

Usage: scorecard.py <scores_dir> --champion CODE [CODE ...] --candidate CODE [CODE ...]

Prints: per-dim pooled means and margins (candidate - champion), per-judge
means, inter-judge agreement (% of shared codes where per-dim scores differ by
<=1), and within-arm spread per dim (max-min) as a variance gate.
"""
import argparse, csv, io, os, re, sys
from collections import defaultdict

SCORES_RE = re.compile(r"```scores\s*\n(.*?)\n```", re.S)

def load(scores_dir):
    rows = []
    for fn in sorted(os.listdir(scores_dir)):
        if not fn.endswith(".md"): continue
        text = open(os.path.join(scores_dir, fn)).read()
        for block in SCORES_RE.findall(text):
            rdr = csv.DictReader(io.StringIO(block.strip()))
            for r in rdr:
                rows.append({k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()})
    if not rows:
        sys.exit(f"no ```scores blocks found in {scores_dir}")
    rows = [r for r in rows if "total" in r and r.get("total") not in (None, "")]
    if not rows:
        sys.exit("no judge-format scores rows (with a total column) found")
    dims = [k for k in rows[0] if k not in ("judge", "code", "total")]
    rows = [r for r in rows if all(d in r and r[d] not in (None, "") for d in dims)]  # skip foreign blocks (e.g. auditor schemas)
    for r in rows:
        for d in dims + ["total"]:
            r[d] = float(r[d])
    return rows, dims

def mean(xs): return sum(xs) / len(xs) if xs else float("nan")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scores_dir"); ap.add_argument("--champion", nargs="+", required=True)
    ap.add_argument("--candidate", nargs="+", required=True)
    a = ap.parse_args()
    rows, dims = load(a.scores_dir)
    ch, ca = set(a.champion), set(a.candidate)

    arm = {r["code"]: ("C" if r["code"] in ch else "V" if r["code"] in ca else "?") for r in rows}
    unknown = sorted(c for c, x in arm.items() if x == "?")
    if unknown: print(f"note: unscored-arm codes present (controls/fixtures?): {unknown}\n")

    print(f"{'dim':5} {'champ':>7} {'cand':>7} {'margin':>8} {'champ_n':>7} {'cand_n':>7}")
    margins = {}
    for d in dims:
        cvals = [r[d] for r in rows if r["code"] in ch]
        vvals = [r[d] for r in rows if r["code"] in ca]
        m = mean(vvals) - mean(cvals)
        margins[d] = m
        print(f"{d:5} {mean(cvals):7.2f} {mean(vvals):7.2f} {m:+8.2f} {len(cvals):7d} {len(vvals):7d}")
    ct = [r["total"] for r in rows if r["code"] in ch]
    vt = [r["total"] for r in rows if r["code"] in ca]
    print(f"{'total':5} {mean(ct):7.2f} {mean(vt):7.2f} {mean(vt)-mean(ct):+8.2f}")

    print("\nper-judge means (champ | cand):")
    byj = defaultdict(lambda: defaultdict(list))
    for r in rows:
        byj[r["judge"]][arm[r["code"]]].append(r["total"])
    for j, arms in sorted(byj.items()):
        c, v = arms.get("C", []), arms.get("V", [])
        print(f"  {j}: {mean(c):.2f} (n={len(c)}) | {mean(v):.2f} (n={len(v)})")

    print("\ninter-judge agreement (shared codes, per dim):")
    bycode = defaultdict(dict)
    for r in rows: bycode[r["code"]][r["judge"]] = r
    cells = within1 = 0
    worst = []
    for code, judges in bycode.items():
        js = list(judges)
        for i in range(len(js)):
            for j2 in js[i+1:]:
                for d in dims:
                    cells += 1
                    diff = abs(judges[js[i]][d] - judges[j2][d])
                    if diff <= 1: within1 += 1
                    else: worst.append((code, d, js[i], j2, diff))
    if cells:
        print(f"  {within1}/{cells} cells within 1 pt ({100*within1/cells:.0f}%)")
        for w in worst[:10]: print(f"  disagreement: {w}")
    else:
        print("  no shared codes (check crossed design)")

    print("\nwithin-arm spread per dim (max-min; should be << margins):")
    for d in dims:
        cvals = [r[d] for r in rows if r["code"] in ch]
        vvals = [r[d] for r in rows if r["code"] in ca]
        print(f"  {d}: champ {max(cvals)-min(cvals):.1f} (n={len(cvals)}) | cand {max(vvals)-min(vvals):.1f} (n={len(vvals)})")

if __name__ == "__main__":
    main()
