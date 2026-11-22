"""Apply a critic report's typed fix operations to the F-curves of one animation.

  python -m pipeline.apply_fixes walk 0     # reads reports/walk/iter_0.json, writes work/walk/iter_1.blend

Order of application: pose/curve ops in report order, then retime ops, then plant_feet,
then joint-limit clamping. Every change is logged to reports/<anim>/iter_N_applied.log.
"""
import json
import math
import os
import sys

import bpy

from pipeline import build, curves, validate_report
from rig.r15_rig import ANIMATED_BONES, CHANNELS, JOINT_LIMITS, ROT_CHANNELS

REPORTS = os.path.join(build.ROOT, "reports")
OPS = {"retime", "set_pose", "add_breakdown", "offset_channel", "scale_amplitude", "set_easing",
       "offset_overlap", "smooth_transition", "plant_feet"}
LATE_OPS = ("retime", "plant_feet")


class FixError(ValueError):
    pass


class Ctx:
    def __init__(self, log):
        self.scene = bpy.context.scene
        self.log = log
        self.loop = bool(self.scene.get("loop", False))

    @property
    def f0(self):
        return self.scene.frame_start

    @property
    def f1(self):
        return self.scene.frame_end

    def bones(self, spec):
        if spec in (None, "all"):
            return list(ANIMATED_BONES)
        if isinstance(spec, str):
            spec = [spec]
        for b in spec:
            if b not in ANIMATED_BONES:
                raise FixError(f"unknown bone {b!r}")
        return spec

    def chans(self, spec):
        if spec in (None, "all"):
            return list(CHANNELS)
        if isinstance(spec, str):
            spec = [spec]
        for c in spec:
            if c not in CHANNELS:
                raise FixError(f"unknown channel {c!r}")
        return spec

    def curves_for(self, bones, chans, create=False):
        fmap = curves.fcurve_map()
        out = []
        for b in bones:
            for c in chans:
                fc = fmap.get((b, c))
                if fc is None and create:
                    fc = curves.get_or_create_fcurve(b, c)
                    # Start the new curve as a flat rest-pose curve over the whole clip.
                    curves.set_key(fc, c, self.f0, 0.0)
                    curves.set_key(fc, c, self.f1, 0.0)
                if fc is not None:
                    out.append((b, c, fc))
        return out

    def rng(self, op):
        r = op.get("range") or op.get("frames")
        if r is None:
            return self.f0, self.f1
        return float(r[0]), float(r[1])


def _snapshot(fc):
    return [(kp.co[0], kp.co[1], kp.interpolation, kp.handle_left_type, kp.easing) for kp in fc.keyframe_points]


def _rebuild(fc, keys):
    """Replace all keyframes of fc with keys = [(frame, internal_value, interp, handle, easing)]."""
    merged = {}
    for k in keys:
        merged[round(k[0], 3)] = k
    while len(fc.keyframe_points):
        fc.keyframe_points.remove(fc.keyframe_points[0], fast=True)
    for f in sorted(merged):
        _, v, interp, handle, easing = merged[f]
        kp = fc.keyframe_points.insert(f, v, options={"FAST"})
        kp.interpolation = interp
        kp.handle_left_type = handle
        kp.handle_right_type = handle
        kp.easing = easing
    fc.update()


def _ensure_cycles(fc):
    if not any(m.type == "CYCLES" for m in fc.modifiers):
        fc.modifiers.new("CYCLES")


def _value_or_delta(op, fc, ch, frame):
    if "value" in op:
        return float(op["value"])
    if "delta" in op:
        return curves.evaluate(fc, ch, frame) + float(op["delta"])
    raise FixError("needs 'value' or 'delta'")


# --- ops -------------------------------------------------------------------------------------------

