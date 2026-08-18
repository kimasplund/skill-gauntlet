#!/usr/bin/env python3
"""Normalize raw executor outputs into blind judge-facing copies.

Usage: normalize.py <mapping.json> <raw_dir> <blind_dir> [--strip-h2-ordinals] [extra_leak_regex ...]

mapping.json: flat {"<raw filename>": "<CODE>", ...} or nested under any keys —
all string leaves ending in .md are mapped. Codes become <CODE>.md in blind_dir.
Leak scan reports regex hits for manual inspection; NEVER auto-fixes (a hit may
be natural language, e.g. 'they champion it').
Coordinator-only: the mapping file must never reach judges or executors.
"""
import json, os, re, sys, hashlib

DEFAULT_LEAKS = [
    (re.compile(r"(?i)\b(skill\.md|the skill|this skill|skill's)\b"), "method"),
    (re.compile(r"(?i)\b(champion|challenger|candidate)\b"), "version"),
]

def collect(obj, out):
    if isinstance(obj, dict):
        for v in obj.values(): collect(v, out)
    elif isinstance(obj, list):
        for v in obj: collect(v, out)
    elif isinstance(obj, str) and obj.endswith(".md"):
        out.append(obj)
    return out

def main():
    argv = [a for a in sys.argv[1:] if a != "--strip-h2-ordinals"]
    strip_ordinals = "--strip-h2-ordinals" in sys.argv[1:]
    mapping_path, raw_dir, blind_dir = argv[0], argv[1], argv[2]
    extra = [(re.compile(p, re.I), "extra") for p in argv[3:]]
    patterns = DEFAULT_LEAKS + extra
    mapping = json.load(open(mapping_path))

    raw2code = {}
    for brief, cells in mapping.get("main", {}).items():
        for cell, code in cells.items():
            raw2code[f"{brief}-{cell}.md"] = code
    for section in ("framing", "fixture", "controls", "neutral"):
        for cell, code in mapping.get(section, {}).items():
            prefix = "" if section in ("neutral",) else f"{section}-"
            raw2code[f"{prefix}{cell}.md"] = code
    # allow an explicit flat override for any naming scheme
    raw2code.update(mapping.get("flat", {}))

    os.makedirs(blind_dir, exist_ok=True)
    done, missing, leaks = [], [], {}
    for raw_name, code in sorted(raw2code.items()):
        src = os.path.join(raw_dir, raw_name)
        if not os.path.exists(src):
            missing.append(raw_name); continue
        text = open(src).read()
        hits = [(lbl, m.group(0)) for pat, lbl in patterns for m in pat.finditer(text)]
        if hits: leaks[raw_name] = hits
        norm = text.strip() + "\n"
        if strip_ordinals:
            # neutralize template format tells: '## 1. The X' -> '## The X' in every blind copy
            norm = re.sub(r"^(## )\d+[.)]\s+", r"\1", norm, flags=re.M)
        open(os.path.join(blind_dir, f"{code}.md"), "w").write(norm)
        done.append(f"{raw_name} -> {code}.md ({len(norm)} chars, sha {hashlib.sha1(norm.encode()).hexdigest()[:8]})")

    print("NORMALIZED:");  print("\n".join(done) if done else "  (none)")
    print("\nMISSING RAW:"); print("\n".join(missing) if missing else "  (none)")
    print("\nLEAK SCAN (inspect, do not auto-fix):")
    if leaks:
        for k, v in leaks.items(): print(f"  {k}: {v}")
    else:
        print("  clean")

if __name__ == "__main__":
    main()
