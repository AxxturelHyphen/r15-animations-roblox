"""Combine simulated playtest runs into a per-moment recall report.

  python playtest/aggregate.py 1        # reads playtest/round_1/run_*/recall.json, writes playtest/round_1/REPORT.md

recall.json format (one file per run, written by the next-day agent):
  {"run": 1, "moments": [{"moment_id": "M11", "mentioned": true, "retold_with_detail": false,
    "wants_to_do_again": false, "sentiment": "neutral", "why": "..."} ...]}
A moment counts as TALKED ABOUT if it was mentioned in at least 2 runs, and FORGOTTEN if it
happened but was mentioned in at most 1 run.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(round_no):
    runs = []
    for p in sorted(glob.glob(os.path.join(HERE, f"round_{round_no}", "run_*", "recall.json"))):
        with open(p) as fh:
            runs.append(json.load(fh))
    return runs


def moment_names():
    names = {}
    for line in open(os.path.join(HERE, "inventory.md")):
        m = re.match(r"\|\s*(M\d+)\s+([\w/ \-]+?)\s*\|\s*([^|]*)\|", line)
        if m:
            names[m.group(1)] = f"{m.group(2).strip()}: {m.group(3).strip()}"
    return names


def aggregate(round_no):
    runs = load(round_no)
    stats = {}
    for run in runs:
        for m in run["moments"]:
            s = stats.setdefault(m["moment_id"], {"happened": 0, "mentioned": 0, "detail": 0, "again": 0, "neg": 0, "why": []})
            s["happened"] += 1
            s["mentioned"] += bool(m.get("mentioned"))
            s["detail"] += bool(m.get("retold_with_detail"))
            s["again"] += bool(m.get("wants_to_do_again"))
            s["neg"] += bool(m.get("mentioned")) and m.get("sentiment") == "negative"
            if m.get("why"):
                s["why"].append(m["why"])
    return runs, stats


def classify(s):
    """talked about (positively) / complained about / forgotten.

    A moment mentioned in 2+ runs but negative in most of those mentions is a COMPLAINT: it is memorable for
    the wrong reason and still needs fixing.
    """
    if s["mentioned"] < 2:
        return "forgotten"
    if s["neg"] * 2 > s["mentioned"]:
        return "complained about"
    return "talked about"


def main():
    round_no = int(sys.argv[1])
    runs, stats = aggregate(round_no)
    names = moment_names()
    key = lambda mid: int(mid[1:]) if mid[1:].isdigit() else 999
    lines = [f"# Simulated playtest — round {round_no}", "",
             f"{len(runs)} independent simulated sessions of the same two friends (see `playtest/personas.md`). "
             "A moment is **talked about** if they brought it up at school in at least 2 of the runs, and "
             "**forgotten** if it happened but came up in at most 1. A moment mentioned mostly negatively is "
             "**complained about**: memorable for the wrong reason. This is an LLM simulation grounded in the "
             "code, not a real playtest.", "",
             "| Moment | Happened (runs) | Mentioned | Negative mentions | Retold with detail | Want to do again | Verdict |",
             "|---|---|---|---|---|---|---|"]
    for mid in sorted(stats, key=key):
        s = stats[mid]
        lines.append(f"| {mid} {names.get(mid, '').split(':')[0]} | {s['happened']} | {s['mentioned']} | {s['detail']} | "
                     f"{s['again']} | **{classify(s)}** |")
    lines += ["", "## Why (from the next-day recall)", ""]
    for mid in sorted(stats, key=key):
        s = stats[mid]
        lines.append(f"- **{mid}** ({classify(s)}): " + " / ".join(s["why"]))
    out = os.path.join(HERE, f"round_{round_no}", "REPORT.md")
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote", os.path.relpath(out, os.path.dirname(HERE)))
    for mid in sorted(stats, key=key):
        print(mid, classify(stats[mid]), stats[mid]["mentioned"], "/", stats[mid]["happened"], "neg", stats[mid]["neg"])
    pa = [r.get("would_play_again") for r in runs]
    print("would_play_again:", pa)
    with open(out, "a") as fh:
        fh.write("\n## Would they play again\n\n" + ", ".join(f"run {r.get('run')}: **{r.get('would_play_again')}**" for r in runs) + "\n\n")
        for r in runs:
            fh.write(f"- Run {r.get('run')} pitch to Sam: \"{r.get('one_line_pitch_to_sam')}\"\n")


if __name__ == "__main__":
    main()