def op_set_pose(ctx, op):
    bone, ch, frame = op["bone"], op.get("ch") or op.get("channel"), float(op["frame"])
    ctx.bones([bone]), ctx.chans([ch])
    if not (ctx.f0 <= frame <= ctx.f1):
        raise FixError(f"frame {frame} outside clip")
    (_, _, fc), = ctx.curves_for([bone], [ch], create=True)
    v = _value_or_delta(op, fc, ch, frame)
    old = curves.evaluate(fc, ch, frame)
    curves.set_key(fc, ch, frame, v, interpolation=op.get("interpolation", "BEZIER"))
    if ctx.loop and frame in (ctx.f0, ctx.f1):  # keep the seam closed
        curves.set_key(fc, ch, ctx.f1 if frame == ctx.f0 else ctx.f0, v)
    fc.update()
    ctx.log(f"set_pose {bone}.{ch} @ {frame:g}: {old:.2f} -> {v:.2f}")


def op_add_breakdown(ctx, op):
    if "overshoot" in op:
        bone, ch = op["bone"], op.get("ch") or op.get("channel")
        (_, _, fc), = ctx.curves_for([bone], [ch], create=True)
        k = float(op["key_frame"])
        settle = float(op.get("settle_frames", 3))
        target = curves.evaluate(fc, ch, k)
        prev = curves.evaluate(fc, ch, max(ctx.f0, k - 2))
        direction = 1 if target >= prev else -1
        over = target + direction * abs(float(op["overshoot"]))
        sf = min(ctx.f1, k + settle)
        settle_val = curves.evaluate(fc, ch, sf)
        curves.set_key(fc, ch, k, over)
        if not any(abs(kp.co[0] - sf) < 1e-3 for kp in fc.keyframe_points):
            curves.set_key(fc, ch, sf, target if settle_val == over else settle_val)
        fc.update()
        ctx.log(f"overshoot {bone}.{ch} @ {k:g}: {target:.2f} -> {over:.2f}, settles by {sf:g}")
    else:
        op_set_pose(ctx, op)


def op_offset_channel(ctx, op):
    a, b = ctx.rng(op)
    d = float(op["delta"])
    for bone, ch, fc in ctx.curves_for(ctx.bones(op.get("bones") or op.get("bone")), ctx.chans(op.get("ch") or op.get("channel")), create=True):
        n = 0
        for kp in fc.keyframe_points:
            if a - 1e-3 <= kp.co[0] <= b + 1e-3:
                kp.co[1] += curves.to_internal(ch, d)
                n += 1
        fc.update()
        ctx.log(f"offset_channel {bone}.{ch} [{a:g},{b:g}] {d:+g} on {n} keys")


def op_scale_amplitude(ctx, op):
    a, b = ctx.rng(op)
    factor = float(op["factor"])
    pivot = op.get("pivot", "mean")
    for bone, ch, fc in ctx.curves_for(ctx.bones(op.get("bones") or op.get("bone")), ctx.chans(op.get("ch") or op.get("channel"))):
        kps = [kp for kp in fc.keyframe_points if a - 1e-3 <= kp.co[0] <= b + 1e-3]
        if not kps:
            continue
        if pivot == "mean":
            p = sum(kp.co[1] for kp in kps) / len(kps)
        elif pivot == "rest":
            p = 0.0
        else:
            p = curves.to_internal(ch, float(pivot))
        for kp in kps:
            kp.co[1] = p + (kp.co[1] - p) * factor
        fc.update()
        ctx.log(f"scale_amplitude {bone}.{ch} [{a:g},{b:g}] x{factor:g} about {pivot}")


def op_set_easing(ctx, op):
    a, b = ctx.rng(op)
    interp = op.get("interpolation", "BEZIER")
    handle = op.get("handle", "AUTO_CLAMPED")
    easing = op.get("easing", "AUTO")
    for bone, ch, fc in ctx.curves_for(ctx.bones(op.get("bones") or op.get("bone")), ctx.chans(op.get("ch") or op.get("channel"))):
        n = 0
        for kp in fc.keyframe_points:
            if a - 1e-3 <= kp.co[0] <= b + 1e-3:
                kp.interpolation = interp
                kp.easing = easing
                kp.handle_left_type = handle
                kp.handle_right_type = handle
                n += 1
        fc.update()
        ctx.log(f"set_easing {bone}.{ch} [{a:g},{b:g}] {interp}/{handle}/{easing} on {n} keys")


