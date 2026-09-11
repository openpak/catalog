#!/usr/bin/env python3
# Generates catalog.md from catalog.json so the two never drift.
# Run: python3 gen.py   (writes catalog.md next to it)
import json, collections, os

here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(here, "catalog.json")))

TITLE_ORDER = ["live", "beta", "partial", "alpha", "requestable", "planned", "not-feasible"]
FEAT_ORDER = ["working", "beta", "partial", "alpha", "planned", "broken"]

def rank(order, s):
    return order.index(s) if s in order else len(order)

def table(rows, cols):
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c.lower(), "")).replace("|", "\\|") for c in cols) + " |")
    return "\n".join(out)

titles = [x for x in data if x["kind"] == "title"]
feats = [x for x in data if x["kind"] == "feature"]

def counts(items):
    return dict(collections.Counter(x["status"] for x in items))

lines = []
lines.append("# OpenPak catalog\n")
lines.append("Generated from `catalog.json` (the source of truth) by `gen.py` — edit the JSON, "
             "then re-run. Status is **OpenPak's real support state**, cross-checked against the "
             "repos, not a wish list. Honesty over optimism: a wrong \"working\" is worse than an "
             "honest \"partial\".\n")
lines.append("- `live` deployed & running · `beta` deployed/built, not console-verified · "
             "`partial` some modes work · `alpha` being brought up, not deployed · "
             "`requestable` candidate, not started · `planned` intended, nothing built · "
             "`not-feasible` investigated & blocked.\n")

# Summary
tc, fc = counts(titles), counts(feats)
lines.append("## Summary\n")
lines.append("Every title with online multiplayer or co-op that OpenPak serves, is building, or would "
             "accept a request for. Only Switch titles are past `requestable` today — the other ten "
             "consoles wait on their network (platform matrix C). Per-console research and sources: "
             "`titles-by-console.md`.\n")
lines.append(f"**{len(titles)} titles** — " + ", ".join(f"{tc[s]} {s}" for s in TITLE_ORDER if s in tc) + ".\n")
ptc = collections.Counter(x["console"] for x in titles)
lines.append("Per console — " + ", ".join(f"{c} ({n})" for c, n in ptc.most_common()) + ".\n")
lines.append(f"**{len(feats)} features** — " + ", ".join(f"{fc[s]} {s}" for s in FEAT_ORDER if s in fc) + ".\n")
plats = [f for f in feats if f.get("category") == "Console network"]
lines.append(f"**{len(plats)} console networks** — " +
             ", ".join(f"{p['console']} ({p['status']})" for p in
                       sorted(plats, key=lambda x: rank(FEAT_ORDER, x["status"]))) + ".\n")

# Titles
lines.append("## (A) Titles — online-multiplayer and co-op games\n")
titles.sort(key=lambda x: (rank(TITLE_ORDER, x["status"]), x["name"]))
lines.append(table(titles, ["Name", "Console", "Category", "Backend", "Status", "Notes"]))
lines.append("")

# Features — capabilities first, then the per-console platform matrix.
caps = [f for f in feats if f.get("category") != "Console network"]
lines.append("## (B) Network features — the capability matrix\n")
caps.sort(key=lambda x: (rank(FEAT_ORDER, x["status"]), x["category"], x["name"]))
lines.append(table(caps, ["Name", "Console", "Category", "Backend", "Status", "Notes"]))
lines.append("")
lines.append("## (C) Console networks — platform matrix\n")
plats.sort(key=lambda x: (rank(FEAT_ORDER, x["status"]), x["name"]))
lines.append(table(plats, ["Console", "Name", "Backend", "Status", "Notes"]))
lines.append("")

open(os.path.join(here, "catalog.md"), "w").write("\n".join(lines))
print("wrote catalog.md:", len(titles), "titles,", len(feats), "features")
