"""Build, render and analyze animations for one iteration.

  python -m pipeline.run_all --build              # build iter_0 from the specs, then render and analyze
  python -m pipeline.run_all --iter 1 walk run    # render and analyze an existing iteration
"""
import argparse
import json
import os
import time

import bpy

from pipeline import analyze, build, curves, render


def review_dir(name, iteration):
    return os.path.join(build.WORK, name, f"iter_{iteration}")


def process(name, iteration, do_render=True):
    build.open_iteration(name, iteration)
    out = review_dir(name, iteration)
    os.makedirs(os.path.join(out, "review"), exist_ok=True)
    title = f"{name} (iteration {iteration})"
    info = render.render_review(out, title) if do_render else {}
    metrics = analyze.analyze()
    analyze.write(os.path.join(out, "metrics.json"), metrics)
    with open(os.path.join(out, "keys.json"), "w") as fh:
        json.dump({"animation": name, "iteration": iteration, "frame_end": bpy.context.scene.frame_end,
                   "loop": bool(bpy.context.scene.get("loop")), "keys": curves.dump_keys()}, fh, indent=1)
    return metrics["score"], info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--iter", type=int, default=0)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()
    names = args.names or build.ALL_ANIMATIONS
    for n in names:
        t = time.time()
        if args.build:
            _, probs = build.build(n)
            for p in probs:
                print("  spec limit:", p)
        score, _ = process(n, args.iter, do_render=not args.no_render)
        print(f"{n} iter {args.iter}: {score}  ({time.time() - t:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
