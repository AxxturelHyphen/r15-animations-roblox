"""Fall: freefall loop after a jump, arms up and out for balance, legs loose. 24 frames."""
SPEC = {
    "name": "fall",
    "description": "Freefall loop: arms raised and waving for balance, legs loosely bent and offset, looking down.",
    "fps": 30, "frame_end": 24, "loop": True, "priority": "Movement", "contact": "none",
    "keys": {
        "LowerTorso": {"rx": [(0, -4), (12, -2), (24, -4)]},
        "UpperTorso": {"rx": [(0, -6), (12, -3), (24, -6)]},
        "Head": {"rx": [(0, 12), (12, 8), (24, 12)]},
        "LeftUpperArm": {"rz": [(0, 120), (12, 135), (24, 120)], "rx": [(0, -10), (24, -10)]},
        "LeftLowerArm": {"rx": [(0, -20), (12, -35), (24, -20)]},
        "RightUpperArm": {"rz": [(0, -130), (12, -118), (24, -130)], "rx": [(0, -10), (24, -10)]},
        "RightLowerArm": {"rx": [(0, -35), (12, -20), (24, -35)]},
        "LeftUpperLeg": {"rx": [(0, -25), (12, -15), (24, -25)]},
        "LeftLowerLeg": {"rx": [(0, 30), (12, 45), (24, 30)]},
        "LeftFoot": {"rx": [(0, 20), (24, 20)]},
        "RightUpperLeg": {"rx": [(0, -5), (12, -20), (24, -5)]},
        "RightLowerLeg": {"rx": [(0, 50), (12, 30), (24, 50)]},
        "RightFoot": {"rx": [(0, 25), (24, 25)]},
    },
}
