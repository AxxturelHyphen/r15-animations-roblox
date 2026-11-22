"""Jump: anticipation crouch, take-off, airborne tuck, landing absorb and recovery. 30 frames.

The Humanoid moves the character upward in-game, so the root only shows the crouch and stretch.
"""
SPEC = {
    "name": "jump",
    "description": "Standing jump: crouch anticipation, explosive take-off with arm swing, tuck, landing absorb, recover.",
    "fps": 30,
    "frame_end": 30,
    "loop": False,
    "priority": "Movement",
    "keys": {
        "LowerTorso": {
            "ly": [(0, 0), (6, -0.75), (9, 0.1), (14, 0.0), (21, 0.0), (23, -0.65), (30, 0)],
            "lz": [(0, 0), (6, -0.3), (9, 0), (23, -0.25), (30, 0)],
        },
        "UpperTorso": {"rx": [(0, 0), (6, 30), (9, -10), (14, 5), (23, 25), (30, 0)]},
        "Head": {"rx": [(0, 0), (6, -15), (10, -5), (23, -10), (30, 0)]},
        "LeftUpperLeg": {"rx": [(0, 0), (6, -70), (9, 5), (13, -40), (18, -30), (21, -15), (23, -60), (30, 0)]},
        "LeftLowerLeg": {"rx": [(0, 0), (6, 110), (9, 5), (13, 80), (18, 60), (21, 20), (23, 100), (30, 0)]},
        "LeftFoot": {"rx": [(0, 0), (6, -30), (9, 40), (13, 20), (21, 10), (23, -30), (30, 0)]},
        "RightUpperLeg": {"rx": [(0, 0), (6, -70), (9, 5), (13, -40), (18, -30), (21, -15), (23, -60), (30, 0)]},
        "RightLowerLeg": {"rx": [(0, 0), (6, 110), (9, 5), (13, 80), (18, 60), (21, 20), (23, 100), (30, 0)]},
        "RightFoot": {"rx": [(0, 0), (6, -30), (9, 40), (13, 20), (21, 10), (23, -30), (30, 0)]},
        "LeftUpperArm": {"rx": [(0, 0), (6, 50), (10, -150), (16, -120), (23, -40), (30, 0)], "rz": [(0, 4), (10, 20), (30, 4)]},
        "LeftLowerArm": {"rx": [(0, -5), (6, -10), (10, -20), (23, -30), (30, -5)]},
        "RightUpperArm": {"rx": [(0, 0), (6, 50), (10, -150), (16, -120), (23, -40), (30, 0)], "rz": [(0, -4), (10, -20), (30, -4)]},
        "RightLowerArm": {"rx": [(0, -5), (6, -10), (10, -20), (23, -30), (30, -5)]},
    },
}
