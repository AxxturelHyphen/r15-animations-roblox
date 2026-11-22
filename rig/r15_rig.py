"""Procedural Roblox R15 rig for headless Blender (bpy).

Coordinate conventions (Blender world, 1 Blender unit = 1 Roblox stud):
  * +Z is up, the character FACES -Y, the character's LEFT side is +X.
  * Every bone points straight up (+Z) with roll 0, so all bones share the same
    rest orientation. Their local axes are:
        local X = world +X  (character's left)
        local Y = world +Z  (up)
        local Z = world -Y  (character's forward)

Animation channels (degrees for rotations, studs for locations), Euler XYZ:
  rx  rotation about the left/right axis.
        > 0 : a hanging limb's far end swings BACKWARD; an upright segment's
              top tips FORWARD.
        e.g. thigh forward (hip flexion) = UpperLeg rx < 0, knee bend = LowerLeg rx > 0,
             arm raised forward = UpperArm rx < 0, elbow bend = LowerArm rx < 0,
             torso lean forward = UpperTorso rx > 0, head nod down = Head rx > 0,
             toes pointed down = Foot rx > 0.
  ry  twist about the vertical axis. > 0 turns toward the character's LEFT.
  rz  rotation about the forward axis.
        > 0 : a hanging limb's far end moves toward the character's LEFT;
              an upright segment's top tips toward the character's RIGHT.
        e.g. left arm out to the side = LeftUpperArm rz > 0 (+90 = T-pose),
             right arm out to the side = RightUpperArm rz < 0.
  lx / ly / lz  translation: lx = toward the character's left, ly = up, lz = forward.

Bone names match the Roblox R15 part names, so the Motor6D joints are:
  Root(LowerTorso) Waist(UpperTorso) Neck(Head) *Shoulder(*UpperArm) *Elbow(*LowerArm)
  *Wrist(*Hand) *Hip(*UpperLeg) *Knee(*LowerLeg) *Ankle(*Foot)
"""
import math

import bpy
from mathutils import Matrix, Vector

ARMATURE_NAME = "R15Rig"

# Colours: the left limbs are warm orange and the right limbs are cool blue,
# so reviewers can tell the sides apart in renders.
C_TORSO = (0.12, 0.42, 0.40, 1.0)
C_HEAD = (0.93, 0.80, 0.62, 1.0)
C_LEFT = (0.95, 0.52, 0.18, 1.0)
C_RIGHT = (0.25, 0.48, 0.92, 1.0)
C_LEFT_LEG = (0.70, 0.36, 0.12, 1.0)
C_RIGHT_LEG = (0.16, 0.30, 0.66, 1.0)
C_DARK = (0.05, 0.05, 0.06, 1.0)