def op_offset_overlap(ctx, op):
    """Delay (positive) or lead (negative) whole curves by N frames for drag and follow-through."""
    n = float(op.get("offset", op.get("frames")))
    L = ctx.f1 - ctx.f0
    for bone, ch, fc in ctx.curves_for(ctx.bones(op.get("bones") or op.get("bone")), ctx.chans(op.get("ch") or op.get("channel"))):
        snap = _snapshot(fc)
        if ctx.loop:
            def orig(t):
                return fc.evaluate(ctx.f0 + ((t - ctx.f0) % L))
            vals_edges = orig(ctx.f0 - n)
            new = []
            for f, v, i, h, e in snap:
                if abs(f - ctx.f1) < 1e-3:
                    continue  # the end key duplicates frame 0
                nf = ctx.f0 + ((f + n - ctx.f0) % L)
                new.append((nf, v, i, h, e))
            new = [k for k in new if 1e-3 < k[0] - ctx.f0 < L - 1e-3]
            new.append((ctx.f0, vals_edges, "BEZIER", "AUTO_CLAMPED", "AUTO"))
            new.append((ctx.f1, vals_edges, "BEZIER", "AUTO_CLAMPED", "AUTO"))
            _rebuild(fc, new)
            _ensure_cycles(fc)
        else:
            start_v = fc.evaluate(ctx.f0)
            end_v = fc.evaluate(ctx.f1)
            new = [(ctx.f0, start_v, "BEZIER", "AUTO_CLAMPED", "AUTO")]
            for f, v, i, h, e in snap:
                if abs(f - ctx.f0) < 1e-3 or abs(f - ctx.f1) < 1e-3:
                    continue
                nf = f + n
                if ctx.f0 < nf < ctx.f1:
                    new.append((nf, v, i, h, e))
            new.append((ctx.f1, end_v, "BEZIER", "AUTO_CLAMPED", "AUTO"))
            _rebuild(fc, new)
        ctx.log(f"offset_overlap {bone}.{ch} by {n:+g} frames")


def op_smooth_transition(ctx, op):
    mode = op.get("mode", "smooth")
    a, b = ctx.rng(op)
    targets = ctx.curves_for(ctx.bones(op.get("bones") or op.get("bone")), ctx.chans(op.get("ch") or op.get("channel")))
    for bone, ch, fc in targets:
        if mode == "loop_seam":
            if not ctx.loop:
                raise FixError("loop_seam on a non-looping clip")
            v0 = fc.evaluate(ctx.f0)
            curves.set_key(fc, ch, ctx.f1, curves.to_display(ch, v0))
            for kp in fc.keyframe_points:
                if kp.co[0] in (ctx.f0, ctx.f1):
                    kp.interpolation = "BEZIER"
                    kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            _ensure_cycles(fc)
            fc.update()
            ctx.log(f"loop_seam {bone}.{ch}: closed + cyclic handles")
        elif mode == "remove_interior":
            snap = _snapshot(fc)
            keep = [k for k in snap if not (a + 1e-3 < k[0] < b - 1e-3)]
            if len(keep) < 2:
                continue
            removed = len(snap) - len(keep)
            _rebuild(fc, keep)
            ctx.log(f"remove_interior {bone}.{ch} ({a:g},{b:g}): removed {removed} keys")
        elif mode == "smooth":
            strength = float(op.get("strength", 0.5))
            step = float(op.get("step", 2))
            radius = int(op.get("radius", 2))
            frames = []
            f = a
            while f <= b + 1e-6:
                frames.append(f)
                f += step
            def sample(t):
                if ctx.loop:
                    t = ctx.f0 + ((t - ctx.f0) % (ctx.f1 - ctx.f0))
                return fc.evaluate(min(max(t, ctx.f0), ctx.f1))
            new_vals = []
            for t in frames:
                if (t <= ctx.f0 + 1e-3 or t >= ctx.f1 - 1e-3) and not ctx.loop:
                    new_vals.append((t, sample(t)))
                    continue
                w_sum, v_sum = 0.0, 0.0
                for d in range(-radius, radius + 1):
                    w = math.exp(-(d * d) / (2 * max(radius, 1) ** 2 / 2.0))
                    w_sum += w
                    v_sum += w * sample(t + d)
                avg = v_sum / w_sum
                new_vals.append((t, sample(t) * (1 - strength) + avg * strength))
            snap = _snapshot(fc)
            keep = [k for k in snap if not (a - 1e-3 <= k[0] <= b + 1e-3)]
            new = keep + [(t, v, "BEZIER", "AUTO_CLAMPED", "AUTO") for t, v in new_vals]
            if ctx.loop:
                # The seam keys must agree.
                vals = {round(k[0], 3): k for k in new}
                if ctx.f0 in vals or ctx.f1 in vals:
                    v0 = vals.get(ctx.f0, vals.get(ctx.f1))[1]
                    new = [k for k in new if k[0] not in (ctx.f0, ctx.f1)]
                    new += [(ctx.f0, v0, "BEZIER", "AUTO_CLAMPED", "AUTO"), (ctx.f1, v0, "BEZIER", "AUTO_CLAMPED", "AUTO")]
            _rebuild(fc, new)
            ctx.log(f"smooth {bone}.{ch} [{a:g},{b:g}] strength {strength:g} step {step:g}")
        else:
            raise FixError(f"unknown smooth_transition mode {mode!r}")


