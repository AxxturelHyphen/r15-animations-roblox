"""Export final animations for Roblox.

  python -m pipeline.export walk:3 run:2 ...   (animation:iteration; omit :N to use the latest iteration)

Writes:
  output/fbx/<anim>.fbx      armature-only FBX with baked animation, for the Avatar/Animation Editor FBX import
  output/rbxmx/<anim>.rbxmx  a KeyframeSequence (baked every frame, linear easing) you can drop straight into Studio
  output/blend/<anim>.blend  the final Blender file (rig + action + review scene)
  output/meta/<anim>.json    loop, priority, length, markers and authored ground speed
  roblox/src/shared/AnimationMeta.luau   all meta JSON combined, for the Rojo project
"""
import json
import glob
import os
import re
import shutil
import sys
from xml.sax.saxutils import escape

import bpy
from mathutils import Matrix

from animations.markers import MARKERS
from pipeline import build, curves
from rig.r15_rig import ARMATURE_NAME, PARTS

OUT = os.path.join(build.ROOT, "output")
PRIORITY = {"Idle": 0, "Movement": 1, "Action": 2, "Action2": 3, "Action3": 4, "Action4": 5, "Core": 1000}
# Blender (x right=char-left, y back, z up), char faces -Y  ->  Roblox (x char-right... ) faces -Z, Y up.
M = Matrix(((-1, 0, 0), (0, 0, 1), (0, 1, 0)))


def latest_iteration(name):
    its = [int(re.search(r"iter_(\d+)\.blend$", p).group(1)) for p in glob.glob(os.path.join(build.WORK, name, "iter_*.blend"))]
    return max(its)


def _children(parent):
    return [n for n, v in PARTS.items() if v[0] == parent]


def _pose_xml(arm, bone, indent, ref):
    pb = arm.pose.bones[bone]
    B = arm.data.bones[bone].matrix_local.to_3x3()
    basis = pb.matrix_basis
    R = M @ (B @ basis.to_3x3() @ B.transposed()) @ M.transposed()
    p = M @ (B @ basis.to_translation())
    pad = " " * indent
    cf = "".join(f"<{k}>{v:.6f}</{k}>" for k, v in (("X", p.x), ("Y", p.y), ("Z", p.z)))
    cf += "".join(f"<R{i}{j}>{R[i][j]:.6f}</R{i}{j}>" for i in range(3) for j in range(3))
    lines = [f'{pad}<Item class="Pose" referent="RBX{next(ref):08X}">',
             f"{pad} <Properties>",
             f'{pad}  <CoordinateFrame name="CFrame">{cf}</CoordinateFrame>',
             f'{pad}  <token name="EasingDirection">0</token>',
             f'{pad}  <token name="EasingStyle">0</token>',
             f'{pad}  <string name="Name">{bone}</string>',
             f'{pad}  <float name="Weight">1</float>',
             f"{pad} </Properties>"]
    for c in _children(bone):
        lines += _pose_xml(arm, c, indent + 1, ref)
    lines.append(f"{pad}</Item>")
    return lines


def _frac_range(scene, fr):
    length = scene.frame_end - scene.frame_start
    return (int(round(scene.frame_start + fr[0] * length)), int(round(scene.frame_start + fr[1] * length)))


