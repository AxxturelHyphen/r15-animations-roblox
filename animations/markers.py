"""Keyframe markers exported into each KeyframeSequence (Luau: track:GetMarkerReachedSignal(name)).

Markers are resolved from the FINAL curves at export time, not hard-coded frames, so they stay on the
right pose even after the critic retimes a clip.

Rules:
  ("extreme", bone, channel, "max"|"min", (start_frac, end_frac))
      the frame where the channel peaks inside that fraction of the clip (e.g. the elbow straightest = impact)
  ("speed_peak", bone, channel, (start_frac, end_frac))
      the frame of the fastest change of the channel (e.g. the middle of a sword cut)
  ("footsteps",)
      every support hand-off, i.e. the frame where the other foot becomes the lowest (value "Left"/"Right")
"""
MARKERS = {
    "punch": [("Hit", ("extreme", "RightLowerArm", "rx", "max", (0.0, 0.6)))],
    "kick": [("Hit", ("extreme", "RightLowerLeg", "rx", "min", (0.15, 0.6)))],
    "combo": [
        ("Hit1", ("extreme", "LeftLowerArm", "rx", "max", (0.0, 0.25))),
        ("Hit2", ("extreme", "RightLowerArm", "rx", "max", (0.22, 0.48))),
        ("Hit3", ("extreme", "LeftUpperArm", "rz", "max", (0.5, 0.8))),
    ],
    "sword_slash": [("Hit", ("speed_peak", "RightUpperArm", "rx", (0.25, 0.6)))],
    "high_five": [("Clap", ("extreme", "RightLowerArm", "rx", "max", (0.2, 0.45)))],
    "land_heavy": [("Impact", ("extreme", "LowerTorso", "ly", "min", (0.0, 0.3)))],
    "walk": [("Footstep", ("footsteps",))],
    "run": [("Footstep", ("footsteps",))],
    "crouch_walk": [("Footstep", ("footsteps",))],
}