# name: (parent, joint_name, pivot(head), box_center, box_size(x, y_depth, z), colour)
PARTS = {
    "HumanoidRootPart": (None, None, (0, 0, 2.0), None, None, None),
    "LowerTorso": ("HumanoidRootPart", "Root", (0, 0, 2.0), (0, 0, 2.15), (2.0, 1.0, 0.45), C_TORSO),
    "UpperTorso": ("LowerTorso", "Waist", (0, 0, 2.35), (0, 0, 3.15), (2.0, 1.0, 1.55), C_TORSO),
    "Head": ("UpperTorso", "Neck", (0, 0, 3.95), (0, 0, 4.55), (1.2, 1.2, 1.2), C_HEAD),
    "LeftUpperArm": ("UpperTorso", "LeftShoulder", (1.5, 0, 3.75), (1.5, 0, 3.35), (0.9, 0.9, 1.15), C_LEFT),
    "LeftLowerArm": ("LeftUpperArm", "LeftElbow", (1.5, 0, 2.8), (1.5, 0, 2.35), (0.85, 0.85, 1.0), C_LEFT),
    "LeftHand": ("LeftLowerArm", "LeftWrist", (1.5, 0, 1.85), (1.5, 0, 1.65), (0.8, 0.8, 0.4), C_LEFT),
    "RightUpperArm": ("UpperTorso", "RightShoulder", (-1.5, 0, 3.75), (-1.5, 0, 3.35), (0.9, 0.9, 1.15), C_RIGHT),
    "RightLowerArm": ("RightUpperArm", "RightElbow", (-1.5, 0, 2.8), (-1.5, 0, 2.35), (0.85, 0.85, 1.0), C_RIGHT),
    "RightHand": ("RightLowerArm", "RightWrist", (-1.5, 0, 1.85), (-1.5, 0, 1.65), (0.8, 0.8, 0.4), C_RIGHT),
    "LeftUpperLeg": ("LowerTorso", "LeftHip", (0.5, 0, 1.95), (0.5, 0, 1.5), (0.95, 0.95, 0.95), C_LEFT_LEG),
    "LeftLowerLeg": ("LeftUpperLeg", "LeftKnee", (0.5, 0, 1.05), (0.5, 0, 0.65), (0.9, 0.9, 0.8), C_LEFT_LEG),
    "LeftFoot": ("LeftLowerLeg", "LeftAnkle", (0.5, 0, 0.3), (0.5, -0.15, 0.15), (0.9, 1.3, 0.3), C_LEFT_LEG),
    "RightUpperLeg": ("LowerTorso", "RightHip", (-0.5, 0, 1.95), (-0.5, 0, 1.5), (0.95, 0.95, 0.95), C_RIGHT_LEG),
    "RightLowerLeg": ("RightUpperLeg", "RightKnee", (-0.5, 0, 1.05), (-0.5, 0, 0.65), (0.9, 0.9, 0.8), C_RIGHT_LEG),
    "RightFoot": ("RightLowerLeg", "RightAnkle", (-0.5, 0, 0.3), (-0.5, -0.15, 0.15), (0.9, 1.3, 0.3), C_RIGHT_LEG),
}
BONES = list(PARTS.keys())
ANIMATED_BONES = [b for b in BONES if b != "HumanoidRootPart"]
MIRROR = {
    b: (b.replace("Left", "Right") if b.startswith("Left") else b.replace("Right", "Left"))
    for b in BONES
    if b.startswith(("Left", "Right"))
}

# Channel name -> (pose bone data path, array index)
CHANNELS = {
    "rx": ("rotation_euler", 0),
    "ry": ("rotation_euler", 1),
    "rz": ("rotation_euler", 2),
    "lx": ("location", 0),
    "ly": ("location", 1),
    "lz": ("location", 2),
}
CHANNEL_BY_PATH = {v: k for k, v in CHANNELS.items()}
ROT_CHANNELS = ("rx", "ry", "rz")

# Joint limits in degrees per bone channel (anatomical comfort range for the blocky rig).
_LIMB_LIMITS = {
    "UpperArm": {"rx": (-185, 70), "ry": (-90, 90)},
    "LowerArm": {"rx": (-150, 3), "ry": (-60, 60), "rz": (-60, 60)},
    "Hand": {"rx": (-75, 75), "ry": (-80, 80), "rz": (-45, 45)},
    "UpperLeg": {"rx": (-125, 50), "ry": (-45, 45)},
    "LowerLeg": {"rx": (-3, 150), "ry": (-12, 12), "rz": (-12, 12)},
    "Foot": {"rx": (-45, 55), "ry": (-25, 25), "rz": (-25, 25)},
}
JOINT_LIMITS = {
    # The Root joint may tip the whole body (swim lies prone, death falls on its back).
    "LowerTorso": {"rx": (-100, 100), "ry": (-60, 60), "rz": (-90, 90)},
    "UpperTorso": {"rx": (-35, 50), "ry": (-50, 50), "rz": (-35, 35)},
    "Head": {"rx": (-50, 60), "ry": (-80, 80), "rz": (-40, 40)},
}
for side in ("Left", "Right"):
    for part, lim in _LIMB_LIMITS.items():
        JOINT_LIMITS[side + part] = dict(lim)