def resolve_markers(name):
    """Resolve animations/markers.py rules against the current (final) curves -> [(frame, name, value)]."""
    from mathutils import Vector

    scene = bpy.context.scene
    fmap = curves.fcurve_map()
    out = []
    for marker, rule in MARKERS.get(name, []):
        kind = rule[0]
        if kind in ("extreme", "speed_peak"):
            bone, ch = rule[1], rule[2]
            fc = fmap[(bone, ch)]
            a, b = _frac_range(scene, rule[-1])
            vals = {f: curves.evaluate(fc, ch, f) for f in range(a, b + 1)}
            if kind == "extreme":
                pick = max if rule[3] == "max" else min
                frame = pick(vals, key=vals.get)
            else:
                frame = max(range(a + 1, b + 1), key=lambda f: abs(vals[f] - vals[f - 1]))
            out.append((frame, marker, ""))
        elif kind == "footsteps":
            lows = {"Left": [], "Right": []}
            for f in range(scene.frame_start, scene.frame_end + 1):
                scene.frame_set(f)
                for side in lows:
                    obj = bpy.data.objects[f"{side}Foot"]
                    lows[side].append(min((obj.matrix_world @ Vector(v.co)).z for v in obj.data.vertices))
            # A footstep is the support hand-off: the frame where the other foot becomes the lowest.
            n = scene.frame_end - scene.frame_start
            low_side = ["Left" if lows["Left"][i] <= lows["Right"][i] else "Right" for i in range(n + 1)]
            # Debounce: heel-toe rolls make the lowest foot flicker, so a hand-off only counts when the new
            # foot stays lowest for a sixth of the clip.
            hold = max(3, n // 6)
            loop = bool(scene.get("loop"))

            def side_at(i):
                return low_side[i % n] if loop else low_side[min(max(i, 0), n)]

            stable = [side_at(i) if all(side_at(i + k) == side_at(i) for k in range(hold)) else None
                      for i in range(n)]
            current = None
            for i in range(-n if loop else 0, n):
                st = stable[i % n] if loop else stable[i]
                if st and st != current:
                    if current is not None and i >= 0:
                        out.append((scene.frame_start + i, marker, st))
                    current = st
    return sorted(out)


def authored_speed(name, iteration):
    """Ground speed (studs/s) the cycle was animated for: mean planted-foot speed x fps (locomotion only)."""
    path = os.path.join(build.WORK, name, f"iter_{iteration}", "metrics.json")
    if name not in ("walk", "run", "crouch_walk") or not os.path.exists(path):
        return None
    with open(path) as fh:
        m = json.load(fh)
    total, weight = 0.0, 0
    for foot in ("LeftFoot", "RightFoot"):
        for seg in m["feet"][foot]["contact_segments"]:
            span = seg["frames"][1] - seg["frames"][0]
            if span >= 3 and seg["moves_backward"]:
                total += seg["mean_speed"] * span
                weight += span
    return round(total / weight * m["fps"], 3) if weight else None


def export_rbxmx(name, path, markers=()):
    scene = bpy.context.scene
    arm = bpy.data.objects[ARMATURE_NAME]
    fps = scene.render.fps
    counter = iter(range(1, 10 ** 8))
    lines = ['<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
             'xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">',
             " <External>null</External>", " <External>nil</External>",
             f' <Item class="KeyframeSequence" referent="RBX{next(counter):08X}">',
             "  <Properties>",
             f'   <float name="AuthoredHipHeight">2</float>',
             f'   <bool name="Loop">{"true" if scene.get("loop") else "false"}</bool>',
             f'   <string name="Name">{escape(name)}</string>',
             f'   <token name="Priority">{PRIORITY.get(scene.get("priority", "Action"), 2)}</token>',
             "  </Properties>"]
    for f in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(f)
        lines += [f'  <Item class="Keyframe" referent="RBX{next(counter):08X}">',
                  "   <Properties>",
                  '    <string name="Name">Keyframe</string>',
                  f'    <float name="Time">{(f - scene.frame_start) / fps:.6f}</float>',
                  "   </Properties>"]
        lines += _pose_xml(arm, "HumanoidRootPart", 3, counter)
        for mf, mname, mval in markers:
            if mf == f:
                lines += [f'   <Item class="KeyframeMarker" referent="RBX{next(counter):08X}">',
                          "    <Properties>",
                          f'     <string name="Name">{escape(mname)}</string>',
                          f'     <string name="Value">{escape(mval)}</string>',
                          "    </Properties>",
                          "   </Item>"]
        lines.append("  </Item>")
    lines += [" </Item>", "</roblox>"]
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def export_fbx(path):
    scene = bpy.context.scene
    for o in bpy.data.objects:
        o.select_set(False)
    arm = bpy.data.objects[ARMATURE_NAME]
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=True, object_types={"ARMATURE"}, add_leaf_bones=False,
        bake_anim=True, bake_anim_use_all_actions=False, bake_anim_use_nla_strips=False,
        bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=0.0,
        axis_forward="-Z", axis_up="Y", apply_scale_options="FBX_SCALE_NONE", global_scale=1.0,
        armature_nodetype="NULL", primary_bone_axis="Y", secondary_bone_axis="X",
    )


