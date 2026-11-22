"""Offline sanity check of the Rojo project (Rojo itself isn't available in the build container).

  python roblox/check_project.py

Checks that default.project.json parses, that every $path exists, that every clip in AnimationIds has a
KeyframeSequence (.rbxmx) and an AnimationMeta entry, and that every .rbxmx is a well-formed
KeyframeSequence with the full R15 pose tree.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R15 = {"HumanoidRootPart", "LowerTorso", "UpperTorso", "Head"} | {
    s + p for s in ("Left", "Right") for p in ("UpperArm", "LowerArm", "Hand", "UpperLeg", "LowerLeg", "Foot")}


def walk(node, where, errs):
    for key, child in node.items():
        if key == "$path":
            if not os.path.exists(os.path.join(ROOT, child)):
                errs.append(f"{where}: $path {child!r} does not exist")
        elif not key.startswith("$") and isinstance(child, dict):
            walk(child, f"{where}.{key}", errs)


def main():
    errs = []
    with open(os.path.join(ROOT, "default.project.json")) as fh:
        project = json.load(fh)
    walk(project["tree"], "game", errs)

    def names(path):
        with open(os.path.join(ROOT, path)) as fh:
            return set(re.findall(r"^\s*(\w+) = ", fh.read(), re.M))

    ids = names("roblox/src/shared/AnimationIds.luau")
    meta = set(re.findall(r"^\t(\w+) = \{ looped", open(os.path.join(ROOT, "roblox/src/shared/AnimationMeta.luau")).read(), re.M))
    rbxmx = {f[:-6] for f in os.listdir(os.path.join(ROOT, "output/rbxmx")) if f.endswith(".rbxmx")}
    for n in sorted(ids - rbxmx):
        errs.append(f"AnimationIds lists {n!r} but output/rbxmx/{n}.rbxmx is missing")
    for n in sorted(ids - meta):
        errs.append(f"AnimationIds lists {n!r} but AnimationMeta has no entry")
    for n in sorted(rbxmx - ids):
        errs.append(f"output/rbxmx/{n}.rbxmx has no AnimationIds entry")
    for n in sorted(rbxmx):
        root = ET.parse(os.path.join(ROOT, "output/rbxmx", f"{n}.rbxmx")).getroot()
        seq = root.find("Item")
        if seq is None or seq.get("class") != "KeyframeSequence":
            errs.append(f"{n}.rbxmx: top item is not a KeyframeSequence")
            continue
        for kf in seq.findall("Item[@class='Keyframe']"):
            poses = {p.find("Properties/string").text for p in kf.iter("Item") if p.get("class") == "Pose"}
            if poses != R15:
                errs.append(f"{n}.rbxmx: keyframe pose set mismatch {sorted(poses ^ R15)}")
                break
    for e in errs:
        print("ERROR", e)
    print(f"checked {len(rbxmx)} KeyframeSequences, {len(ids)} AnimationIds, {len(meta)} AnimationMeta entries:",
          "OK" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
