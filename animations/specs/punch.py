"""Punch: right cross from a guard stance. 24 frames, played once."""
GUARD_L = {"rx": -50, "rz": 15}
SPEC = {
    "name": "punch",
    "description": "Right cross: guard, small wind-up, hip/shoulder rotation into a full extension, hold, recover to guard.",
    "fps": 30,
    "frame_end": 24,
    "loop": False,
    "priority": "Action",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.1), (24, -0.1)], "ry": [(0, 0), (5, -10), (8, 15), (12, 15), (24, 0)]},
        "UpperTorso": {"ry": [(0, 0), (5, -15), (8, 25), (12, 25), (24, 0)], "rx": [(0, 5), (8, 10), (24, 5)]},
        "Head": {"ry": [(0, 0), (5, 10), (8, -20), (12, -20), (24, 0)], "rx": [(0, 5), (24, 5)]},
        "RightUpperArm": {
            "rx": [(0, -50), (5, -40), (8, -90), (12, -90), (24, -50)],
            "rz": [(0, -15), (5, -25), (8, 10), (12, 10), (24, -15)],
        },
        "RightLowerArm": {"rx": [(0, -110), (5, -120), (8, -5), (12, -5), (24, -110)]},
        "LeftUpperArm": {"rx": [(0, -50), (8, -55), (24, -50)], "rz": [(0, 15), (8, 10), (24, 15)]},
        "LeftLowerArm": {"rx": [(0, -110), (8, -115), (24, -110)]},
        "LeftUpperLeg": {"rx": [(0, -15), (24, -15)]},
        "LeftLowerLeg": {"rx": [(0, 15), (24, 15)]},
        "RightUpperLeg": {"rx": [(0, 15), (24, 15)]},
        "RightLowerLeg": {"rx": [(0, 10), (24, 10)]},
        "RightFoot": {"rx": [(0, 0), (8, 15), (24, 0)]},
    },
}
