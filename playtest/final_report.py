"""Cross-round summary of the simulated playtest: python playtest/final_report.py  ->  playtest/REPORT.md"""
import glob
import json
import os
import re

from aggregate import aggregate, classify, moment_names

HERE = os.path.dirname(os.path.abspath(__file__))
SHORT = {"talked about": "talked about", "complained about": "complained", "forgotten": "forgotten"}


def rounds():
    return sorted(int(re.search(r"round_(\d+)$", d).group(1)) for d in glob.glob(os.path.join(HERE, "round_*"))
                  if glob.glob(os.path.join(d, "run_*", "recall.json")))


def first_quote(path, who="Robin"):
    """A short line from the lunch scene, for flavour."""
    try:
        for line in open(path):
            line = line.strip().strip("*")
            if line.startswith(f"{who}:") or line.startswith(f"**{who}"):
                text = re.sub(r"^\**\w+\**:\s*", "", line)
                if 40 <= len(text) <= 160:
                    return text
    except OSError:
        pass
    return ""


def main():
    rs = rounds()
    data = {r: aggregate(r) for r in rs}
    names = moment_names()
    ids = sorted({m for r in rs for m in data[r][1]}, key=lambda m: int(m[1:]))
    out = ["# Simulated first session: what two friends remember", "",
           "Two simulated 12-year-old best friends (Kai and Robin, `personas.md`) play the Roblox build for the first time,",
           "three independent sessions per round. Separate zero-context agents then write the next-day lunch-table",
           "conversation and record which moments came up. **This is an LLM simulation grounded in the code, not a real",
           "playtest.** Treat it as a design review that predicts what kids would retell. The real-playtest checklist is",
           "at the bottom.", "",
           "Verdicts: **talked about** (mentioned in at least 2 of 3 runs, mostly positive), **complained** (mentioned in at least 2 of 3, mostly negative),",
           "**forgotten** (happened, mentioned in at most 1 of 3). Cells show the verdict and the mention count.", "",
           "| Moment | " + " | ".join(f"Round {r}" for r in rs) + " |",
           "|---|" + "---|" * len(rs)]
    for m in ids:
        cells = []
        for r in rs:
            s = data[r][1].get(m)
            cells.append(f"{SHORT[classify(s)]} ({s['mentioned']}/{s['happened']})" if s else "n/a")
        out.append(f"| {m} {names.get(m, '').split(':')[0]} | " + " | ".join(cells) + " |")
    out += ["", "| | " + " | ".join(f"Round {r}" for r in rs) + " |", "|---|" + "---|" * len(rs),
            "| Would play again | " + " | ".join(", ".join(x.get("would_play_again", "?") for x in data[r][0]) for r in rs) + " |"]
    out += ["", "## Pitches to Sam, the friend who hasn't played", ""]
    for r in rs:
        for run in data[r][0]:
            out.append(f"- Round {r}, run {run.get('run')}: \"{run.get('one_line_pitch_to_sam')}\"")
    out.append("")
    open(os.path.join(HERE, "REPORT.md"), "w").write("\n".join(out) + "\n")
    print("wrote playtest/REPORT.md")


if __name__ == "__main__":
    main()
