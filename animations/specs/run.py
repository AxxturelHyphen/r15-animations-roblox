"""Run cycle, in place: 20 frames at 30 fps (two strides in about 0.67 s).

Frame 0: left foot contact, 3: down/absorb, 5-9: push-off and flight, 10: right contact.
"""
SPEC = {
    "name": "run",
    "description": "In-place R15 run cycle with forward lean, high knee recovery, pumping bent arms and a flight phase.",
    "fps": 30,
    "frame_end": 20,
    "loop": True,
    "priority": "Movement",
    "keys": {
        "LowerTorso": {
            "ly": [(0, -0.1), (3, -0.2), (6, 0.15), (10, -0.1), (13, -0.2), (16, 0.15), (20, -0.1)],
            "ry": [(0, -8), (10, 8), (20, -8)],
        },
        "UpperTorso": {"rx": [(0, 12), (10, 12), (20, 12)], "ry": [(0, 12), (10, -12), (20, 12)]},
        "Head": {"rx": [(0, -8), (20, -8)], "ry": [(0, -5), (10, 5), (20, -5)]},
        "LeftUpperLeg": {"rx": [(0, -35), (5, 10), (10, 40), (15, -55), (20, -35)]},
        "LeftLowerLeg": {"rx": [(0, 15), (3, 35), (7, 20), (10, 30), (13, 95), (15, 85), (18, 30), (20, 15)]},
        "LeftFoot": {"rx": [(0, -10), (5, 5), (10, 30), (15, -5), (20, -10)]},
        "RightUpperLeg": {"rx": [(0, 40), (5, -55), (10, -35), (15, 10), (20, 40)]},
        "RightLowerLeg": {"rx": [(0, 30), (3, 95), (5, 85), (8, 30), (10, 15), (13, 35), (17, 20), (20, 30)]},
        "RightFoot": {"rx": [(0, 30), (5, -5), (10, -10), (15, 5), (20, 30)]},
        "LeftUpperArm": {"rx": [(0, 40), (10, -50), (20, 40)], "rz": [(0, 8), (20, 8)]},
        "LeftLowerArm": {"rx": [(0, -80), (10, -95), (20, -80)]},
        "RightUpperArm": {"rx": [(0, -50), (10, 40), (20, -50)], "rz": [(0, -8), (20, -8)]},
        "RightLowerArm": {"rx": [(0, -95), (10, -80), (20, -95)]},
    },
}
