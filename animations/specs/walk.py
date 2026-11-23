"""Walk cycle, in place: 32 frames at 30 fps (about 1.07 s per two steps).

Frame 0: left heel contact, 8: passing (right leg swings), 16: right heel contact, 24: passing.
Channel conventions are documented in rig/r15_rig.py.
"""
SPEC = {
    "name": "walk",
    "description": "In-place R15 walk cycle with heel contact, passing pose, arm swing and hip/shoulder counter-rotation.",
    "fps": 30,
    "frame_end": 32,
    "loop": True,
    "priority": "Movement",
    "keys": {
        "LowerTorso": {
            "ly": [(0, -0.03), (4, -0.08), (8, 0.05), (16, -0.03), (20, -0.08), (24, 0.05), (32, -0.03)],
            "ry": [(0, -6), (16, 6), (32, -6)],
        },
        "UpperTorso": {
            "rx": [(0, 4), (16, 4), (32, 4)],
            "ry": [(0, 9), (16, -9), (32, 9)],
        },
        "Head": {
            "ry": [(0, -3), (16, 3), (32, -3)],
            "rx": [(0, -2), (32, -2)],
        },
        "LeftUpperLeg": {"rx": [(0, -25), (8, 0), (16, 22), (24, -10), (32, -25)]},
        "LeftLowerLeg": {"rx": [(0, 5), (4, 15), (8, 5), (16, 10), (20, 40), (24, 50), (28, 15), (32, 5)]},
        "LeftFoot": {"rx": [(0, -15), (4, 0), (16, 15), (24, -5), (32, -15)]},
        "RightUpperLeg": {"rx": [(0, 22), (8, -10), (16, -25), (24, 0), (32, 22)]},
        "RightLowerLeg": {"rx": [(0, 10), (4, 40), (8, 50), (12, 15), (16, 5), (20, 15), (24, 5), (32, 10)]},
        "RightFoot": {"rx": [(0, 15), (8, -5), (16, -15), (20, 0), (32, 15)]},
        "LeftUpperArm": {"rx": [(0, 20), (16, -20), (32, 20)], "rz": [(0, 5), (32, 5)]},
        "LeftLowerArm": {"rx": [(0, -12), (16, -25), (32, -12)]},
        "RightUpperArm": {"rx": [(0, -20), (16, 20), (32, -20)], "rz": [(0, -5), (32, -5)]},
        "RightLowerArm": {"rx": [(0, -25), (16, -12), (32, -25)]},
    },
}