def export(name, iteration=None):
    iteration = latest_iteration(name) if iteration is None else iteration
    build.open_iteration(name, iteration)
    for sub in ("fbx", "rbxmx", "blend", "meta"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    scene = bpy.context.scene
    markers = resolve_markers(name)
    meta = {
        "name": name,
        "iteration": iteration,
        "looped": bool(scene.get("loop")),
        "priority": scene.get("priority", "Action"),
        "length": round((scene.frame_end - scene.frame_start) / scene.render.fps, 4),
        "authoredSpeed": authored_speed(name, iteration),
        "markers": [{"name": n, "value": v, "time": round((f - scene.frame_start) / scene.render.fps, 4)}
                    for f, n, v in markers],
    }
    with open(os.path.join(OUT, "meta", f"{name}.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    export_rbxmx(name, os.path.join(OUT, "rbxmx", f"{name}.rbxmx"), markers)
    export_fbx(os.path.join(OUT, "fbx", f"{name}.fbx"))
    shutil.copy(build.blend_path(name, iteration), os.path.join(OUT, "blend", f"{name}.blend"))
    return iteration


def verify(name):
    """Re-import the FBX into an empty scene and parse the rbxmx. Returns a list of problems."""
    import xml.etree.ElementTree as ET

    problems = []
    build.reset_scene()
    bpy.ops.import_scene.fbx(filepath=os.path.join(OUT, "fbx", f"{name}.fbx"))
    arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    if len(arms) != 1:
        problems.append(f"expected 1 armature, got {len(arms)}")
    else:
        names = {b.name for b in arms[0].data.bones}
        missing = set(PARTS) - names
        if missing:
            problems.append(f"missing bones {sorted(missing)}")
        act = arms[0].animation_data.action if arms[0].animation_data else None
        if act is None:
            problems.append("no action in FBX")
        fr = tuple(act.frame_range) if act else None
    root = ET.parse(os.path.join(OUT, "rbxmx", f"{name}.rbxmx")).getroot()
    seq = root.find("Item")
    kfs = seq.findall("Item")
    poses = kfs[0].findall(".//Item[@class='Pose']")
    pose_names = {p.find("Properties/string").text for p in poses}
    if pose_names != set(PARTS):
        problems.append(f"rbxmx pose set mismatch: {sorted(set(PARTS) ^ pose_names)}")
    return problems, {"fbx_frame_range": fr if arms else None, "rbxmx_keyframes": len(kfs),
                      "duration_s": float(kfs[-1].find("Properties/float").text)}


def write_meta_luau():
    """Combine output/meta/*.json into the Rojo project's AnimationMeta ModuleScript."""
    rows = []
    for name in build.ALL_ANIMATIONS:
        p = os.path.join(OUT, "meta", f"{name}.json")
        if not os.path.exists(p):
            print(f"WARNING: no output/meta/{name}.json; '{name}' is left out of AnimationMeta.luau (export it first)")
            continue
        with open(p) as fh:
            m = json.load(fh)
        markers = ", ".join(f'{{ name = "{x["name"]}", value = "{x["value"]}", time = {x["time"]} }}' for x in m["markers"])
        speed = "nil" if m["authoredSpeed"] is None else m["authoredSpeed"]
        rows.append(f'\t{name} = {{ looped = {str(m["looped"]).lower()}, priority = Enum.AnimationPriority.{m["priority"]}, '
                    f'length = {m["length"]}, authoredSpeed = {speed}, markers = {{ {markers} }} }},')
    dest = os.path.join(build.ROOT, "roblox", "src", "shared", "AnimationMeta.luau")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as fh:
        fh.write("--!strict\n-- GENERATED by pipeline/export.py. Do not edit by hand; re-run `python -m pipeline.export`.\n"
                 "-- authoredSpeed: ground speed (studs/s) the cycle was animated for; playback speed = actual / authored.\n\n"
                 "export type Marker = { name: string, value: string, time: number }\n"
                 "export type Meta = { looped: boolean, priority: Enum.AnimationPriority, length: number, "
                 "authoredSpeed: number?, markers: { Marker } }\n\n"
                 "local AnimationMeta: { [string]: Meta } = {\n" + "\n".join(rows) + "\n}\n\nreturn AnimationMeta\n")
    return dest


if __name__ == "__main__":
    args = sys.argv[1:] or build.ALL_ANIMATIONS
    for a in args:
        n, _, it = a.partition(":")
        used = export(n, int(it) if it else None)
        probs, info = verify(n)
        print(f"{n} (iter {used}): {info} {'OK' if not probs else probs}")
    print("wrote", os.path.relpath(write_meta_luau(), build.ROOT))
