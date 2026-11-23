"""F-curve helpers for Blender 5 layered (slotted) actions."""
import math

import bpy
from bpy_extras import anim_utils

from rig.r15_rig import CHANNEL_BY_PATH, CHANNELS, ROT_CHANNELS, get_armature


def channelbag(arm=None, ensure=False):
    arm = arm or get_armature()
    ad = arm.animation_data
    if ensure:
        return anim_utils.action_ensure_channelbag_for_slot(ad.action, ad.action_slot)
    return anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)


def bone_of(fc):
    # data_path looks like: pose.bones["LeftUpperArm"].rotation_euler
    return fc.data_path.split('"')[1]


def channel_of(fc):
    prop = fc.data_path.rsplit(".", 1)[1]
    return CHANNEL_BY_PATH[(prop, fc.array_index)]


def fcurve_map(arm=None):
    """Return a dict mapping (bone, channel) to an fcurve."""
    cb = channelbag(arm)
    out = {}
    if cb is None:
        return out
    for fc in cb.fcurves:
        try:
            out[(bone_of(fc), channel_of(fc))] = fc
        except (IndexError, KeyError):
            continue
    return out


def get_or_create_fcurve(bone, channel, arm=None):
    cb = channelbag(arm, ensure=True)
    path, idx = CHANNELS[channel]
    data_path = f'pose.bones["{bone}"].{path}'
    fc = cb.fcurves.find(data_path, index=idx)
    if fc is None:
        fc = cb.fcurves.new(data_path, index=idx, group_name=bone)
    return fc


def to_internal(channel, value):
    return math.radians(value) if channel in ROT_CHANNELS else value


def to_display(channel, value):
    return math.degrees(value) if channel in ROT_CHANNELS else value


def evaluate(fc, channel, frame):
    return to_display(channel, fc.evaluate(frame))


def set_key(fc, channel, frame, value, interpolation="BEZIER", handle="AUTO_CLAMPED", easing="AUTO"):
    """Insert or replace a key (value in display units). Returns the keyframe point."""
    v = to_internal(channel, value)
    for kp in fc.keyframe_points:
        if abs(kp.co[0] - frame) < 1e-4:
            kp.co[1] = v
            break
    else:
        kp = fc.keyframe_points.insert(frame, v, options={"FAST"})
    kp.interpolation = interpolation
    kp.easing = easing
    kp.handle_left_type = handle
    kp.handle_right_type = handle
    return kp


def dump_keys(arm=None):
    """Serialise all keys: {bone: {channel: [[frame, value, interp, handle], ...]}}."""
    out = {}
    for (bone, ch), fc in sorted(fcurve_map(arm).items()):
        keys = []
        for kp in fc.keyframe_points:
            keys.append([round(kp.co[0], 2), round(to_display(ch, kp.co[1]), 3), kp.interpolation, kp.handle_left_type])
        cyc = any(m.type == "CYCLES" for m in fc.modifiers)
        out.setdefault(bone, {})[ch] = {"keys": keys, "cyclic": cyc}
    return out


def sample_all(frame_start, frame_end, arm=None, step=1.0):
    """Sample every channel at regular steps. Returns (frames, {(bone, ch): [values]})."""
    frames = []
    f = frame_start
    while f <= frame_end + 1e-6:
        frames.append(f)
        f += step
    data = {}
    for key, fc in fcurve_map(arm).items():
        data[key] = [evaluate(fc, key[1], fr) for fr in frames]
    return frames, data


def refresh(arm=None):
    for fc in fcurve_map(arm).values():
        fc.keyframe_points.sort()
        fc.update()
