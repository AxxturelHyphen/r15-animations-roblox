"""Objective per-frame motion metrics that go to the critic with the renders.

Units: degrees per frame (rotation channels) and studs per frame (location channels).
"""
import json
import math

import bpy
from mathutils import Vector

from pipeline import curves
from rig.r15_rig import ANIMATED_BONES, JOINT_LIMITS, MIRROR, ROT_CHANNELS

ACC_SPIKE_DEG = 9.0      # |second difference| that reads as a pop
ACC_SPIKE_LOC = 0.06
CORNER_DEG = 2.5         # velocity jump across a key (a linear/vector corner)
SEAM_VALUE_DEG = 0.5
SEAM_VEL_DEG = 1.2
HOLD_SPEED = 0.35        # whole-body deg/frame, below which the body counts as frozen
HOLD_MIN_FRAMES = 5
CONTACT_Z = 0.06
PENETRATION_Z = -0.05


def _series(fc, ch, f0, f1):
    return [curves.evaluate(fc, ch, f) for f in range(f0, f1 + 1)]


def _diff(v, cyclic):
    if cyclic:
        n = len(v) - 1  # the last frame duplicates the first
        return [v[(i + 1) % n] - v[i % n] for i in range(n)]
    return [v[i + 1] - v[i] for i in range(len(v) - 1)]


def _foot_samples(f0, f1):
    scene = bpy.context.scene
    out = {"LeftFoot": [], "RightFoot": []}
    for f in range(f0, f1 + 1):
        scene.frame_set(f)
        for foot in out:
            obj = bpy.data.objects[foot]
            pts = [obj.matrix_world @ Vector(v.co) for v in obj.data.vertices]
            low = min(pts, key=lambda p: p.z)
            cx = sum(p.x for p in pts) / len(pts)
            cy = sum(p.y for p in pts) / len(pts)
            out[foot].append((f, round(low.z, 4), round(cx, 4), round(cy, 4)))
    return out