def op_retime(ctx, op):
    a, b = ctx.rng(op)
    scale = float(op.get("scale", 1.0))
    shift = float(op.get("shift", 0.0))
    ripple = bool(op.get("ripple", not ctx.loop))
    bones = op.get("bones", "all")
    all_bones = bones == "all"
    new_b = a + (b - a) * scale + shift
    delta_after = new_b - b
    if ctx.loop and all_bones and ripple:
        raise FixError("ripple-retiming every bone of a loop would change the cycle length; use ripple=false")
    for bone, ch, fc in ctx.curves_for(ctx.bones(bones), ctx.chans(op.get("ch") or op.get("channel"))):
        snap = _snapshot(fc)
        new = []
        for f, v, i, h, e in snap:
            if a - 1e-3 <= f <= b + 1e-3 and not (ctx.loop and f in (ctx.f0, ctx.f1)):
                nf = a + (f - a) * scale + shift
            elif f > b + 1e-3 and ripple:
                nf = f + delta_after
            else:
                nf = f
            new.append((round(nf, 2), v, i, h, e))
        if not ripple:
            # Do not let retimed keys cross their unmoved neighbours.
            outside = [k[0] for k in snap if not (a - 1e-3 <= k[0] <= b + 1e-3)]
            lo = max([x for x in outside if x < a] + [ctx.f0 - 1])
            hi = min([x for x in outside if x > b] + [ctx.f1 + 1])
            new = [k if (k[0] in outside) else ((min(max(k[0], lo + 0.5), hi - 0.5),) + k[1:]) for k in new]
        _rebuild(fc, new)
    if ripple and all_bones and abs(delta_after) > 1e-6:
        ctx.scene.frame_end = int(round(ctx.f1 + delta_after))
    ctx.log(f"retime bones={bones} [{a:g},{b:g}] scale {scale:g} shift {shift:+g} ripple={ripple} -> frame_end {ctx.scene.frame_end}")


