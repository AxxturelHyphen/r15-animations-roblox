"""Round-trip check: rebuild every frame of an exported .rbxmx with Roblox joint math
(world_child = world_parent * C0_offset * Pose.CFrame) and compare joint positions and
bone directions against the Blender pose.

  python -m pipeline.verify_rbxmx walk:3 punch:2 ...
"""
import os
import sys
import xml.etree.ElementTree as ET

import bpy
from mathutils import Matrix, Vector

from pipeline import build
from pipeline.export import M, OUT, latest_iteration
from rig.r15_rig import ARMATURE_NAME, PARTS


def _cf(pose):
    c = pose.find("Properties/CoordinateFrame")
    g = lambda k: float(c.find(k).text)
    m = Matrix([[g(f"R{i}{j}") for j in range(3)] for i in range(3)]).to_4x4()
    m.translation = Vector((g("X"), g("Y"), g("Z")))
    return m


def check(name, iteration):
    keyframes = ET.parse(os.path.join(OUT, "rbxmx", f"{name}.rbxmx")).getroot().find("Item").findall("Item")
    build.open_iteration(name, iteration)
    scene = bpy.context.scene
    arm = bpy.data.objects[ARMATURE_NAME]
    worst = 0.0
    for i, kf in enumerate(keyframes):
        world = {}

        def walk(pose, parent):
            n = pose.find("Properties/string").text
            if parent is None:
                world[n] = Matrix.Translation(M @ Vector(PARTS[n][2])) @ _cf(pose)
            else:
                off = M @ (Vector(PARTS[n][2]) - Vector(PARTS[parent][2]))
                world[n] = world[parent] @ Matrix.Translation(off) @ _cf(pose)
            for c in pose.findall("Item"):
                walk(c, n)

        walk(kf.find("Item"), None)
        scene.frame_set(scene.frame_start + i)
        for n in PARTS:
            pb = arm.pose.bones[n]
            head = M @ (arm.matrix_world @ pb.head)
            direction = M @ ((arm.matrix_world @ pb.tail) - (arm.matrix_world @ pb.head)).normalized()
            up = world[n].to_3x3() @ Vector((0, 1, 0))
            worst = max(worst, (world[n].translation - head).length, (up - direction).length)
    return len(keyframes), worst


if __name__ == "__main__":
    for a in sys.argv[1:] or build.ALL_ANIMATIONS:
        n, _, it = a.partition(":")
        frames, err = check(n, int(it) if it else latest_iteration(n))
        print(f"{n}: {frames} keyframes, max deviation {err:.2e} studs", "OK" if err < 1e-3 else "MISMATCH")
