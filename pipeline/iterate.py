"""Apply critic reports for iteration N, then render and analyze iteration N+1.

  python -m pipeline.iterate 0                # every animation that has reports/<anim>/iter_0.json with needs_work
  python -m pipeline.iterate 1 walk jump
"""
import json
import os
import sys

from pipeline import apply_fixes, build, run_all


def main():
    it = int(sys.argv[1])
    names = sys.argv[2:] or build.ALL_ANIMATIONS
    for n in names:
        rp = os.path.join(apply_fixes.REPORTS, n, f"iter_{it}.json")
        if not os.path.exists(rp):
            print(f"{n}: no report for iter {it}, skipping")
            continue
        with open(rp) as fh:
            rep = json.load(fh)
        if rep.get("verdict") == "approved" and not rep.get("findings"):
            print(f"{n}: approved at iter {it}")
            continue
        applied, failed = apply_fixes.apply_report(n, it)
        score, _ = run_all.process(n, it + 1)
        print(f"{n}: applied {applied} ops ({failed} skipped) -> iter {it + 1}: {score}", flush=True)


if __name__ == "__main__":
    main()
