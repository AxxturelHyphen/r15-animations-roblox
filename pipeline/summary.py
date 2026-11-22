"""Write reports/SUMMARY.md and the before/after previews in output/previews/.

  python -m pipeline.summary
"""
import glob
import json
import os
import re
import shutil

from PIL import Image, ImageDraw

from pipeline import build
from pipeline.render import CELL, _font

REPORTS = os.path.join(build.ROOT, "reports")
PREV = os.path.join(build.ROOT, "output", "previews")
METRIC_KEYS = ["accel_spikes", "velocity_corners", "loop_seam_issues", "joint_limit_violations", "dead_holds",
               "lockstep_key_frames", "twinned_channels", "foot_slide_segments", "foot_penetration_frames", "overlap_score"]


def iterations(name):
    its = []
    for p in glob.glob(os.path.join(build.WORK, name, "iter_*", "metrics.json")):
        its.append(int(re.search(r"iter_(\d+)", p).group(1)))
    return sorted(its)


def load(path):
    with open(path) as fh:
        return json.load(fh)


def before_after(name, first, last):
    """Two GIF rows side by side: iteration 0 on top, the final iteration underneath."""
    fa = sorted(glob.glob(os.path.join(build.WORK, name, f"iter_{first}", "frames", "f*.png")))
    fb = sorted(glob.glob(os.path.join(build.WORK, name, f"iter_{last}", "frames", "f*.png")))
    n = max(len(fa), len(fb))
    font = _font(15)
    frames = []
    for i in range(n):
        canvas = Image.new("RGB", (CELL * 2, CELL * 2 + 44), (30, 30, 34))
        d = ImageDraw.Draw(canvas)
        for row, (lst, label) in enumerate(((fa, f"BEFORE (iter {first})"), (fb, f"AFTER (iter {last})"))):
            im = Image.open(lst[min(i, len(lst) - 1)])
            y = row * (CELL + 22) + 22
            canvas.paste(im, (0, y))
            d.text((6, y - 19), label, fill=(255, 220, 120) if row else (200, 200, 200), font=font)
        frames.append(canvas.convert("P", palette=Image.ADAPTIVE, colors=160))
    os.makedirs(PREV, exist_ok=True)
    out = os.path.join(PREV, f"{name}_before_after.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=33, loop=0, optimize=True)
    # Final contact sheet(s) + curves for reference.
    for p in glob.glob(os.path.join(build.WORK, name, f"iter_{last}", "review", "*.png")):
        shutil.copy(p, os.path.join(PREV, f"{name}_final_{os.path.basename(p)}"))
    shutil.copy(os.path.join(build.WORK, name, f"iter_{last}", "preview.gif"), os.path.join(PREV, f"{name}.gif"))
    return out


def main():
    lines = ["# Critic loop summary", "",
             "Each animation went through: build → render/analyze → Fable 5.2 critique → automatic F-curve fixes → re-render, "
             "until the critic approved it (no high- or medium-severity findings) or 3 rounds had run.", "",
             "Metrics are issue counts from `pipeline/analyze.py` (lower is better), except `overlap_score` (higher is better: 1.0 means "
             "no lockstep keys).", ""]
    overview = ["| Animation | Rounds | Final verdict | Findings per round (H/M/L) | Critic scores, first → last (fluidity/posing/timing/transitions/appeal) |",
                "|---|---|---|---|---|"]
    detail = []
    for name in build.ALL_ANIMATIONS:
        its = iterations(name)
        if not its:
            continue
        reports = {}
        for p in glob.glob(os.path.join(REPORTS, name, "iter_*.json")):
            reports[int(re.search(r"iter_(\d+)\.json$", p).group(1))] = load(p)
        sev = []
        for i in sorted(reports):
            c = {"high": 0, "medium": 0, "low": 0}
            for f in reports[i].get("findings", []):
                c[f.get("severity", "low")] = c.get(f.get("severity", "low"), 0) + 1
            sev.append(f"r{i}: {c['high']}/{c['medium']}/{c['low']}")
        last_rep = reports[max(reports)] if reports else {}
        verdict = last_rep.get("verdict", "n/a")

        def sc(r):
            s = r.get("scores", {})
            return "/".join(str(s.get(k, "-")) for k in ("fluidity", "posing", "timing", "transitions", "appeal"))

        scores = f"{sc(reports[min(reports)])} → {sc(last_rep)}" if reports else ""
        overview.append(f"| {name} | {len(reports)} | {verdict} | {' · '.join(sev)} | {scores} |")

        detail += [f"## {name}", "", "| Metric | " + " | ".join(f"iter {i}" for i in its) + " |",
                   "|---|" + "---|" * len(its)]
        ms = {i: load(os.path.join(build.WORK, name, f"iter_{i}", "metrics.json"))["score"] for i in its}
        for k in METRIC_KEYS:
            detail.append(f"| {k} | " + " | ".join(str(ms[i].get(k)) for i in its) + " |")
        detail.append("")
        for i in sorted(reports):
            r = reports[i]
            detail.append(f"**Round {i} critique** ({r.get('verdict')}): {r.get('summary', '')}")
            detail.append("")
            for f in r.get("findings", []):
                ops = ", ".join(o.get("op") for o in f.get("fix", []))
                detail.append(f"- `{f.get('severity')}` **{f.get('category')}** F{f.get('frames')} {', '.join(f.get('bones', []))}: "
                              f"{f.get('observation')} → *{ops}*")
            logp = os.path.join(REPORTS, name, f"iter_{i}_applied.log")
            if os.path.exists(logp):
                with open(logp) as fh:
                    last_line = fh.read().strip().splitlines()[-1]
                detail.append(f"- *apply_fixes:* {last_line}")
            detail.append("")
        detail.append(f"Before/after: `output/previews/{name}_before_after.gif`")
        detail.append("")
        before_after(name, its[0], its[-1])
    with open(os.path.join(REPORTS, "SUMMARY.md"), "w") as fh:
        fh.write("\n".join(lines + overview + [""] + detail) + "\n")
    print("wrote reports/SUMMARY.md")


if __name__ == "__main__":
    main()