def op_plant_feet(ctx, op):
    """Adjust LowerTorso.ly so the lowest point of either foot rests on the floor.

    mode "contact" only lifts or lowers frames where a foot should be planted (feet near the floor,
    within `tolerance`); mode "all" grounds every sampled frame (good for locomotion in place).
    """
    from mathutils import Vector

    a, b = ctx.rng(op)
    step = float(op.get("step", 2))
    mode = op.get("mode", "all")
    tol = float(op.get("tolerance", 0.25))
    (_, _, fc), = ctx.curves_for(["LowerTorso"], ["ly"], create=True)
    frames = []
    f = a
    while f <= b + 1e-6:
        frames.append(round(f, 2))
        f += step
    if frames[-1] != b:
        frames.append(b)
    corrections = []
    for f in frames:
        ctx.scene.frame_set(int(f), subframe=f - int(f))
        low = 1e9
        for foot in ("LeftFoot", "RightFoot"):
            obj = bpy.data.objects[foot]
            for v in obj.data.vertices:
                low = min(low, (obj.matrix_world @ Vector(v.co)).z)
        if mode == "contact" and low > tol:
            continue
        corrections.append((f, -low))
    smooth = float(op.get("smooth", 0.0))
    if smooth > 0 and len(corrections) > 2:
        ds = [d for _, d in corrections]
        n = len(ds)
        avg = []
        for i in range(n):
            if ctx.loop:
                nb = (ds[(i - 1) % n] + ds[i] + ds[(i + 1) % n]) / 3
            else:
                nb = (ds[max(i - 1, 0)] + ds[i] + ds[min(i + 1, n - 1)]) / 3
            avg.append(ds[i] * (1 - smooth) + nb * smooth)
        corrections = [(f, d) for (f, _), d in zip(corrections, avg)]
    # Read every original height before writing any key: each new key reshapes the curve,
    # so evaluating while keying would compound corrections.
    targets = [(f, curves.evaluate(fc, "ly", f) + d) for f, d in corrections]
    for f, v in targets:
        curves.set_key(fc, "ly", f, v)
    if ctx.loop:
        v0 = curves.evaluate(fc, "ly", ctx.f0)
        curves.set_key(fc, "ly", ctx.f1, v0)
        _ensure_cycles(fc)
    fc.update()
    worst = max((abs(d) for _, d in corrections), default=0)
    ctx.log(f"plant_feet [{a:g},{b:g}] step {step:g} mode {mode}: {len(corrections)} keys, max correction {worst:.3f} studs")


DISPATCH = {
    "retime": op_retime, "set_pose": op_set_pose, "add_breakdown": op_add_breakdown,
    "offset_channel": op_offset_channel, "scale_amplitude": op_scale_amplitude, "set_easing": op_set_easing,
    "offset_overlap": op_offset_overlap, "smooth_transition": op_smooth_transition, "plant_feet": op_plant_feet,
}


def clamp_limits(ctx):
    for (bone, ch), fc in curves.fcurve_map().items():
        lim = JOINT_LIMITS.get(bone, {}).get(ch)
        if not lim or ch not in ROT_CHANNELS:
            continue
        for kp in fc.keyframe_points:
            v = math.degrees(kp.co[1])
            if v < lim[0] or v > lim[1]:
                nv = min(max(v, lim[0]), lim[1])
                kp.co[1] = math.radians(nv)
                ctx.log(f"clamp {bone}.{ch} @ {kp.co[0]:g}: {v:.1f} -> {nv:.1f} (limit {lim})")
        fc.update()


def apply_report(name, iteration, rpath=None, out_iteration=None):
    rpath = rpath or os.path.join(REPORTS, name, f"iter_{iteration}.json")
    with open(rpath) as fh:
        report = json.load(fh)
    errs = validate_report.validate(report)
    log_lines = []

    def log(msg):
        log_lines.append(msg)

    for e in errs:
        log(f"SCHEMA: {e}")
    build.open_iteration(name, iteration)
    ctx = Ctx(log)
    early, late = [], []
    for fnd in report.get("findings", []):
        for op in fnd.get("fix", []):
            (late if op.get("op") in LATE_OPS else early).append((fnd.get("id", "?"), op))
    late.sort(key=lambda x: LATE_OPS.index(x[1]["op"]))
    applied = failed = 0
    for fid, op in early + late:
        fn = DISPATCH.get(op.get("op"))
        if fn is None:
            continue
        try:
            log(f"[{fid}] {json.dumps(op)}")
            fn(ctx, op)
            applied += 1
        except (FixError, KeyError, ValueError, TypeError) as exc:
            failed += 1
            log(f"  !! skipped: {exc!r}")
    clamp_limits(ctx)
    curves.refresh()
    out = build.blend_path(name, iteration + 1 if out_iteration is None else out_iteration)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    log(f"applied {applied} ops, skipped {failed}; saved {os.path.relpath(out, build.ROOT)}")
    os.makedirs(os.path.join(REPORTS, name), exist_ok=True)
    with open(os.path.join(REPORTS, name, f"iter_{iteration}_applied.log") if out_iteration is None else rpath + ".log", "w") as fh:
        fh.write("\n".join(log_lines) + "\n")
    return applied, failed


if __name__ == "__main__":
    name, it = sys.argv[1], int(sys.argv[2])
    print(name, it, apply_report(name, it))
