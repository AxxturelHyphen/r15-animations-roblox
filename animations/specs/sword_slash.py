"""Sword slash: overhead diagonal slash with the right hand and a forward step. 30 frames."""
SPEC = {
    "name": "sword_slash",
    "description": "Right-handed overhead diagonal sword slash with a wind-up, a forward step, follow-through and recovery.",
    "fps": 30,
    "frame_end": 30,
    "loop": False,
    "priority": "Action",
    "props": ["sword"],
    "keys": {
        "LowerTorso": {
            "ly": [(0, -0.05), (10, -0.1), (14, -0.3), (18, -0.3), (30, -0.05)],
            "ry": [(0, 0), (10, -15), (14, 15), (18, 20), (30, 0)],
        },
        "UpperTorso": {
            "ry": [(0, 0), (10, -25), (14, 25), (18, 35), (30, 0)],
            "rx": [(0, 0), (10, -8), (14, 20), (18, 22), (30, 0)],
        },
        "Head": {"ry": [(0, 0), (10, 15), (14, -15), (18, -20), (30, 0)], "rx": [(0, 0), (10, -5), (14, 5), (30, 0)]},
        "RightUpperArm": {
            "rx": [(0, -40), (10, -160), (14, -40), (18, -10), (30, -40)],
            "rz": [(0, -10), (10, -40), (14, 10), (18, 25), (30, -10)],
        },
        "RightLowerArm": {"rx": [(0, -70), (10, -60), (14, -10), (18, -15), (30, -70)]},
        "RightHand": {"rx": [(0, 0), (10, -30), (14, 20), (18, 30), (30, 0)]},
        "LeftUpperArm": {"rx": [(0, -20), (10, -50), (14, 20), (18, 25), (30, -20)], "rz": [(0, 10), (10, 30), (14, 25), (30, 10)]},
        "LeftLowerArm": {"rx": [(0, -40), (10, -60), (14, -30), (30, -40)]},
        "LeftUpperLeg": {"rx": [(0, -10), (12, -35), (30, -10)]},
        "LeftLowerLeg": {"rx": [(0, 10), (12, 35), (30, 10)]},
        "RightUpperLeg": {"rx": [(0, 10), (12, 25), (30, 10)]},
        "RightLowerLeg": {"rx": [(0, 10), (12, 20), (30, 10)]},
    },
}