def analyze():
    scene = bpy.context.scene
    f0, f1 = scene.frame_start, scene.frame_end
    loop = bool(scene.get("loop", False))
    name = scene.get("anim_name", "anim")
    fmap = curves.fcurve_map()
    res = {"animation": name, "frames": [f0, f1], "loop": loop, "fps": scene.render.fps}

    spikes, corners, seam, limits, ranges = [], [], [], [], {}
    body_speed = [0.0] * (f1 - f0 + (0 if loop else 0))
    series_cache = {}
    for (bone, ch), fc in sorted(fmap.items()):
        v = _series(fc, ch, f0, f1)
        series_cache[(bone, ch)] = v
        rot = ch in ROT_CHANNELS
        vel = _diff(v, loop)
        acc = _diff(vel + ([vel[0]] if loop else []), loop) if len(vel) > 1 else []
        thr = ACC_SPIKE_DEG if rot else ACC_SPIKE_LOC
        for i, a in enumerate(acc):
            if abs(a) > thr:
                spikes.append({"bone": bone, "ch": ch, "frame": f0 + i + 1, "accel": round(a, 3)})
        if rot:
            for i, s in enumerate(vel):
                if i < len(body_speed):
                    body_speed[i] += abs(s)
        # Velocity corners at keys (left and right derivatives disagree).
        for kp in fc.keyframe_points:
            k = kp.co[0]
            if k <= f0 or k >= f1:
                continue
            left = curves.evaluate(fc, ch, k) - curves.evaluate(fc, ch, k - 0.25)
            right = curves.evaluate(fc, ch, k + 0.25) - curves.evaluate(fc, ch, k)
            jump = abs(right - left) * 4
            if rot and jump > CORNER_DEG:
                corners.append({"bone": bone, "ch": ch, "frame": int(k), "vel_jump_deg_per_frame": round(jump, 2),
                                "interp": kp.interpolation})
        # Loop seam: values match and velocity continues smoothly through the loop point.
        if loop:
            vdiff = v[-1] - v[0]
            v_in = v[-1] - v[-2]
            v_out = v[1] - v[0]
            peak = max(abs(x) for x in vel) if vel else 0
            sthr = SEAM_VALUE_DEG if rot else 0.01
            vthr = SEAM_VEL_DEG if rot else 0.02
            issue = None
            seam_acc = v[1] - 2 * v[0] + v[-2]
            interior = [abs(v[i + 1] - 2 * v[i] + v[i - 1]) for i in range(1, len(v) - 1)]
            interior_max = max(interior) if interior else 0
            if abs(vdiff) > sthr:
                issue = "value_mismatch"
            elif abs(seam_acc) > max(1.5 * interior_max, vthr):
                issue = "kink_at_seam"
            elif rot and peak > 2.0 and abs(v_in) < 0.25 and abs(v_out) < 0.25 and abs(v[0] - min(v)) > 1 and abs(v[0] - max(v)) > 1:
                issue = "eases_to_stop_at_seam"
            if issue:
                seam.append({"bone": bone, "ch": ch, "issue": issue, "start": round(v[0], 3), "end": round(v[-1], 3),
                             "vel_in": round(v_in, 3), "vel_out": round(v_out, 3), "seam_accel": round(seam_acc, 3),
                             "max_interior_accel": round(interior_max, 3)})
        # Joint limits.
        lim = JOINT_LIMITS.get(bone, {}).get(ch)
        if lim:
            for i, x in enumerate(v):
                if x < lim[0] - 0.5 or x > lim[1] + 0.5:
                    limits.append({"bone": bone, "ch": ch, "frame": f0 + i, "value": round(x, 2), "limit": lim})
        ranges.setdefault(bone, {})[ch] = round(max(v) - min(v), 3)

    spikes.sort(key=lambda s: -abs(s["accel"]))
    res["accel_spikes"] = spikes[:25]
    res["accel_spike_count"] = len(spikes)
    res["velocity_corners"] = corners
    res["loop_seam_issues"] = seam
    res["joint_limit_violations"] = limits[:30]
    res["joint_limit_violation_count"] = len(limits)
    res["motion_range"] = ranges

    # Dead holds: the whole body is (almost) frozen.
    holds, start = [], None
    for i, s in enumerate(body_speed + [999]):
        if s < HOLD_SPEED and start is None:
            start = i
        elif s >= HOLD_SPEED and start is not None:
            if i - start >= HOLD_MIN_FRAMES:
                holds.append({"frames": [f0 + start, f0 + i], "length": i - start})
            start = None
    res["dead_holds"] = holds
    res["whole_body_speed_deg_per_frame"] = [round(s, 2) for s in body_speed]

    # Lockstep keys: interior frames where most animated bones are keyed together (no overlap).
    bone_keys = {}
    for (bone, ch), fc in fmap.items():
        bone_keys.setdefault(bone, set()).update(int(round(kp.co[0])) for kp in fc.keyframe_points)
    animated = [b for b in bone_keys if b in ANIMATED_BONES]
    counts = {}
    for b in animated:
        for k in bone_keys[b]:
            if f0 < k < f1:
                counts[k] = counts.get(k, 0) + 1
    lock = [{"frame": k, "bones_keyed": c, "of": len(animated)} for k, c in sorted(counts.items())
            if len(animated) >= 4 and c / len(animated) >= 0.6]
    res["lockstep_key_frames"] = lock
    total_keys = sum(counts.values()) or 1
    res["overlap_score"] = round(1 - sum(c for k, c in counts.items() if c / max(len(animated), 1) >= 0.6) / total_keys, 3)

    # Twinning: left/right curves that are identical (perfect symmetry looks robotic).
    twins = []
    for b in animated:
        m = MIRROR.get(b)
        if not m or not b.startswith("Left") or m not in bone_keys:
            continue
        for ch in ("rx", "ry", "rz"):
            a, c = series_cache.get((b, ch)), series_cache.get((m, ch))
            if not a or not c:
                continue
            sign = 1 if ch == "rx" else -1
            if max(abs(x - sign * y) for x, y in zip(a, c)) < 0.5 and (max(a) - min(a)) > 5:
                twins.append({"bones": [b, m], "ch": ch})
    res["twinning"] = twins

    # Feet: ground contact, penetration, sliding, floating.
    feet = _foot_samples(f0, f1)
    foot_res = {}
    for foot, samples in feet.items():
        contact = [s for s in samples if s[1] < CONTACT_Z]
        pen = [{"frame": s[0], "z": s[1]} for s in samples if s[1] < PENETRATION_Z]
        segs, cur = [], []
        for s in samples:
            if s[1] < CONTACT_Z:
                cur.append(s)
            else:
                if len(cur) >= 2:
                    segs.append(cur)
                cur = []
        if len(cur) >= 2:
            segs.append(cur)
        seg_out = []
        for seg in segs:
            steps = [math.hypot(b[2] - a[2], b[3] - a[3]) for a, b in zip(seg, seg[1:])]
            dy = [b[3] - a[3] for a, b in zip(seg, seg[1:])]
            seg_out.append({
                "frames": [seg[0][0], seg[-1][0]],
                "drift_studs": round(math.hypot(seg[-1][2] - seg[0][2], seg[-1][3] - seg[0][3]), 3),
                "mean_speed": round(sum(steps) / len(steps), 4),
                "speed_std": round((sum((x - sum(steps) / len(steps)) ** 2 for x in steps) / len(steps)) ** 0.5, 4),
                "moves_backward": sum(dy) > 0,  # +Y is backward for this character
            })
        foot_res[foot] = {
            "contact_frames": len(contact),
            "penetration": pen[:20],
            "penetration_count": len(pen),
            "contact_segments": seg_out,
            "lowest_z_per_frame": [s[1] for s in samples],
        }
    floating = [f0 + i for i in range(f1 - f0 + 1)
                if feet["LeftFoot"][i][1] > 0.1 and feet["RightFoot"][i][1] > 0.1]
    foot_res["both_feet_airborne_frames"] = floating
    res["feet"] = foot_res

    res["score"] = score(res)
    return res


def score(res):
    """Issue counts used for the before/after comparison (lower is better)."""
    slide = 0
    for foot in ("LeftFoot", "RightFoot"):
        for seg in res["feet"][foot]["contact_segments"]:
            if res["animation"] in ("walk", "run"):
                if seg["speed_std"] > 0.03:
                    slide += 1
            elif seg["drift_studs"] > 0.12:
                slide += 1
    return {
        "accel_spikes": res["accel_spike_count"],
        "velocity_corners": len(res["velocity_corners"]),
        "loop_seam_issues": len(res["loop_seam_issues"]),
        "joint_limit_violations": res["joint_limit_violation_count"],
        "dead_holds": len(res["dead_holds"]),
        "lockstep_key_frames": len(res["lockstep_key_frames"]),
        "twinned_channels": len(res["twinning"]),
        "foot_slide_segments": slide,
        "foot_penetration_frames": res["feet"]["LeftFoot"]["penetration_count"] + res["feet"]["RightFoot"]["penetration_count"],
        "floating_frames": 0 if res["animation"] in ("run", "jump") else len(res["feet"]["both_feet_airborne_frames"]),
        "overlap_score": res["overlap_score"],
    }


def write(path, res):
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
