"""Build a .blend for one animation spec: R15 rig, render scene, and the keyed action."""
import importlib
import math
import os

import bpy
from mathutils import Vector

from pipeline import curves
from rig.r15_rig import JOINT_LIMITS, build_rig, set_props_visible

ALL_ANIMATIONS = [
    "idle", "walk", "run", "jump",
    "punch", "sword_slash", "hit_react",
    "wave", "dance", "cheer",
    "fall", "climb", "swim", "swim_idle", "sit",
    "block", "kick", "combo", "death",
    "point", "laugh", "clap", "salute",
    "crouch_idle", "crouch_walk",
]
SETS = {
    "locomotion": ["idle", "walk", "run", "jump"],
    "combat": ["punch", "sword_slash", "hit_react"],
    "emotes": ["wave", "dance", "cheer"],
    "movement_states": ["fall", "climb", "swim", "swim_idle", "sit"],
    "combat_2": ["block", "kick", "combo", "death"],
    "emotes_2": ["point", "laugh", "clap", "salute"],
    "crouch": ["crouch_idle", "crouch_walk"],
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work")


def load_spec(name):
    return importlib.import_module(f"animations.specs.{name}").SPEC


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_render_scene():
    scene = bpy.context.scene
    coll = scene.collection
    # Floor with a 1-stud checker, so foot sliding is visible.
    mesh = bpy.data.meshes.new("Floor")
    s = 8.0
    mesh.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    floor = bpy.data.objects.new("Floor", mesh)
    coll.objects.link(floor)
    mat = bpy.data.materials.new("FloorChecker")
    mat.use_nodes = True
    nt = mat.node_tree
    checker = nt.nodes.new("ShaderNodeTexChecker")
    checker.inputs["Scale"].default_value = 2 * s / 2.0  # 2-stud squares
    checker.inputs["Color1"].default_value = (0.82, 0.82, 0.80, 1)
    checker.inputs["Color2"].default_value = (0.62, 0.62, 0.60, 1)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(coord.outputs["UV"], checker.inputs["Vector"])
    bsdf = nt.nodes["Principled BSDF"]
    nt.links.new(checker.outputs["Color"], bsdf.inputs["Base Color"])
    mesh.uv_layers.new(name="UVMap")
    for i, loop in enumerate(mesh.loops):
        co = mesh.vertices[loop.vertex_index].co
        mesh.uv_layers[0].data[i].uv = ((co.x + s) / (2 * s), (co.y + s) / (2 * s))
    mesh.materials.append(mat)
    # Thin dark slab under the floor, so the ground line shows in the edge-on side view.
    slab_mesh = bpy.data.meshes.new("FloorEdge")
    t = 0.06
    slab_mesh.from_pydata(
        [(x, y, z) for x in (-s, s) for y in (-s, s) for z in (-t, -0.002)], [],
        [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)],
    )
    slab = bpy.data.objects.new("FloorEdge", slab_mesh)
    smat = bpy.data.materials.new("FloorEdge")
    smat.use_nodes = True
    smat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.18, 0.18, 0.2, 1)
    slab_mesh.materials.append(smat)
    coll.objects.link(slab)

    # Cameras: a front three-quarter perspective view and an orthographic right-side view.
    cam34 = bpy.data.objects.new("Cam34", bpy.data.cameras.new("Cam34"))
    cam34.location = (7.5, -11.0, 4.6)
    cam34.data.lens = 50
    _look_at(cam34, (0, -0.3, 2.3))
    coll.objects.link(cam34)
    side = bpy.data.objects.new("CamSide", bpy.data.cameras.new("CamSide"))
    side.location = (-14.0, 0, 2.6)
    side.data.type = "ORTHO"
    side.data.ortho_scale = 8.5
    _look_at(side, (0, 0, 2.6))
    coll.objects.link(side)
    scene.camera = cam34

    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 3.2
    sun.data.angle = math.radians(8)
    sun.rotation_euler = (math.radians(40), math.radians(-25), math.radians(-35))
    coll.objects.link(sun)
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.55, 0.6, 0.68, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    scene.world = world

    r = scene.render
    r.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 12
    scene.cycles.use_denoising = False
    scene.cycles.max_bounces = 2
    r.resolution_x = 220
    r.resolution_y = 220
    r.film_transparent = False
    r.use_persistent_data = True
    r.image_settings.file_format = "PNG"


def apply_spec(arm, spec):
    """Key the spec onto a fresh action. Values in degrees and studs."""
    action = bpy.data.actions.new(spec["name"])
    arm.animation_data_create()
    arm.animation_data.action = action
    slot = action.slots.new(id_type="OBJECT", name=arm.name)
    arm.animation_data.action_slot = slot
    if not action.layers:
        layer = action.layers.new("Layer")
        layer.strips.new(type="KEYFRAME")
    for bone, chans in spec["keys"].items():
        for ch, keys in chans.items():
            fc = curves.get_or_create_fcurve(bone, ch, arm)
            for k in keys:
                frame, value = k[0], k[1]
                interp = k[2] if len(k) > 2 else "BEZIER"
                curves.set_key(fc, ch, frame, value, interpolation=interp)
            fc.update()
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = spec["frame_end"]
    scene.render.fps = spec.get("fps", 30)
    scene["anim_name"] = spec["name"]
    scene["loop"] = bool(spec.get("loop", False))
    scene["priority"] = spec.get("priority", "Action")
    scene["props"] = ",".join(spec.get("props", []))
    scene["description"] = spec.get("description", "")
    # What should touch the floor: "feet" (default), "none" (airborne, climbing, swimming, seated)
    # or "body" (lying on the floor).
    scene["contact"] = spec.get("contact", "feet")
    set_props_visible(spec.get("props", []))


def check_spec_limits(spec):
    problems = []
    for bone, chans in spec["keys"].items():
        for ch, keys in chans.items():
            lim = JOINT_LIMITS.get(bone, {}).get(ch)
            if not lim:
                continue
            for k in keys:
                if not (lim[0] <= k[1] <= lim[1]):
                    problems.append(f"{spec['name']}: {bone}.{ch}={k[1]} @ {k[0]} outside {lim}")
    return problems


def blend_path(name, iteration):
    return os.path.join(WORK, name, f"iter_{iteration}.blend")


def build(name):
    spec = load_spec(name)
    reset_scene()
    arm = build_rig(with_sword=True)
    setup_render_scene()
    apply_spec(arm, spec)
    path = blend_path(name, 0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=path)
    return path, check_spec_limits(spec)


def open_iteration(name, iteration):
    bpy.ops.wm.open_mainfile(filepath=blend_path(name, iteration))


if __name__ == "__main__":
    import sys

    for n in sys.argv[1:] or ALL_ANIMATIONS:
        p, probs = build(n)
        print("built", p, *probs, sep="\n  ")