# Side-dependent abduction (rz) limits: outward is +rz on the left, -rz on the right.
JOINT_LIMITS["LeftUpperArm"]["rz"] = (-35, 185)
JOINT_LIMITS["RightUpperArm"]["rz"] = (-185, 35)
JOINT_LIMITS["LeftUpperLeg"]["rz"] = (-25, 70)
JOINT_LIMITS["RightUpperLeg"]["rz"] = (-70, 25)


def _material(name, rgba):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = 0.65
    mat.diffuse_color = rgba
    return mat


def _box(name, center, size, rgba, collection):
    sx, sy, sz = (s / 2 for s in size)
    verts = [(x, y, z) for x in (-sx, sx) for y in (-sy, sy) for z in (-sz, sz)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    mesh.materials.append(_material("M_" + "_".join(f"{c:.2f}" for c in rgba[:3]), rgba))
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.location = center
    return obj


def _parent_to_bone(obj, arm_obj, bone_name):
    world = Matrix.Translation(obj.location)
    obj.parent = arm_obj
    obj.parent_type = "BONE"
    obj.parent_bone = bone_name
    bone = arm_obj.data.bones[bone_name]
    # Bone-parented children are relative to the bone TAIL in armature space.
    tail_mat = arm_obj.matrix_world @ Matrix.Translation(bone.tail_local) @ bone.matrix_local.to_3x3().to_4x4()
    obj.matrix_parent_inverse = tail_mat.inverted()
    obj.matrix_basis = world


def build_rig(with_sword=True):
    """Create the R15 armature + block meshes in the current scene. Returns the armature object."""
    scene = bpy.context.scene
    coll = scene.collection
    arm_data = bpy.data.armatures.new(ARMATURE_NAME)
    arm_obj = bpy.data.objects.new(ARMATURE_NAME, arm_data)
    coll.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    arm_obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for name, (parent, _joint, head, *_rest) in PARTS.items():
        eb = arm_data.edit_bones.new(name)
        eb.head = Vector(head)
        eb.tail = Vector(head) + Vector((0, 0, 0.3))
        eb.roll = 0.0
        if parent:
            eb.parent = arm_data.edit_bones[parent]
            eb.use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")

    for name, (_parent, joint, _head, center, size, rgba) in PARTS.items():
        pb = arm_obj.pose.bones[name]
        pb.rotation_mode = "XYZ"
        arm_data.bones[name]["roblox_joint"] = joint or ""
        if center is None:
            continue
        obj = _box(name, center, size, rgba, coll)
        _parent_to_bone(obj, arm_obj, name)

    # Face so the facing direction reads in renders.
    for side, x in (("L", 0.25), ("R", -0.25)):
        eye = _box(f"Eye{side}", (x, -0.61, 4.68), (0.16, 0.04, 0.26), C_DARK, coll)
        _parent_to_bone(eye, arm_obj, "Head")
    mouth = _box("Mouth", (0, -0.61, 4.3), (0.45, 0.04, 0.07), C_DARK, coll)
    _parent_to_bone(mouth, arm_obj, "Head")

    if with_sword:
        # The grip sits in the right hand. The blade points forward when the arm hangs.
        sword = []
        sword.append(_box("SwordGrip", (-1.5, -0.1, 1.6), (0.18, 0.7, 0.18), C_DARK, coll))
        sword.append(_box("SwordGuard", (-1.5, -0.5, 1.6), (0.7, 0.12, 0.2), (0.75, 0.62, 0.2, 1), coll))
        sword.append(_box("SwordBlade", (-1.5, -2.2, 1.6), (0.22, 3.3, 0.08), (0.85, 0.87, 0.9, 1), coll))
        for s in sword:
            _parent_to_bone(s, arm_obj, "RightHand")
            s["prop"] = "sword"
            s.hide_render = True
            s.hide_viewport = True

    bpy.context.view_layer.update()
    return arm_obj


def set_props_visible(props):
    for obj in bpy.data.objects:
        if "prop" in obj:
            vis = obj["prop"] in props
            obj.hide_render = not vis
            obj.hide_viewport = not vis


def get_armature():
    return bpy.data.objects[ARMATURE_NAME]


def deg(x):
    return math.radians(x)
