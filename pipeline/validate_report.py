"""Validate a critic report against the fix contract.  python3 -m pipeline.validate_report <report.json>..."""
import json
import sys

REQUIRED_TOP = ("animation", "iteration", "verdict", "scores", "summary", "findings")
REQUIRED_OP = {
    "set_pose": ("bone", "ch", "frame"), "add_breakdown": ("bone", "ch"), "offset_channel": ("bones", "ch", "delta"),
    "scale_amplitude": ("bones", "factor"), "set_easing": ("bones",), "offset_overlap": ("bones", "offset"),
    "smooth_transition": ("bones", "mode"), "retime": ("range",), "plant_feet": (),
}
BONES = {"LowerTorso", "UpperTorso", "Head"} | {
    s + p for s in ("Left", "Right") for p in ("UpperArm", "LowerArm", "Hand", "UpperLeg", "LowerLeg", "Foot")}
CHANS = {"rx", "ry", "rz", "lx", "ly", "lz"}


def _check_bones(v, where, errs):
    if v == "all":
        return
    for b in ([v] if isinstance(v, str) else v):
        if b not in BONES:
            errs.append(f"{where}: unknown bone {b!r}")


def validate(report):
    errs = []
    for k in REQUIRED_TOP:
        if k not in report:
            errs.append(f"missing top-level {k!r}")
    if report.get("verdict") not in ("approved", "needs_work"):
        errs.append("verdict must be approved|needs_work")
    for i, f in enumerate(report.get("findings", [])):
        fid = f.get("id", f"#{i}")
        for k in ("id", "category", "severity", "frames", "bones", "observation", "fix"):
            if k not in f:
                errs.append(f"{fid}: missing {k}")
        if f.get("category") not in ("stiff", "awkward_pose", "timing", "transition"):
            errs.append(f"{fid}: bad category {f.get('category')!r}")
        if f.get("severity") not in ("high", "medium", "low"):
            errs.append(f"{fid}: bad severity {f.get('severity')!r}")
        if not f.get("fix"):
            errs.append(f"{fid}: no fix ops")
        for j, op in enumerate(f.get("fix", [])):
            where = f"{fid}.fix[{j}]"
            name = op.get("op")
            if name not in REQUIRED_OP:
                errs.append(f"{where}: unknown op {name!r}")
                continue
            for k in REQUIRED_OP[name]:
                if k not in op and not (k == "bones" and "bone" in op) and not (k == "ch" and "channel" in op):
                    errs.append(f"{where}: {name} needs {k!r}")
            if "bone" in op:
                _check_bones(op["bone"], where, errs)
            if "bones" in op:
                _check_bones(op["bones"], where, errs)
            ch = op.get("ch", op.get("channel"))
            if ch not in (None, "all"):
                for c in ([ch] if isinstance(ch, str) else ch):
                    if c not in CHANS:
                        errs.append(f"{where}: unknown channel {c!r}")
            if name in ("set_pose",) and "value" not in op and "delta" not in op:
                errs.append(f"{where}: set_pose needs value or delta")
            if name == "add_breakdown" and not ("overshoot" in op and "key_frame" in op) and not (
                    "frame" in op and ("value" in op or "delta" in op)):
                errs.append(f"{where}: add_breakdown needs frame+value/delta or key_frame+overshoot")
    if report.get("verdict") == "approved" and any(f.get("severity") in ("high", "medium") for f in report.get("findings", [])):
        errs.append("verdict approved but high/medium findings remain")
    return errs


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        try:
            with open(p) as fh:
                e = validate(json.load(fh))
        except (OSError, json.JSONDecodeError) as exc:
            e = [repr(exc)]
        print(p, "OK" if not e else "INVALID")
        for x in e:
            print("  -", x)
        bad += bool(e)
    sys.exit(1 if bad else 0)
