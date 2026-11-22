"""Export final animations for Roblox.

  python -m pipeline.export walk:3 run:2 ...   (animation:iteration; omit :N to use the latest iteration)

Writes:
  output/fbx/<anim>.fbx      armature-only FBX with baked animation, for the Avatar/Animation Editor FBX import
  output/rbxmx/<anim>.rbxmx  a KeyframeSequence (baked every frame, linear easing) you can drop straight into Studio
  output/blend/<anim>.blend  the final Blender file (rig + action + review scene)
"""
import glob
import os
import re
import shutil
import sys
from xml.sax.saxutils import escape

import bpy
from mathutils import Matrix

from pipeline import build
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


def export_rbxmx(name, path):
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
    for sub in ("fbx", "rbxmx", "blend"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    export_rbxmx(name, os.path.join(OUT, "rbxmx", f"{name}.rbxmx"))
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


if __name__ == "__main__":
    args = sys.argv[1:] or build.ALL_ANIMATIONS
    for a in args:
        n, _, it = a.partition(":")
        used = export(n, int(it) if it else None)
        probs, info = verify(n)
        print(f"{n} (iter {used}): {info} {'OK' if not probs else probs}")
